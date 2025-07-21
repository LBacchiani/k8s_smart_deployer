import os
import uuid
import yaml
from code_generation.utilities import to_dns_name

class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


def enumerate_service_groups(input_list):
    service_groups = {}
    result = []

    for host, service in input_list:
        if service not in service_groups:
            service_groups[service] = 0
        result.append((host, service_groups[service], service))
        service_groups[service] += 1

    return result


def add_pod_definitions(order, components):
    component_mapping = {comp['metadata']['labels']['type']: comp for comp in components}
    pod_definitions = []
    name_to_variable = {}
    indexed_services = enumerate_service_groups(order)

    service_variable_map = {}
    for node_name, service_idx, service_name in indexed_services:
        variable_name = f"{service_name}-{to_dns_name(str(uuid.uuid4()))}".replace("-type", "")
        if service_name not in name_to_variable:
            name_to_variable[service_name] = []
        name_to_variable[service_name].append(variable_name)
        service_variable_map[(node_name, service_idx, service_name)] = variable_name

    for node_name, service_idx, service_name in indexed_services:
        variable_name = name_to_variable[service_name][service_idx]
        component = component_mapping.get(service_name)
        if not component:
            continue

        kind = component.get("kind")
        mapped_dependencies = {}
        
        ports_required = component.get('ports', {}).get('strong', [])
        for entry in ports_required:
            dep_name = entry.get("id")
            dep_type = entry.get("type")
            dep_count = entry.get("value", 1)
            if dep_name:
                mapped_dependencies[dep_name] = [dep_type, dep_count]
        

        depends_on = []
        if kind == 'Pod':
            containers = component['spec']['containers']
            for container in containers:
                env_list = container.get("env", [])
                for dep_name, dep_info in mapped_dependencies.items():
                    dep_type = dep_info[0]
                    dep_count =  dep_info[1]
                    if dep_type in name_to_variable:
                        value = name_to_variable[dep_type][0]
                        env_list.append({"name": dep_name, "value": value})
                        depends_on.extend(f"${{{name_to_variable[dep_type][i]}}}" for i in range(dep_count))

            props = create_pod_definition(variable_name, component, node_name)

        elif kind == 'Service':
            props = create_service_definition(variable_name, component)
            for dep_name, dep_info in mapped_dependencies.items():
                count = dep_info[0]
                if dep_name in name_to_variable:
                    depends_on.extend(f"${{{name_to_variable[dep_name][i]}}}" for i in range(count))

        pod_definitions.append({
            'name': variable_name,
            'type': 'kubernetes:core/v1:Pod' if kind == 'Pod' else 'kubernetes:core/v1:Service',
            'properties': props,
            'options': {"dependsOn": depends_on} if depends_on else {}
        })

    return pod_definitions


def create_pod_definition(name, component, node_name):
    return {
        'apiVersion': 'v1',
        'kind': 'Pod',
        'metadata': {
            'name': name,
            'labels': component['metadata'].get('labels', {}) 
        },
        'spec': {
            'nodeName': node_name,
            'containers': component['spec']['containers']
        }
    }


def create_service_definition(name, component):
    return {
        'apiVersion': 'v1',
        'kind': 'Service',
        'metadata': {
            'name': name,
            'labels': component['metadata'].get('labels', {}) 
        },
        'spec': component['spec']
    }


def no_dash_representer(dumper, value):
    return dumper.represent_mapping('tag:yaml.org,2002:map', value.items(), flow_style=False)


def generate_yaml_definition(order, components, folder_name):
    os.makedirs(folder_name, exist_ok=True)
    yaml.add_representer(dict, no_dash_representer)

    pulumi_yaml = {
        'name': 'my-k8s-app',
        'runtime': 'yaml',
        'resources': {
            pod['name']: pod for pod in add_pod_definitions(order, components)
        }
    }

    with open(f"{folder_name}/pulumi_deployment.yaml", "w") as file:
        yaml.dump(pulumi_yaml, file, default_flow_style=False, Dumper=NoAliasDumper, sort_keys=False)
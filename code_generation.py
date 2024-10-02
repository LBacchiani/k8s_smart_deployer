from jinja2 import Environment, FileSystemLoader
import yaml
import os

class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


def prepare_deployment_data(order, components):
    component_mapping = {comp['metadata']['name']: comp for comp in components}
    deployment_data = []
    deployed_services = []

    def create_service_data(node_name, service_name, service_index, component):
        return {
            "node_name": node_name,
            "service_name": service_name,
            "service_index": service_index,
            "image": component['spec']['template']['spec']['containers'][0]['image'],
            "cpu": component['spec']['template']['spec']['containers'][0]['resources']['requests']['cpu'],
            "memory": component['spec']['template']['spec']['containers'][0]['resources']['requests']['memory'],
            "depends_on": [
                {"service_name": dep_service["service_name"], "service_index": dep_service["service_index"]}
                for dep_service in deployed_services
            ]
        }

    if not order:
        # If order is empty, create service data for all components without dependencies
        for component in components:
            service_data = create_service_data(
                node_name=component['metadata']['name'],  # Placeholder node name
                service_name=component['metadata']['name'],
                service_index=0,  # Default index
                component=component
            )
            deployment_data.append([service_data])  # Wrap in list to maintain structure
        return deployment_data

    for service_info_set in order:
        service_group = []
        for service_info in service_info_set:
            node_name = service_info[0]
            service_name = service_info[2]
            service_index = service_info[3]

            component = component_mapping.get(service_name)
            if component:
                service_data = create_service_data(
                    node_name=node_name,
                    service_name=service_name,
                    service_index=service_index,
                    component=component
                )
                service_group.append(service_data)

        deployment_data.append(service_group)
        deployed_services.extend(service_group)

    return deployment_data



def generate_python_script(resources, order, components, folder_name):
    os.makedirs(f"deployments/{folder_name}", exist_ok=True)
    file_loader = FileSystemLoader('script_template')
    env = Environment(loader=file_loader)
    template = env.get_template('orchestration_program.jinja2')

    deployment_data = prepare_deployment_data(order, components)
    rendered_script = template.render(deployment_data=deployment_data)

    with open(f"deployments/{folder_name}/pulumi_deployment.py", 'w') as f:
        f.write(rendered_script)

    with open(f"deployments/{folder_name}/vm_annotations.yaml", "w") as file:
        yaml.dump(resources, file, default_flow_style=False)


def generate_yaml(node_name, config_file, folder_name):
    os.makedirs(f"deployments/{folder_name}/manifests", exist_ok=True)
    files_dict = {}
    service_name = config_file['metadata']['name']
    replicas = config_file['spec']['replicas']
    for r in range(replicas):
        file_name = "deployments/" + folder_name + "/manifests/" + node_name + "_" + service_name + "_" + str(r) + ".yaml"
        name = 'sys-' + config_file['metadata']['name'] + '-'
        generate_name = {'generateName': name}
        files_dict[file_name] = {'apiVersion': 'v1',
                                 'kind': 'Pod',
                                 'metadata': generate_name,
                                 'spec': {**config_file['spec']['template']['spec'], 'nodeName': node_name}}
        with open(file_name, "w") as file:
            yaml.dump(files_dict[file_name], file)


def create_pod_definition(component, containers, node_name):
    return {
        'apiVersion': 'v1',
        'kind': 'Pod',
        'metadata': {
            'name': component,
            'labels': {'app': component}
        },
        'spec': {
            'nodeName': node_name,
            'containers': containers
        }
    }


def add_pod_definitions(components, order=None):
    pod_definitions = []
    previous_pods = []

    if not order:
        for comp in components:
            service_name = comp['metadata']['name']
            containers = comp['spec']['template']['spec']['containers']
            pod_definitions.append({
                'name': f"{service_name}-pod",
                'type': 'kubernetes:core/v1:Pod',
                'properties': create_pod_definition(service_name, containers, "default-node"),
                'options': {}
            })
    else:
        for group in order:
            current_pods = []
            for node, _, service_name, service_index in group:
                component = f"{service_name}-{service_index}"
                containers = next(comp['spec']['template']['spec']['containers']
                                  for comp in components if comp['metadata']['name'] == service_name)

                pod_def = {
                    'name': f"{component}-pod",
                    'type': 'kubernetes:core/v1:Pod',
                    'properties': create_pod_definition(component, containers, node),
                    'options': {'dependsOn': previous_pods} if previous_pods else {}
                }
                pod_definitions.append(pod_def)
                current_pods.append(f"${{{component}-pod}}")

            previous_pods = current_pods

    return pod_definitions

def generate_pulumi_yaml_definition(resources, order, components, folder_name):
    os.makedirs(f"deployments/{folder_name}", exist_ok=True)

    pulumi_yaml = {
        'name': 'my-k8s-app',
        'runtime': 'yaml',
        'resources': {pod['name']: pod for pod in add_pod_definitions(components, order)}
    }

    with open(f"deployments/{folder_name}/pulumi_deployment.yaml", "w") as file:
        yaml.dump(pulumi_yaml, file, default_flow_style=False, Dumper=NoAliasDumper)

    with open(f"deployments/{folder_name}/vm_annotations.yaml", "w") as file:
        yaml.dump(resources, file, default_flow_style=False)

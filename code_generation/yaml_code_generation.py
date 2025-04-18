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
    component_mapping = {comp['metadata']['name']: comp for comp in components}
    pod_definitions = []
    mapped = []
    name_to_variable = {}

    indexed_services = enumerate_service_groups(order)

    for node_name, service_idx, service_name in indexed_services:
        variable_name = service_name + '-' + to_dns_name(str(uuid.uuid4()))
        if service_name not in name_to_variable:
            name_to_variable[service_name] = []
        if 'ports' in component_mapping[service_name]:
            mapped = dict(map(lambda x: x.values(), component_mapping[service_name]['ports']['required']['strong']))

        pod_definitions.append({
            'name': variable_name,
            'type': 'kubernetes:core/v1:Pod',
            'properties': create_pod_definition(service_name, service_idx, component_mapping[service_name]['spec']['containers'], node_name) if component_mapping[service_name]['kind'] == 'Pod' else create_service_definition(service_name, component_mapping[service_name]['spec']),
            'options': {"dependsOn": [f"${{{name_to_variable[k][i]}}}" for k in mapped for i in range(mapped[k])]} if mapped else {}
        })
        name_to_variable[service_name] += [variable_name]
    return pod_definitions


def create_pod_definition(component, service_idx, containers, node_name):
    return {
        'apiVersion': 'v1',
        'kind': 'Pod',
        'metadata': {
            'name': component+ "-" + str(service_idx) + "-${pulumi.stack}",
            'labels': {'app': component}
        },
        'spec': {
            'nodeName': node_name,
            'containers': containers
        }
    }

def create_service_definition(component, spec):
    return {
        'apiVersion': 'v1',
        'kind': 'Service',
        'metadata': {
            'name': component,
        }, 
        'spec': spec
        # 'spec': {
        #     'nodeName': node_name,
        #     'containers': containers
        # }
    }


def no_dash_representer(dumper, value):
    return dumper.represent_mapping('tag:yaml.org,2002:map', value.keys(), flow_style=False)


def generate_yaml_definition(order, components, folder_name):
    os.makedirs(f"{folder_name}", exist_ok=True)
    yaml.add_representer(dict, no_dash_representer)
    pulumi_yaml = {
        'name': 'my-k8s-app',
        'runtime': 'yaml',
        'resources': {pod['name']: pod for pod in add_pod_definitions(order, components)}
    }
    with open(f"{folder_name}/pulumi_deployment.yaml", "w") as file:
        yaml.dump(pulumi_yaml, file, default_flow_style=False, Dumper=NoAliasDumper, sort_keys=False)
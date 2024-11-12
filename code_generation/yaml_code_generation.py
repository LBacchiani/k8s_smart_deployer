import os
import uuid
import yaml
from code_generation.utilities import to_valid_variable_name


class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True

def add_pod_definitions(order, components):
    component_mapping = {comp['metadata']['name']: comp for comp in components}
    pod_definitions = []
    previous_pods = []

    for node in order:
        for service in order[node]:
            service_name = service[0] + '_' + to_valid_variable_name(str(uuid.uuid4()))
            container = component_mapping[service[0]]['spec']['template']['spec']['containers']
            pod_definitions += [{'name': service_name, 'type': 'kubernetes:core/v1:Pod',
                                 'properties': create_pod_definition(service_name, container, "default-node"),
                                 'options': {}}]
            print(component_mapping[service[0]]['spec']['template']['spec']['containers'])

    exit("BASTA")
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
                containers = next(comp['spec']['template']['spec']['containers'] for comp in components if comp['metadata']['name'] == service_name)
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


def generate_yaml_definition(order, components, folder_name):
    os.makedirs(f"{folder_name}", exist_ok=True)

    pulumi_yaml = {
        'name': 'my-k8s-app',
        'runtime': 'yaml',
        'resources': {pod['name']: pod for pod in add_pod_definitions(order, components)}
    }

    with open(f"deployments/{folder_name}/pulumi_deployment.yaml", "w") as file:
        yaml.dump(pulumi_yaml, file, default_flow_style=False, Dumper=NoAliasDumper)
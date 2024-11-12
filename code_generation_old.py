from jinja2 import Environment, FileSystemLoader
import yaml
import os
import re
import uuid


class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True

def add_pod_definitions(components, excluded_services, order=None,):
    if excluded_services is None:
        excluded_services = []

    excluded_service_names = set(excluded_services.get('services_present', {}).get('name', []))
    pod_definitions = []
    previous_pods = []

    if not order:
        for comp in components:
            service_name = comp['metadata']['name']
            if service_name not in excluded_service_names:
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
                if service_name not in excluded_service_names:
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

def generate_pulumi_yaml_definition(order, components, folder_name, excluded_services=None):
    if excluded_services is None:
        excluded_services = []
    os.makedirs(f"deployments/{folder_name}", exist_ok=True)

    pulumi_yaml = {
        'name': 'my-k8s-app',
        'runtime': 'yaml',
        'resources': {pod['name']: pod for pod in add_pod_definitions(components, excluded_services, order)}
    }

    with open(f"deployments/{folder_name}/pulumi_deployment.yaml", "w") as file:
        yaml.dump(pulumi_yaml, file, default_flow_style=False, Dumper=NoAliasDumper)
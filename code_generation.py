import yaml
import os

class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True

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
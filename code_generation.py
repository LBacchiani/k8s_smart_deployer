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

def generate_pulumi_yaml_definition(resources, order, components, folder_name):
    pulumi_pod_definitions = []
    previous_pods = []

    for group in order:
        current_pods = []
        for (node, _, service_name, service_index) in group:
            component = f"{service_name}-{service_index}"
            yaml_file = list(filter(lambda x: x['metadata']['name'] == service_name, components))[0]
            containers = yaml_file['spec']['template']['spec']['containers']

            pod_definition = {
                'name': f"{component}-pod",
                'type': 'kubernetes:core/v1:Pod',
                'properties': create_pod_definition(component, containers, node),
                'options': {}
            }

            if previous_pods:
                pod_definition['options']['dependsOn'] = previous_pods

            pulumi_pod_definitions.append(pod_definition)
            current_pods.append("${" + f"{component}-pod" + "}")

        previous_pods = current_pods

    file_name = f"deployments/{folder_name}/pulumi_deployment.yaml"
    pulumi_yaml = {
        'name': 'my-k8s-app',
        'runtime': 'yaml',
        'resources': {pod['name']: pod for pod in pulumi_pod_definitions}
    }

    with open(file_name, "w") as file:
        yaml.dump(pulumi_yaml, file, default_flow_style=False, Dumper=NoAliasDumper)

    file_name = f"deployments/{folder_name}/vm_annotations.yaml"
    with open(file_name, "w") as file:
        yaml.dump(resources, file, default_flow_style=False)
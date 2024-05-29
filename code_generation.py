import yaml
import os


def generate_yaml(node_name, config_file):
    os.makedirs("deployments", exist_ok=True)
    files_dict = {}
    service_name = config_file['metadata']['name']
    print(service_name)
    replicas = config_file['spec']['replicas']
    for r in range(replicas):
        file_name = "deployments/" + node_name + "_" + service_name + "_" + str(r) + ".yaml"
        files_dict[file_name] = {'apiVersion': 'v1',
                                 'kind': 'Pod',
                                 'metadata': config_file['metadata'],
                                 'spec': {**config_file['spec']['template']['spec'], 'nodeName': node_name}}
        with open(file_name, "w") as file:
            yaml.dump(files_dict[file_name], file)

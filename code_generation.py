import yaml
import os
import shutil

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

def insert_deploy_script(folder_name):
    os.makedirs(f"deployments/{folder_name}", exist_ok=True)
    shutil.copyfile('./script_template/deployer.py', f'deployments/{folder_name}/deployer.py')

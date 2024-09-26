import json
import sys
import yaml
import glob
from code_generation import *

from optimizer import Optimizer

if __name__ == '__main__':
    args = sys.argv[1:]
    kubelet_reserved_ram = int(args[0])
    reserved_kublet_cpu = int(args[1])
    path = args[2]  # 'annotation_examples/test1/'
    folder_name = path.split('/')[-2]
    print(folder_name)
    extension = '*.yaml'
    file_paths = glob.glob(f"{path}/{extension}")
    vm_file = path + args[3]
    with open(vm_file, 'r') as f:
        vm_properties = yaml.load(f, Loader=yaml.FullLoader)
    port = args[4]
    components = []
    for file_path in file_paths:
        if vm_file != file_path:
            with open(file_path, 'r') as f:
                components.append(yaml.load(f, Loader=yaml.FullLoader))
    optimizer = Optimizer(reserved_kublet_cpu, kubelet_reserved_ram, port, '--solver, lex-or-tools')
    configuration, resources, order = optimizer.optimize(vm_properties, components)
    print(order)
    for node in configuration["configuration"]['locations']:
        for component in configuration["configuration"]['locations'][node]['0']:
            yaml_file = list(filter(lambda x: x['metadata']['name'] == component, components))[0]
            generate_yaml(node, yaml_file, folder_name)
    insert_deploy_script(folder_name)
    file_name = f"deployments/{folder_name}/vm_annotations.yaml"
    with open(file_name, "w") as file:
        yaml.dump(resources, file)

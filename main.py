import sys
import glob
from code_generation import *
import yaml

from optimizer import Optimizer

if __name__ == '__main__':
    args = sys.argv[1:]
    kubelet_reserved_ram = int(args[0])
    reserved_kublet_cpu = int(args[1])
    path = args[2]
    folder_name = path.split('/')[-2]
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
    _, resources, order = optimizer.optimize(vm_properties, components)
    generate_pulumi_yaml_definition(resources, order, components, folder_name)
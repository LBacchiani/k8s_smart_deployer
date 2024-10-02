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
    configuration_file = path + args[3]
    with open(configuration_file, 'r') as f:
        configuration = list(yaml.safe_load_all(f))
    port = args[4]
    components = []
    for file_path in file_paths:
        if configuration_file != file_path:
            with open(file_path, 'r') as f:
                components.append(yaml.load(f, Loader=yaml.FullLoader))
    optimizer = Optimizer(reserved_kublet_cpu, kubelet_reserved_ram, port, '--solver, lex-or-tools')
    _, resources, order = optimizer.optimize(configuration, components)
    generate_python_script(resources, order, components, folder_name)
    #generate_pulumi_yaml_definition(resources, order, components, folder_name)
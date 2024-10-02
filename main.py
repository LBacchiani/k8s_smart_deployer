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
        configurations = list(yaml.safe_load_all(f))
        vm_config = configurations[0]
        if len(configurations) == 2:
            excluded_services = configurations[1]
        else:
            excluded_services = None

    port = args[4]
    output_format = args[5].lower()
    components = []
    for file_path in file_paths:
        if configuration_file != file_path:
            with open(file_path, 'r') as f:
                components.append(yaml.load(f, Loader=yaml.FullLoader))
    optimizer = Optimizer(reserved_kublet_cpu, kubelet_reserved_ram, port, '--solver, lex-or-tools')
    _, resources, order = optimizer.optimize(vm_config, components)
    # Use the output_format to determine which generation function to call
    if output_format == 'python':
        generate_python_script(resources, order, components, folder_name, excluded_services)
    elif output_format == 'yaml':
        generate_pulumi_yaml_definition(resources, order, components, folder_name, excluded_services)
    else:
        print(f"Unsupported output format: {output_format}")
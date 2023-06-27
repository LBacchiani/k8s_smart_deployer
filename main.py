import json
import sys
import yaml
import glob
from code_generation import *

from optimizer import Optimizer

if __name__ == '__main__':

    ######ARGS######
    args = sys.argv[1:]
    kubelet_reserved_ram = int(args[0])
    reserved_kublet_cpu = int(args[1])
    path = args[2]
    port = args[3]

    ######EXTRACTION#######
    files = os.listdir(path)
    components = []
    vm_properties = {}
    for file_name in files:
        file_path = os.path.join(path, file_name)
        with open(file_path, 'r') as f:
            if file_path.endswith('.yaml') or file_path.endswith('.yml'):
                components.append(yaml.load(f, Loader=yaml.FullLoader))
            elif file_path.endswith('.json'):
                vm_properties = json.load(f)
    #######

    ####OPTIMAL DEPLOYMENT PROBLEM SOLUTION######
    optimizer = Optimizer(reserved_kublet_cpu, kubelet_reserved_ram, port, '--solver, lex-or-tools')
    configuration = optimizer.optimize(vm_properties, components)
    resources = optimizer.update_usage(configuration['configuration']['locations'])
    configuration = optimizer.normalize_names(configuration)
    #####################

    #######CODE GENERATION########
    for node in configuration["configuration"]['locations']:
        for component in configuration["configuration"]['locations'][node]['0']:
            yaml_file = list(filter(lambda x: x['metadata']['name'] == component, components))[0]
            generate_yaml(node, component, yaml_file, configuration["configuration"]['locations'][node]['0'][component])
    file_name = "deployments/vm_annotations.json"

    with open(file_name, "w") as file: json.dump(resources, file, indent=4)
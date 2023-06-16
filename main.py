import json
import os
import yaml
import glob

from optimizer import Optimizer

if __name__ == '__main__':
    path = 'annotation_examples/test1/'
    extension = '*.yaml'
    file_paths = glob.glob(f"{path}/{extension}")
    vm_properties = json.load(open(path + 'vm_annotation.json')) #TODO PASS AS PARAMETER
    kubelet_reserved_ram = 0 #TODO PASS AS PARAMETER
    reserved_kublet_cpu = 0 #TODO PASS AS PARAMETER
    components = []
    for file_path in file_paths:
        with open(file_path, 'r') as f:
            components.append(yaml.load(f, Loader=yaml.FullLoader))
    optimizer = Optimizer(reserved_kublet_cpu, kubelet_reserved_ram, '--solver, lex-or-tools')
    optimizer.optimize(vm_properties, components)

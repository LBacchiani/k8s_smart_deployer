import json
import os
import sys
import yaml
import glob

from optimizer import Optimizer

if __name__ == '__main__':
    args = sys.argv[1:]
    kubelet_reserved_ram = int(args[0])
    reserved_kublet_cpu = int(args[1])
    path = args[2] #'annotation_examples/test1/'
    extension = '*.yaml'
    file_paths = glob.glob(f"{path}/{extension}")
    vm_properties = json.load(open(path + args[3]))
    port = args[4]
    components = []
    for file_path in file_paths:
        with open(file_path, 'r') as f:
            components.append(yaml.load(f, Loader=yaml.FullLoader))
    optimizer = Optimizer(reserved_kublet_cpu, kubelet_reserved_ram, port, '--solver, lex-or-tools')
    optimizer.optimize(vm_properties, components)

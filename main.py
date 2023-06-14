import json
import os
import yaml

from optimizer import Optimizer

if __name__ == '__main__':
    vm_properties = json.load(open("annotation_examples/vm_annotation_example.json")) #TODO PASS AS PARAMETER
    components = []
    for filename in os.listdir("annotation_examples/test1"): #TODO PASS PATH AS PARAMETER
        with open(os.path.join("annotation_examples/test1", filename), 'r') as f:
            components.append(yaml.load(f, Loader=yaml.FullLoader))
    kubelet_reserved_ram = 0 #TODO PASS AS PARAMETER
    reserved_kublet_cpu = 0 #TODO PASS AS PARAMETER
    optimizer = Optimizer(reserved_kublet_cpu, kubelet_reserved_ram)
    optimizer.optimize(vm_properties, components)

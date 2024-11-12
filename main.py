import sys

import yaml
from code_generation.python_code_generation import generate_python_script
from code_generation.yaml_code_generation import generate_yaml_definition
from utilities import *
from optimizer import Optimizer
import os


if __name__ == '__main__':
    args = sys.argv[1:]
    resource_folder = args[0] + '/'

    #load declarative specifications
    components = []
    kubelet_ram = "0"
    kubelet_cpu = "0"
    existing_dep = {}
    vms = {}
    port = args[1]
    language = args[2]
    target_folder = './deployment'
    for filename in os.listdir(resource_folder):
        with open(resource_folder + filename, 'r') as f:
            configurations = list(yaml.safe_load_all(f))
            if len(configurations) == 1: components.append(configurations[0])
            else:
                for c in configurations:
                    if 'kubelet' in c:
                        kubelet_ram = c['kubelet']['resources']['memory']
                        kubelet_cpu = c['kubelet']['resources']['cpu']
                    if 'nodes' in c:
                        vms = c['nodes']
                    if 'existingDependencies' in c:
                        for dep in c['existingDependencies']:
                            existing_dep[dep['name']] = dep['value']

    #manage dependencies already satisfied#
    for c in components:
        if 'ports' in c:
            dependencies_left = []
            for dep in c['ports']['required']['strong']:
                name, val = dep['name'], dep['value']
                res = val - existing_dep[name]
                if res > 0:
                    dependencies_left.append({'name': name, 'value': res})
            if not dependencies_left:
                del c['ports']
            else:
                c['ports']['required']['strong'] = dependencies_left


    #compute configuration
    optimizer = Optimizer(kubelet_cpu, kubelet_ram, port, '--solver, lex-or-tools')
    configuration = optimizer.optimize(vms, components)
    ###compute resource left
    for comp in components:
        if comp['metadata']['name'] in existing_dep:
            existing_dep[comp['metadata']['name']] += comp['spec']['replicas']
        else:
            existing_dep[comp['metadata']['name']] = comp['spec']['replicas']
    placement = {x: [(y, configuration['configuration']['locations'][x]['0'][y]) for y in configuration['configuration']['locations'][x]['0']] for x in configuration['configuration']['locations']}
    requirements = {x['metadata']['name']: x['spec']['template']['spec']['containers'][0]['resources']['requests'] for x in components}
    resource_left = update_usage(placement, requirements, vms, kubelet_cpu, kubelet_ram)
    os.makedirs(target_folder, exist_ok=True)
    with open(f"{target_folder}/vm_annotations.yaml", "w") as file:
        yaml.dump({'nodes': resource_left}, file, default_flow_style=False)
        file.write('---\n')
        yaml.dump({'existingDependencies': [{'name': k, 'value': existing_dep[k]} for k in existing_dep]}, file, default_flow_style=False)

    ##code generation##
    order = get_topological_sort(configuration['optimized_bindings'])

    if not order:
        order = [(k, x) for k in configuration['configuration']['locations']
                        for x in configuration['configuration']['locations'][k]['0']
                        for _ in range(configuration['configuration']['locations'][k]['0'][x])
                ]
    if language == 'python':
        generate_python_script(order, components, target_folder)
    elif language == 'yaml':
        generate_yaml_definition(order, components, target_folder)
    else:
        print(f"Unsupported output format: {language}")
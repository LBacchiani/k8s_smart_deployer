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
    services = args[1] + '/'
    target_decl = args[2]
    vms_decl = args[3]
    port = args[4]
    language = args[5]
    target_folder = './deployment'

    components = []
    vms = {}
    target_requirements = None


    #load services declarative specifications
    for filename in os.listdir(resource_folder + services):
        with open(resource_folder + services + filename, 'r') as f:
            configurations = list(yaml.safe_load_all(f))
            components.append(configurations[0])

    #load vms declarative specifications
    with open(resource_folder + vms_decl, 'r') as f:
        vms = list(yaml.safe_load_all(f))[0]

    #load target desiderata declarative specifications
    existing_dep = {}
    with open(resource_folder + target_decl, 'r') as f:
        target_requirements = list(yaml.safe_load_all(f))[0]
        if 'existingDependencies' in target_requirements:
            for dep in target_requirements['existingDependencies']:
                existing_dep[dep['name']] = dep['value']

    #remove strong dep already satisfied
    for c in components:
        if 'ports' in c:
            dependencies_left = []
            for dep in c['ports']['required']['strong']:
                name, val = dep['name'], dep['value']
                if name in existing_dep:
                    val -= existing_dep[name]
                if val > 0:
                    dependencies_left.append({'name': name, 'value': val})
            if not dependencies_left:
                del c['ports']
            else:
                c['ports']['required']['strong'] = dependencies_left
    
    #compute configuration
    optimizer = Optimizer(port, '--solver, lex-or-tools')
    configuration = optimizer.optimize(vms, components, target_requirements)

    ###compute resource left
    placement = {x: [(y, configuration['configuration']['locations'][x]['0'][y]) for y in configuration['configuration']['locations'][x]['0']] for x in configuration['configuration']['locations']}
    requirements = {refine_name(x['metadata']['name']): x['spec']['containers'][0]['resources']['requests'] if x['kind'] == 'Pod' else {'cpu': '0m', 'memory': '0M'} for x in components}

    resource_left = update_usage(placement, requirements, vms)
    os.makedirs(target_folder, exist_ok=True)
    with open(f"{target_folder}/vm_annotations.yaml", "w") as file:
        yaml.dump({'nodes': resource_left}, file, default_flow_style=False)

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
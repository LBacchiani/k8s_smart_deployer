import sys

import yaml
from code_generation.python_code_generation import generate_python_script
from code_generation.yaml_code_generation import generate_yaml_definition
from code_generation.utilities import replace_underscores
from utilities import *
from optimizer import Optimizer
import os


if __name__ == '__main__':
    args = sys.argv[1:]
    services = args[0] + '/'
    target_decl = args[1]
    vms_decl = args[2]
    port = args[3]
    language = args[4]
    target_folder = './deployment'

    components = []
    vms = {}
    target_requirements = None


    #load services declarative specifications
    for filename in os.listdir( services):
        with open(services + filename, 'r') as f:
            configurations = list(yaml.safe_load_all(f))
            components.append(configurations[0])

    #load vms declarative specifications
    with open(vms_decl, 'r') as f:
        vms = list(yaml.safe_load_all(f))[0]

    #load target desiderata declarative specifications
    existing_dep = {}
    with open(target_decl, 'r') as f:
        target_requirements = list(yaml.safe_load_all(f))[0]
        if 'existingResources' in target_requirements:
            for dep in target_requirements['existingResources']:
                existing_dep[dep['type']] = dep['value']

    #remove strong dep already satisfied
    deleted_deps = {}
    for c in components:
        comp_type = c['metadata']['labels']['type']
        if 'ports' in c:
            dependencies_left = []
            for dep in c['ports']['strong']:
                dep_type = dep['type']
                val = 1 if 'value' not in dep else dep['value']
                env = ""
                if 'id' in dep:
                    env = dep['id']
                if dep_type in existing_dep:
                    val -= existing_dep[dep_type]
                if val <= 0:
                    out = {'type': dep_type, 'value': dep['value'] if 'value' in dep else 1}
                    if env != "":
                        out['id'] = env
                    deleted_deps.setdefault(comp_type, []).append(out)
                if val > 0:
                    out = {'type': dep_type, 'value': val}
                    if env != "":
                        out['id'] = env
                    dependencies_left.append(out)
            if not dependencies_left:
                del c['ports']
            else:
                c['ports']['strong'] = dependencies_left

    #compute configuration
    optimizer = Optimizer(port, '--solver, lex-or-tools')
    configuration = replace_underscores(optimizer.optimize(vms, components, target_requirements))
    ###compute resource left
    placement = {x: [(y, configuration['configuration']['locations'][x]['0'][y]) for y in configuration['configuration']['locations'][x]['0']] for x in configuration['configuration']['locations']}
    requirements = {x['metadata']['labels']['type']: x['spec']['containers'][0]['resources']['requests'] if x['kind'] == 'Pod' else {'cpu': '0m', 'memory': '0M'} for x in components}

    resource_left = update_usage(placement, requirements, vms)
    os.makedirs(target_folder, exist_ok=True)
    with open(f"{target_folder}/vm_annotations.yaml", "w") as file:
        yaml.dump({'nodes': resource_left}, file, default_flow_style=False)

    ##code generation##
    order = get_topological_sort(configuration['optimized-bindings'])

    if not order:
        order = [(k, x) for k in configuration['configuration']['locations']
                        for x in configuration['configuration']['locations'][k]['0']
                        for _ in range(configuration['configuration']['locations'][k]['0'][x])
                ]

    # put back existing dependencies in components ports
    for c in components:
        comp_type = c['metadata']['labels']['type']
        if comp_type in deleted_deps:
            if 'ports' in c:
                c['ports']['strong'].extend(deleted_deps[comp_type])
            else:
                c['ports'] = {'strong': deleted_deps[comp_type]}
                
    if language == 'python':
        generate_python_script(order, components, target_folder)
    elif language == 'yaml':
        generate_yaml_definition(order, components, target_folder)
    else:
        print(f"Unsupported output format: {language}")
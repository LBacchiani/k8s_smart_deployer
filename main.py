import sys
from code_generation import *
import yaml
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
    existing_dep = []
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
                        existing_dep = c['existingDependencies']['name']
    #compute configuration
    optimizer = Optimizer(kubelet_cpu, kubelet_ram, port, '--solver, lex-or-tools')
    configuration = optimizer.optimize(vms, components)

    ###compute resource left
    existing_dep += [x['provider'] for x in configuration['configuration']['bindings']]
    placement = {x: [(y,configuration['configuration']['locations'][x]['0'][y]) for y in configuration['configuration']['locations'][x]['0']] for x in configuration['configuration']['locations']}
    requirements = {x['metadata']['name']: x['spec']['template']['spec']['containers'][0]['resources']['requests'] for x in components}
    resource_left = update_usage(placement, requirements, vms, kubelet_cpu, kubelet_ram)
    os.makedirs(target_folder, exist_ok=True)
    with open(f"{target_folder}/vm_annotations.yaml", "w") as file:
        yaml.dump(resource_left, file, default_flow_style=False)
        file.write('---\n')
        yaml.dump({'existingDependencies': {'name': existing_dep}}, file, default_flow_style=False)

    ##the topological sort must be done during code gen##
    # Use the output_format to determine which generation function to call
    # if language == 'py':
    #     generate_python_script(resources, order, components, folder_name, excluded_services)
    # elif language == 'yaml':
    #     generate_pulumi_yaml_definition(resources, order, components, folder_name, excluded_services)
    # else:
    #     print(f"Unsupported output format: {output_format}")
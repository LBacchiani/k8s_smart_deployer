import json
import sys
from code_generation import *
from optimizer import *
from requests import post as requests_post


if __name__ == '__main__':

    ######ARGS######
    args = sys.argv[1:]
    kubelet_reserved_ram = int(args[0])
    reserved_kublet_cpu = int(args[1])
    path = args[2]
    port = args[3]
    options = '--solver, lex-or-tools'

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
    nodes_specification = nodes_specs(vm_properties, reserved_kublet_cpu, kubelet_reserved_ram)
    zephyrus_query = build_query(nodes_specification, components, [x.strip() for x in options.split(',')] if options else None)
    query_url = 'http://localhost:{}/process'.format(port)
    configuration = requests_post(query_url, data=json.dumps(zephyrus_query)).json()
    if 'error' in configuration:
        print('Configuration not found')
        exit()
    print(json.dumps(configuration, indent=4))
    #####################

    #######CODE GENERATION########
    # for node in configuration["configuration"]['locations']:
    #     for component in configuration["configuration"]['locations'][node]['0']:
    #         yaml_file = list(filter(lambda x: refine_name(x['metadata']['name']) == component, components))[0]
    #         add_target_node(node, component, yaml_file, configuration["configuration"]['locations'][node]['0'][component])
    # file_name = "deployments/vm_annotations.json"
    # with open(file_name, "w") as file: json.dump(resources, file, indent=4)
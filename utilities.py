from re import match as re_match
import toposort


def cpu_convertion(cpu):
    '''k8s allows for fractional CPUs, in two units: 100m (millicpu/millicores) or 0.1.'''
    try:
        if cpu.endswith('m'):
            return int(cpu[:-1])
        else: return int(float(cpu) * 1000)
    except ValueError:
        raise Exception('Argument not a CPU measurement: \'{}\''.format(cpu))


def ram_convertion(ram):
    '''k8s allows the following RAM suffixes: E, Ei, P, Pi, T, Ti, G, Gi, M, Mi, K or Ki.'''
    try:
        val, unit = re_match(r'(\d+)(\w+)', ram).groups()
    except AttributeError:
        raise Exception('Argument not a RAM measurement: \'{}\''.format(ram))
    if unit == 'M': return int(val) # Megabyte
    if unit == 'Mi': return int(int(val) * 1.049) # Mebibyte
    if unit == 'K': return int(int(val) / 1000) # Kilobyte
    if unit == 'Ki': return int(int(val) / 976.562) # Kibibyte
    if ram.isdigit(): return int(int(val) / 1e+6) # Byte
    if unit == 'G': return int(int(val) * 1000) # Gigabyte
    if unit == 'Gi': return int(int(val) * 1073.742) # Gibibyte
    if unit == 'T': return int(int(val) * 1e+6) # Terabyte
    if unit == 'Ti': return int(int(val) * 1.1e+6) # Tebibyte
    if unit == 'P': return int(int(val) * 1e+9) # Petabyte
    if unit == 'Pi': return int(int(val) * 1.126e+9) # Pebibyte
    if unit == 'E': return int(int(val) * 1e+12) # Exabyte
    if unit == 'Ei': return int(int(val) * 1.153e+12) # Exbibyte
    raise Exception('Unrecognized RAM measurement: \'{}\''.format(ram))


def refine_name(name):
    '''Zephyrus2 gives dash symbols in names meaning so a workaround like this is needed.'''
    if '-' not in name: return name
    else: return name.replace('-', '_')


def compute_resources(vm_properties, occupied_cpu, occupied_ram):
    nodes = {}
    for x in vm_properties.keys():
        cpu = cpu_convertion(vm_properties[x]['resources']['cpu']) - cpu_convertion(occupied_cpu)
        ram = ram_convertion(vm_properties[x]['resources']['memory']) - ram_convertion(occupied_ram)
        nodes[x] = {'num': 1, 'resources': {'memory': ram, 'cpu': cpu}} #TODO add "cost"
    return nodes


def update_usage(placement, requirements, resources, kubelet_cpu, kubelet_ram):
    resources_left = compute_resources(resources, kubelet_cpu, kubelet_ram)
    for node in placement:
        for (s,n) in placement[node]:
            cpu = cpu_convertion(requirements[s]['cpu']) * n
            mem = ram_convertion(requirements[s]['memory']) * n
            resources_left[node]['resources']['cpu'] -= cpu
            resources_left[node]['resources']['memory'] -= mem
    for r in resources_left:
        resources_left[r]['resources']['cpu'] = str(resources_left[r]['resources']['cpu'])
        resources_left[r]['resources']['memory'] =  str(resources_left[r]['resources']['memory'] * int(1e+6)) #convert in byte
    return resources_left


def get_topological_sort(bindings):
    graph = {}
    for i in bindings:
        graph.setdefault((i["req_location"], i["req_location_num"], i["req_comp"], i["req_comp_num"]), set()).add(
            ( i["prov_location"],i["prov_location_num"],i["prov_comp"],i["prov_comp_num"]))
    return list(toposort.toposort(graph))



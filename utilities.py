from re import match as re_match
from bidict import bidict


def cpu_convertion(input):
    '''k8s allows for fractional CPUs, in two units: 100m (millicpu/millicores) or 0.1.'''
    try:
        if input.endswith('m'):
            return int(input[:-1])
        else: return int(float(input) * 1000)
    except ValueError:
        raise Exception('Argument not a CPU measurement: \'{}\''.format(input))


def ram_convertion(input):
    '''k8s allows the following RAM suffixes: E, Ei, P, Pi, T, Ti, G, Gi, M, Mi, K or Ki.'''
    try:
        ram, unit = re_match(r'(\d+)(\w+)', input).groups()
    except AttributeError:
        raise Exception('Argument not a RAM measurement: \'{}\''.format(input))
    if unit == 'M': return int(ram) # Megabyte
    if unit == 'Mi': return int(int(ram) * 1.049) # Mebibyte
    if unit == 'K': return int(int(ram) / 1000) # Kilobyte
    if unit == 'Ki': return int(int(ram) / 976.562) # Kibibyte
    if input.isdigit(): return int(int(input) / 1e+6) # Byte
    if unit == 'G': return int(int(ram) * 1000) # Gigabyte
    if unit == 'Gi': return int(int(ram) * 1073.742) # Gibibyte
    if unit == 'T': return int(int(ram) * 1e+6) # Terabyte
    if unit == 'Ti': return int(int(ram) * 1.1e+6) # Tebibyte
    if unit == 'P': return int(int(ram) * 1e+9) # Petabyte
    if unit == 'Pi': return int(int(ram) * 1.126e+9) # Pebibyte
    if unit == 'E': return int(int(ram) * 1e+12) # Exabyte
    if unit == 'Ei': return int(int(ram) * 1.153e+12) # Exbibyte
    raise Exception('Unrecognized RAM measurement: \'{}\''.format(input))

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
    return resources_left






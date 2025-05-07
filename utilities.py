from re import match as re_match
from re import sub
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

def scale_storage(val):
    if isinstance(val, int) and val >= 0:  # Ensure input is a non-negative integer.
        units = ['M', 'Mi', 'K', 'Ki', 'B', 'G', 'Gi', 'T', 'Ti', 'P', 'Pi', 'E', 'Ei']
        conversions = {
            'M': 1, 
            'Mi': 1.049, 
            'K': 1000, 
            'Ki': 976.562, 
            'B': 1e+6, 
            'G': 1000, 
            'Gi': 1073.742, 
            'T': 1e+6, 
            'Ti': 1.1e+6, 
            'P': 1e+9, 
            'Pi': 1.126e+9, 
            'E': 1e+12, 
            'Ei': 1.153e+12
        }
        
        for unit in units:
            scaled_value = val / conversions[unit]
            # Formatting output with one decimal point for clarity
            return f"{int(scaled_value)}{unit}"

    else:
        raise ValueError("Input should be a non-negative integer")


def refine_name(name):
    '''Zephyrus2 gives dash symbols in names meaning so a workaround like this is needed.'''
    if '-' not in name: return name
    else: return name.replace('-', '_')


def convert_resources(vm_properties):
    nodes = {}
    for x in vm_properties.keys():
        cpu = cpu_convertion(vm_properties[x]['resources']['cpu'])
        ram = ram_convertion(vm_properties[x]['resources']['memory'])
        nodes[x] = {'resources': {'memory': ram, 'cpu': cpu}} #TODO add "cost"
    return nodes


def update_usage(placement, requirements, resources):
    resources_left = convert_resources(resources)

    def find_requirement(service_id):
        for prefix in requirements:
            if service_id.startswith(prefix):
                return requirements[prefix]
        raise ValueError(f"No matching requirement found for service ID: {service_id}")

    for node in placement:
        for (service_id, count) in placement[node]:
            req = find_requirement(service_id)
            cpu = cpu_convertion(req['cpu']) * count
            mem = ram_convertion(req['memory']) * count
            resources_left[node]['resources']['cpu'] -= cpu
            resources_left[node]['resources']['memory'] -= mem

    for r in resources_left:
        resources_left[r]['resources']['cpu'] = str(resources_left[r]['resources']['cpu']) + 'm'
        resources_left[r]['resources']['memory'] = scale_storage(resources_left[r]['resources']['memory'])

    return resources_left

def get_topological_sort(bindings):
    graph = {}
    for i in bindings:
        graph.setdefault((i["req-location"], i["req-location-num"], i["req-comp"], i["req-comp-num"]), set()).add(
            ( i["prov-location"],i["prov-location-num"],i["prov-comp"],i["prov-comp-num"]))
    toposorted = list(toposort.toposort(graph))
    res = []
    for level in toposorted:
        for node in level:
            res += [(node[0], node[2])]
    return res






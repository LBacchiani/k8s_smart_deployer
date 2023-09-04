from utilities import *

def build_query(nodes_specification, components, options):
    spec = {'locations': nodes_specification, 'components': {},
            'options': options if options else '', 'specification': ''}
    for component in components:
        pod_name = refine_name(component['metadata']['name'])
        spec['components'][pod_name] = pod_requirements(component)
        if spec['specification']: spec['specification'] += ' and '
        spec['specification'] += '{} > {}'.format(pod_name, component['spec']['replicas'] - 1)
        if 'affinity' in component['spec']['template']['spec']:
            affinities = pod_affinity(component, components)
            if affinities: spec['specification'] += ' and {}'.format(affinities)
    spec['specification'] += '; cost; (sum ?y in components: ?y)'
    return spec

def nodes_specs(vm_properties, reserved_kublet_cpu, reserved_kublet_ram):
    nodes = {}
    for x in vm_properties:
        cpu = cpu_convertion(vm_properties[x]['resources']['cpu']) - reserved_kublet_cpu
        ram = ram_convertion(vm_properties[x]['resources']['RAM']) - reserved_kublet_ram
        nodes[x] = {'num': 1, 'resources': {'RAM': ram, 'cpu': cpu}}  # TODO add "cost"
    return nodes

def pod_requirements(component):
    '''Sums up the resource requirements of containers in a pod.'''
    total_cpu = 0
    total_ram = 0
    for container in component['spec']['template']['spec']['containers']:
        try:
            total_cpu += cpu_convertion(container['resources']['requests']['cpu'])
            total_ram += ram_convertion(container['resources']['requests']['memory'])
        except KeyError as e:
            raise Exception('Resource request for {}\'s {} container lacks {} key.'.format(component['metadata']['name'], container['name'], e))
    return {'resources': {'RAM': total_ram, 'cpu': total_cpu}}

def pod_affinity(component, components):
    affinities = []
    for x in component['spec']['template']['spec']['affinity']:
        for selector in component['spec']['template']['spec']['affinity'][x]['requiredDuringSchedulingIgnoredDuringExecution']:
            for expression in selector['labelSelector']['matchExpressions']:
                matches = matches_lookup(components, expression['values'], expression['key'])
                if expression['operator'] == 'In':
                    affinities += in_operator(component, matches, x)
                else:
                    raise Exception('Operator not supported')
    return ' and '.join(affinities)


def matches_lookup(components, values, key):
    match = []
    for component in components:
        if (key in component['spec']['selector']['matchLabels'].keys() and
                component['spec']['selector']['matchLabels'][key] in values):
            match.append(refine_name(component['metadata']['name']))
    return match

def in_operator(component, matches, kind):
    affinities = []
    pod_nickname = refine_name(component['metadata']['name'])
    if kind == 'podAffinity':
        for match in matches:
            affinities.append('(forall ?x in locations: (?x.{} > 0 impl ?x.{} > 0))'
                              .format(pod_nickname, match))
    elif kind == 'podAntiAffinity':
        if pod_nickname in matches:
            affinities.append('(forall ?x in locations: (?x.{} <= 1))'
                              .format(pod_nickname))
        else:
            for match in matches:
                affinities.append('(forall ?x in locations: (?x.{} > 0 impl ?x.{} = 0))'.format(pod_nickname, match))
    else: raise Exception('Affinity not supported')
    return affinities
def update_usage(configuration, spec):
    locations = spec['locations']
    components = spec['components']
    for node in configuration:
        for component in configuration[node]['0']:
            locations[node]['resources']['RAM'] -= components[component]['resources']['RAM'] * configuration[node]['0'][component]
            locations[node]['resources']['cpu'] -= components[component]['resources']['cpu'] * configuration[node]['0'][component]
    return spec['locations']











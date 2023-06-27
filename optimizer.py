import json
from requests import post as requests_post
from Utilities import *


class Optimizer:
    def __init__(self, kubelet_cpu, kubelet_ram, port, options=None):
        self.reserved_kublet_cpu = kubelet_cpu
        self.reserved_kublet_ram = kubelet_ram
        self.port = port
        self.nicknames = bidict()
        self.options = [x.strip() for x in options.split(',')] if options else None
        self.spec = {}

    def optimize(self, vm_properties, components):
        query_url = 'http://localhost:{}/process'.format(self.port)
        self.build_specification(vm_properties, components)
        configuration = requests_post(query_url, data=json.dumps(self.spec)).json()
        if 'error' not in configuration:
            print(json.dumps(configuration, indent=4))
        else:
            print('Configuration not found')
        return configuration

    def normalize_names(self, configuration):
        for node in configuration['configuration']['locations']:
            configuration['configuration']['locations'][node]["0"] = \
                {get_nickname(self.nicknames, key): value
                 for key, value in configuration['configuration']['locations'][node]["0"].items()}
        return configuration

    def update_usage(self, configuration):
        locations = self.spec['locations']
        components = self.spec['components']
        for node in configuration:
            for component in configuration[node]['0']:
                locations[node]['resources']['RAM'] -= components[component]['resources']['RAM'] * \
                                                       configuration[node]['0'][component]
                locations[node]['resources']['cpu'] -= components[component]['resources']['cpu'] * \
                                                       configuration[node]['0'][component]
        return self.spec['locations']

    def build_specification(self, vm_properties, components):
        self.spec = {'locations': self.node_specs(vm_properties), 'components': {},
                'options': self.options if self.options else '', 'specification': ''}
        for component in components:
            pod_name = set_nickname(self.nicknames, component['metadata']['name'])
            self.spec['components'][pod_name] = self.pod_requirements(component)
            if self.spec['specification']: self.spec['specification'] += ' and '
            self.spec['specification'] += '{} > {}'.format(pod_name, component['spec']['replicas'] - 1)
            if 'affinity' in component['spec']['template']['spec']:
                affinities = self.pod_affinity(component, components)
                if affinities: self.spec['specification'] += ' and {}'.format(affinities)
        self.spec['specification'] += '; cost; (sum ?y in components: ?y)'

    def node_specs(self, vm_properties):
        nodes = {}
        for x in vm_properties:
            cpu = cpu_convertion(vm_properties[x]['resources']['cpu']) - self.reserved_kublet_cpu
            ram = ram_convertion(vm_properties[x]['resources']['RAM']) - self.reserved_kublet_ram
            nodes[x] = {'num': 1, 'resources': {'RAM': ram, 'cpu': cpu}}  # TODO add "cost"
        return nodes

    def pod_requirements(self, component):
        '''Sums up the resource requirements of containers in a pod.'''
        total_cpu = 0
        total_ram = 0
        for container in component['spec']['template']['spec']['containers']:
            try:
                total_cpu += cpu_convertion(container['resources']['requests']['cpu'])
                total_ram += ram_convertion(container['resources']['requests']['memory'])
            except KeyError as e:
                raise Exception('Resource request for {}\'s {} container lacks {} key.'
                                .format(component['metadata']['name'], container['name'], e))
        return {'resources': {'RAM': total_ram, 'cpu': total_cpu}}

    def match_by_app(self, components, values):
        match = []
        for component in components:
            if component['spec']['selector']['matchLabels']['app'] in values:
                match.append(get_nickname(component['metadata']['name']))
        return match

    def in_operator(self, component, matches, kind):
        affinities = []
        pod_nickname = get_nickname(component['metadata']['name'])
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
                    affinities.append('(forall ?x in locations: (?x.{} > 0 impl ?x.{} = 0))'
                                      .format(pod_nickname, match))
        else:
            raise Exception('Affinity not supported')
        return affinities

    def pod_affinity(self, component, components):
        affinities = []
        for x in component['spec']['template']['spec']['affinity']:
            for selector in component['spec']['template']['spec']['affinity'][x]['requiredDuringSchedulingIgnoredDuringExecution']:
                if selector['topologyKey'] == 'kubernetes.io/hostname':
                    for expression in selector['labelSelector']['matchExpressions']:
                        if expression['key'] == 'app':
                            matches = self.match_by_app(components, expression['values'])
                        else:
                            raise Exception('Key not supported')
                        if expression['operator'] == 'In':
                            affinities += self.in_operator(component, matches, x)
                        else:
                            raise Exception('Operator not supported')
                else:
                    raise Exception('Missing topology key: kubernetes.io/hostname')
        return ' and '.join(affinities)

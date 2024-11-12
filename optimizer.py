import json
from requests import post as requests_post

from utilities import *

class Optimizer:
    def __init__(self, kubelet_cpu, kubelet_ram, port, options=None):
        self.reserved_kublet_cpu = kubelet_cpu
        self.reserved_kublet_ram = kubelet_ram
        self.port = port
        self.options = [x.strip() for x in options.split(',')] if options else None

    def pod_requirements(self, component):
        '''Sums up the resource requirements of containers in a pod.'''
        total_cpu = 0
        total_ram = 0
        to_return = {'resources': {}, 'provides': [{}], 'requires': {}}
        for container in component['spec']['template']['spec']['containers']:
            try:
                total_cpu += cpu_convertion(container['resources']['requests']['cpu'])
                total_ram += ram_convertion(container['resources']['requests']['memory'])
            except KeyError as e:
                raise Exception('Resource request for {}\'s {} container lacks {} key.'
                                .format(component['metadata']['name'], container['name'], e))
        to_return['resources'] = {'memory': total_ram, 'cpu': total_cpu}
        if 'ports' in component:
            required = {}
            for port in component['ports']['required']['strong']:
                required[port['name']] = port['value']
            to_return['requires'] = required
        to_return['provides'] = [{'ports': [component['metadata']['name']], 'num': -1}]
        return to_return

    def match_by_app(self, components, values):
        match = []
        for component in components:
            if component['spec']['selector']['matchLabels']['app'] in values:
                match.append(refine_name(component['metadata']['name']))
        return match

    def in_operator(self, component, matches, kind):
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
                            matches = self.match_by_app(components,  expression['values'])
                        else:
                            raise Exception('Key not supported')
                        if expression['operator'] == 'In':
                            affinities += self.in_operator(component, matches, x)
                        else:
                            raise Exception('Operator not supported')
                else:
                    raise Exception('Missing topology key: kubernetes.io/hostname')
        return ' and '.join(affinities)

    def build_specification(self, vm_properties, components):
        spec = {}
        spec['locations'] = compute_resources(vm_properties, self.reserved_kublet_cpu, self.reserved_kublet_ram)
        spec['components'] = {}
        if self.options: spec['options'] = self.options
        spec['specification'] = ''
        for component in components:
            pod_name = refine_name(component['metadata']['name'])
            spec['components'][pod_name] = self.pod_requirements(component)
            if spec['specification']: spec['specification'] += ' and '
            spec['specification'] += '{} > {}'.format(pod_name, component['spec']['replicas'] - 1)
            if 'affinity' in component['spec']['template']['spec']:
                affinities = self.pod_affinity(component, components)
                if affinities: spec['specification'] += ' and {}'.format(affinities)
        spec['specification'] += '; cost; (sum ?y in components: ?y)'
        return spec

    def optimize(self, resources, components):
        query_url = 'http://localhost:{}/process'.format(self.port)
        spec = self.build_specification(resources, components)
        configuration = requests_post(query_url, data=json.dumps(spec)).json()
        if 'error' in configuration:
            print('Configuration not found')
            exit(1)
        for node in configuration['configuration']['locations']:
            configuration['configuration']['locations'][node]["0"] = \
                {refine_name(key): value
                for key, value in configuration['configuration']['locations'][node]["0"].items()}
        return configuration




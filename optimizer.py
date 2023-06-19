from re import match as re_match
from bidict import bidict
import json
from requests import post as requests_post

class Optimizer:
    def __init__(self, kubelet_cpu, kubelet_ram, port, options=None):
        self.reserved_kublet_cpu = kubelet_cpu
        self.reserved_kublet_ram = kubelet_ram
        self.port = port
        self.nicknames = bidict()
        self.options = [x.strip() for x in options.split(',')] if options else None

    ###VIRTUAL MACHINES RESOURCES GATHERING###

    def __cpu_convertion__(self, input):
        '''k8s allows for fractional CPUs, in two units: 100m (millicpu/millicores) or 0.1.'''
        try:
            if input.endswith('m'): return int(input[:-1])
            else: return int(float(input) * 1000)
        except ValueError:
            raise Exception('Argument not a CPU measurement: \'{}\''.format(input))


    def __ram_convertion__(self, input):
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


    def node_specs(self, vm_properties):
        nodes = {}
        for x in vm_properties:
            cpu = self.__cpu_convertion__(vm_properties[x]['resources']['cpu']) - self.reserved_kublet_cpu
            ram = self.__ram_convertion__(vm_properties[x]['resources']['RAM']) - self.reserved_kublet_ram
            nodes[x] = {'num': 1, 'resources': {'RAM': ram, 'cpu': cpu}} #TODO add "cost"
        return nodes


    ###############

    def set_nickname(self, name):
        '''Zephyrus2 gives dash symbols in names meaning so a workaround like this is needed.'''
        if '-' not in name: return name
        else:
            try:
                nickname = name.replace('-', '_')
                self.nicknames[nickname] = name
            except bidict.ValueDuplicationError: raise Exception('Both keys and values must be unique in bidict')
            return nickname


    def get_nickname(self, name):
        if '_' not in name or name not in self.nicknames: return name
        else: return self.nicknames[name]

    def pod_requirements(self, component):
        '''Sums up the resource requirements of containers in a pod.'''
        total_cpu = 0
        total_ram = 0
        for container in component['spec']['template']['spec']['containers']:
            try:
                total_cpu += self.__cpu_convertion__(container['resources']['requests']['cpu'])
                total_ram += self.__ram_convertion__(container['resources']['requests']['memory'])
            except KeyError as e:
                raise Exception('Resource request for {}\'s {} container lacks {} key.'
                                .format(component['metadata']['name'], container['name'], e))
        return {'resources': {'RAM': total_ram, 'cpu': total_cpu}}


    def match_by_app(self, components, values):
        match = []
        for component in components:
            if component['spec']['selector']['matchLabels']['app'] in values:
                match.append(self.get_nickname(component['metadata']['name']))
        return match


    def in_operator(self, component, matches, kind):
        affinities = []
        pod_nickname = self.get_nickname(component['metadata']['name'])
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

    def update_usage(self, locations, components, configuration):
        for node in configuration:
            for component in configuration[node]['0']:
                locations[node]['resources']['RAM'] -= components[component]['resources']['RAM'] * configuration[node]['0'][component]
                locations[node]['resources']['cpu'] -= components[component]['resources']['cpu'] * configuration[node]['0'][component]

    def build_specification(self, vm_properties, components):
        spec = {}
        spec['locations'] = self.node_specs(vm_properties)
        spec['components'] = {}
        if self.options: spec['options'] = self.options
        spec['specification'] = ''
        for component in components:
            pod_name = self.set_nickname(component['metadata']['name'])
            spec['components'][pod_name] = self.pod_requirements(component)
            if spec['specification']: spec['specification'] += ' and '
            spec['specification'] += '{} > {}'.format(pod_name, component['spec']['replicas'] - 1)
            if 'affinity' in component['spec']['template']['spec']:
                affinities = self.pod_affinity(component, components)
                if affinities: spec['specification'] += ' and {}'.format(affinities)
        spec['specification'] += '; cost; (sum ?y in components: ?y)'
        return spec


    def optimize(self, vm_properties, components):
        query_url = 'http://localhost:{}/process'.format(self.port)
        spec = self.build_specification(vm_properties, components)
        print(json.dumps(spec, sort_keys=True, indent=4))
        configuration = requests_post(query_url, data=json.dumps(spec)).json()
        if 'error' not in configuration:
            print(json.dumps(configuration, indent=4))
            self.update_usage(spec['locations'], spec['components'], configuration['configuration']['locations'])
            print(json.dumps(spec['locations'], indent=4))
        else:
            print('Configuration not found')





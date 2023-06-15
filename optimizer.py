from re import match as re_match
from bidict import bidict
import json
from requests import post as requests_post


class Optimizer:
    def __init__(self, kubelet_cpu, kubelet_ram, options=None):
        self.reserved_kublet_cpu = kubelet_cpu
        self.reserved_kublet_ram = kubelet_ram
        self.port = 8082 #TODO THIS SHOULD BE PARAMETRIC
        self.nicknames = bidict()
        self.options = [x.strip() for x in options.split(',')] if options else None

    ###VIRTUAL MACHINES RESOURCES GATHERING###

    def __cpu_convertion__(self, input):
        '''k8s allows for fractional CPUs, in two units: 100m (millicpu/millicores) or 0.1.'''
        try:
            if input.endswith('m'):
                return int(input[:-1])
            else:
                return int(float(input) * 1000)
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
            cpu = self.__cpu_convertion__(vm_properties[x]['resources']['cpu']) -self.reserved_kublet_cpu
            ram = self.__ram_convertion__(vm_properties[x]['resources']['RAM']) - self.reserved_kublet_ram
            nodes[x] = {'num': 1, 'resources': {'RAM': ram, 'cpu': cpu}} #TODO add "cost"
        return nodes


    ###############

    def set_nickname(self, name):
        '''Zephyrus2 gives dash symbols in names meaning so a workaround like this is needed.'''
        if '-' not in name:
            return name
        else:
            try:
                nickname = name.replace('-', '_')
                self.nicknames[nickname] = name
            except bidict.ValueDuplicationError:
                raise Exception('Both keys and values must be unique in bidict')
            return nickname


    def get_nickname(self, name):
        if '_' not in name or name not in self.nicknames:
            return name
        else:
            return self.nicknames[name]

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

    def optimize(self, vm_properties, components):
        query_url = 'http://localhost:{}/process'.format(self.port)
        spec = {}
        spec['locations'] = self.node_specs(vm_properties)
        spec['components'] = {}
        if self.options: spec['options'] = self.options
        spec['specification'] = ''
        for component in components:
            pod_name = component['metadata']['name']
            spec['components'][pod_name] = self.pod_requirements(component)
            if spec['specification']: spec['specification'] += ' and '
            spec['specification'] += '{} > {}'.format(pod_name, component['spec']['replicas'] - 1)
        spec['specification'] += '; cost; (sum ?y in components: ?y)'
        print(json.dumps(spec, sort_keys=True, indent=4))
        result = requests_post(query_url, data=json.dumps(spec)).json()
        print(result)





from re import match as re_match
from bidict import bidict


def cpu_convertion(input):
    '''k8s allows for fractional CPUs, in two units: 100m (millicpu/millicores) or 0.1.'''
    try:
        if input.endswith('m'): return int(input[:-1])
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



def set_nickname(nicknames, name):
    '''Zephyrus2 gives dash symbols in names meaning so a workaround like this is needed.'''
    if '-' not in name: return name
    else:
        try:
            nickname = name.replace('-', '_')
            nicknames[nickname] = name
        except bidict.ValueDuplicationError: raise Exception('Both keys and values must be unique in bidict')
        return nickname


def get_nickname(nicknames, name):
    if '_' not in name or name not in nicknames: return name
    else: return nicknames[name]
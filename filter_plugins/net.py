import sys
import os

try:
    slug
except NameError:
    # slug has not yet been loaded. So we load it.
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from misc import slug
    del sys.path[0]

def net_slug(net_config, inventory_hostname, capital=False):
    name = 'Unnamed'
    if net_config['type'] == 'vpn':
        hosts = []
        if inventory_hostname is None:
            hosts = [net_config['server'], net_config['client']]
        else:
            hosts = [net_config[net_host_key(net_config, 'remote', inventory_hostname)]]
        name = '-'.join([host.split('.', 1)[0] for host in hosts])
    else:
        raise RuntimeError('Unsupported type \'%s\' for net config in net_slug' % (net_config['type']))
    return slug(name, capital=capital)

def net_dev_name(net_config, inventory_hostname):
    if net_config['type'] == 'vpn':
        name = 'tun' + net_slug(net_config, inventory_hostname, capital=True)
    elif net_config['type'] == 'shim':
        name = net_config['interface']
    elif net_config['type'] == 'local-subnet':
        name = net_config['interface']
    else:
        raise RuntimeError('Unsupported type \'%s\' for net config in net_dev_name' % (net_config['type']))
    return name

def host_net_keys(hostname, net_configs, type=None, exclude=[]):
    for key, net_config in sorted(net_configs.iteritems()):
        if type is None or type == net_config['type']:
            on_host = False
            if net_config['type'] == 'shim':
                on_host = True
            elif net_config['type'] == 'vpn':
                on_host = (hostname in [
                        net_config['server'],
                        net_config['client']
                        ])
            elif net_config['type'] == 'local-subnet':
                on_host = net_config.get('local_ip', False)
            else:
                raise RuntimeError('Unsupported type \'%s\' for net config in host_net_keys' % (net_config['type']))
            if on_host and key not in exclude:
                yield key

def host_nets(hostname, net_configs, type=None):
    for key in host_net_keys(hostname, net_configs, type):
        yield net_configs[key]

# good
def net_served_by(net_config, inventory_hostname):
    served = False
    if net_config['type'] == 'vpn':
        served = (inventory_hostname == net_config['server'])
    else:
        raise RuntimeError('Unsupported type \'%s\' for net_config in net_served_by' % (net_config['type']))
    return served


# good
def net_host_key(net_config, kind, inventory_hostname=None):
    if net_config['type'] == 'vpn':
        if kind == 'local':
            kind = 'server' if net_served_by(net_config, inventory_hostname) else 'client'
        elif kind == 'remote':
            kind = 'client' if net_served_by(net_config, inventory_hostname) else 'server'
        # No `else` to allow passing kinds that do not need resolving (E.g.: 'server')
    else:
        raise RuntimeError('Unsupported type \'%s\' for net config in net_host_key' % (net_config['type']))

    return kind

def net_ip(net_config, kind, inventory_hostname=None):
    if net_config['type'] == 'vpn':
        kind = net_host_key(net_config, kind, inventory_hostname)

        if kind == 'server':
            offset = 1
        elif kind == 'client':
            offset = 2
        else:
            raise RuntimeError('Unsupported kind \'%s\' for net_ip' % (kind))
        ip_split = net_config['ipv4_net'].split('/', 1)[0].split('.')
        ip_split[3] = str(int(ip_split[3]) + offset)
        ip = '.'.join(ip_split)
    elif net_config['type'] == 'shim':
        if kind == 'local':
            ip = net_config['local_ip']
        else:
            raise RuntimeError('Unsupported kind \'%s\' for net config in net_ip / shim' % (kind))
    elif net_config['type'] == 'local-subnet':
        ip = net_config['local_ip']
    else:
        raise RuntimeError('Unsupported type \'%s\' for net config in net_ip' % (net_config['type']))

    return ip

def build_net_access(net_access, net_configs):
    ret = net_access
    if not isinstance(net_access, dict):
        ret = {
            'net_key': net_access
            }
    if 'hosts' not in ret:
        ret['hosts'] = ['all']
    return ret

def net_accesses_to_local_ips(net_accesses, net_configs, inventory_hostname):
    ret = []
    for net_access in net_accesses:
        net_access = build_net_access(net_access, net_configs)
        net_config = net_configs[net_access['net_key']]
        ip = net_ip(net_config, 'local', inventory_hostname)
        ret += [ip]
    return ret

def cidrToNetmask(cidr):
    ret = ''
    val = 2**32 - 2**(32-cidr)
    for i in range(3,-1,-1):
        ret += str((val >> (i*8)) & 255) + '.'
    return ret[:-1]

def rangeCidrToNetmask(range):
    split = range.split('/',1)
    return [split[0], cidrToNetmask(int(split[1]))]

def net_access_to_remote_ranges(net_access, net_configs, inventory_hostname, hostvars, notation='CIDR'):
    net_access = build_net_access(net_access, net_configs)
    net_config = net_configs[net_access['net_key']]

    if net_access.get('hosts', ['all']) != ['all']:
        ranges = net_access['hosts']
    else:
        if net_config['type'] == 'vpn':
            ranges = [net_ip(net_config, 'remote', inventory_hostname) + '/32']
        elif net_config['type'] == 'shim':
            if net_config['public']:
                ranges = net_access['hosts']
            else:
                ranges = net_config['remote_ranges']
        elif net_config['type'] == 'local-subnet':
            ranges = net_config['remote_ranges']
        else:
            raise RuntimeError('Unsupported type \'%s\' for net config in net_ranges' % (net_config['type']))

    # Resolve names in ranges
    unresolved_ranges = ranges
    ranges=[]
    for item in unresolved_ranges:
        if item == 'all':
            ranges += net_config['remote_ranges']
        else:
            if item in hostvars.keys():
                if 'public_ipv4_address' in hostvars[item]:
                    ranges += [hostvars[item]['public_ipv4_address']]
                else:
                    ranges += hostvars[item]['public_ipv4_address_ranges']
            else:
                ranges += [item]

    if notation == 'CIDR':
        pass # default notation
    elif notation == 'netmask':
        ranges = [ rangeCidrToNetmask(range) for range in ranges ]
    else:
        raise RuntimeError('Unsupported notation \'%s\' in net_access_to_remote_ranges' % (notation))

    return ranges

def net_accesses_to_remote_ranges(net_accesses, net_configs, inventory_hostname, hostvars, notation='CIDR'):
    ret = []
    for net_access in net_accesses:
        ret += net_access_to_remote_ranges(net_access, net_configs, inventory_hostname, hostvars, notation=notation)
    return ret

def net_access_to_incoming_rules(net_access, net_configs, inventory_hostname, hostvars):
    net_access = build_net_access(net_access, net_configs)
    net_config = net_configs[net_access['net_key']]
    interface = net_dev_name(net_config, inventory_hostname)

    rules = []

    sources = net_access_to_remote_ranges(net_access, net_configs, inventory_hostname, hostvars)

    for source in sources:
        rules += [{
                "source": source,
                "i": interface
                }]

    return rules


class FilterModule(object):
    '''Network jinja2 filters'''

    def filters(self):
        return {
            'host_nets': host_nets,
            'host_net_keys': host_net_keys,
            'net_dev_name': net_dev_name,
            'net_slug': net_slug,
            'net_served_by': net_served_by,
            'net_host_key': net_host_key,
            'net_ip': net_ip,
            'net_accesses_to_local_ips': net_accesses_to_local_ips,
            'net_accesses_to_remote_ranges': net_accesses_to_remote_ranges,
            'net_access_to_incoming_rules': net_access_to_incoming_rules,
        }

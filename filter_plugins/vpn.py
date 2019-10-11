def vpn_name(vpn_config, inventory_hostname):
    if inventory_hostname is None:
        ret = vpn_config['server'].split('.', 1)[0] + '-' + vpn_config['client'].split('.', 1)[0]
    else:
        if vpn_served_by(vpn_config, inventory_hostname):
            host = vpn_config['client']
        else:
            host = vpn_config['server']
        ret = host.split('.', 1)[0]
    return ret


def vpn_dev_name(vpn_config, inventory_hostname):
    return vpn_name(vpn_config, inventory_hostname).capitalize()


def host_vpns(hostname, vpn_configs):
    for key, vpn_config in sorted(vpn_configs.iteritems()):
        if hostname in [vpn_config['server'], vpn_config['client']]:
            yield vpn_config


def vpn_served_by(vpn_config, inventory_hostname):
    return inventory_hostname == vpn_config['server']


def vpn_ip(vpn_config, kind, inventory_hostname=None):
    if kind == 'local':
        kind = 'server' if vpn_served_by(vpn_config, inventory_hostname) else 'client'
    elif kind == 'remote':
        kind = 'client' if vpn_served_by(vpn_config, inventory_hostname) else 'server'
    # No else

    if kind == 'server':
        offset = 1
    elif kind == 'client':
        offset = 2
    else:
        raise RuntimeError('Unsupported kind \'%s\' for vpn_ip' % (kind))
    ip = vpn_config['ipv4_net'].split('/', 1)[0].split('.')
    ip[3] = str(int(ip[3]) + offset)
    return '.'.join(ip)


class FilterModule(object):
    '''Vpn jinja2 filters'''

    def filters(self):
        return {
            'host_vpns': host_vpns,
            'vpn_dev_name': vpn_dev_name,
            'vpn_name': vpn_name,
            'vpn_served_by': vpn_served_by,
            'vpn_ip': vpn_ip,
        }

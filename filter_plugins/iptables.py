def iptables_init_chain(name):
    return '\n'.join([
        ':%s DROP [0:0]' % (name),
        '-A %s -j LOG --log-prefix "DROP %s\: " ' % (name, name),
        '-A %s -j DROP' % (name),
        ])

class FilterModule(object):
    '''iptables jinja2 filters'''

    def filters(self):
        return {
            'iptables_init_chain': iptables_init_chain,
        }

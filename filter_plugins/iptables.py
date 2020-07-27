def iptables_init_chain(name):
    return '\n'.join([
        ':%s DROP [0:0]' % (name),
        iptables_rule(name, 'LOG', log_prefix=('"DROP %s\: "' % (name))),
        iptables_rule(name, 'DROP'),
        ])

def dict_remove(key, dictionary):
    if key in dictionary:
        value = dictionary[key]
        del dictionary[key]
    else:
        value = None
    return value, dictionary

def iptables_rule(chain, target, how='append', **kwargs):
    ret = '-' + ('I' if how == 'insert' else 'A') + ' ' + chain
    log_prefix, kwargs = dict_remove('log_prefix', kwargs)
    for key in [
        '-m',
        '-i',
        '-p',
        '--source',
        '--dport',
        '--state',
        '--icmp-type',
        ]:
        dict_key = key.lstrip('-')
        value, kwargs = dict_remove(dict_key, kwargs)
        if not value:
            dict_key = dict_key.replace('-', '_')
            value, kwargs = dict_remove(dict_key, kwargs)
        if value:
            if key == "--icmp-type":
                ret += ' -p icmp'
            ret += ' ' + key + ' ' + str(value)

    ret += ' -j ' + target
    if log_prefix:
        if target == 'LOG':
            ret += ' --log-prefix ' + log_prefix
        else:
            raise RuntimeError('Received "log-prefix" "%s" with target "%s" instead of "LOG"' % (log_prefix, target))
    if kwargs:
        raise RuntimeError('Unparsed kwargs: ' + str(kwargs))

    return ret


def iptables_insert_rule(chain, target, **kwargs):
    return iptables_rule(chain, target, how='insert', **kwargs)


def iptables_append_rule(chain, target, **kwargs):
    return iptables_rule(chain, target, how='append', **kwargs)


class FilterModule(object):
    '''iptables jinja2 filters'''

    def filters(self):
        return {
            'iptables_init_chain': iptables_init_chain,
            'iptables_insert_rule': iptables_insert_rule,
            'iptables_append_rule': iptables_append_rule,
        }

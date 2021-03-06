import collections
import re
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from misc import is_undefined
del sys.path[0]

def inject_user(check, role_config):
    if role_config['user'] != 'omit':
        check['user'] = role_config['user']
    return check


def role_to_name(role_config):
    ret = role_config['role'][0].upper() + role_config['role'][1:]
    ret = re.sub(r'[^a-zA-Z0-9]', r' ', ret)
    return ret


def append_common_role_tasks_config(monitoring_check_config, role_config):
        if not isinstance(monitoring_check_config, list):
            if is_undefined(monitoring_check_config):
                monitoring_check_config = []
            else:
                raise RuntimeError('monitoring_check_config has to be a list, but is "%s"' % type(monitoring_check_config))

        checks = role_config['monitoring_checks']
        # expand `services`
        checks = [check for item in checks for check in (role_config['services'] if item == 'services' else [item])]

        role_name_formatted = role_to_name(role_config)
        check_number = 0
        for check in checks:
            check_number += 1
            if isinstance(check, str) or isinstance(check, unicode):
                check = {
                        'name': check,
                        'command': check,
                        }
            check.setdefault('name', role_name_formatted + ((' ' + str(check_number)) if len(checks) > 1 else ''))
            if check.get('name_prefix', True):
                if len(checks) == 1 and (check['name'] == role_config['role'] or check['name'] == role_name_formatted):
                    check['name'] = role_name_formatted
                else:
                    check['name'] = role_name_formatted + '/' + check['name']
            if check.setdefault('type', 'process') == 'process':
                if 'user' not in check:
                    check = inject_user(check, role_config)
            monitoring_check_config.append(check)
        return monitoring_check_config

def explicitize(checks):
    ret = []
    for check in checks:
        if isinstance(check, str) or isinstance(check, unicode):
            check = {
                'name': check,
                'command': check,
                }
        check.setdefault('type', 'process')

        if check['type'] == 'file_age':
            check.setdefault('path', check['name'])
            check.setdefault('warn', 300)
            check.setdefault('critical', 300)

        if check['type'] == 'process':
            check.setdefault('min-procs', 1)
            check.setdefault('max-procs', 1)
            check.setdefault('user', 'root')

        if check['type'] == 'port':
            check.setdefault('protocol', 'tcp')
            check.setdefault('service', None)

        if check['type'] == 'website':
            check.setdefault('dns', False)

        if check['type'] == 'disk':
            check.setdefault('bytes_left_warn', '20%')
            check.setdefault('bytes_left_critical', '10%')
            check.setdefault('inodes_left_warn', '20%')
            check.setdefault('inodes_left_critical', '10%')

        if check['type'] == 'load':
            check.setdefault('load1_warn', 2)
            check.setdefault('load1_critical', 4)
            check.setdefault('load5_warn', 1.1)
            check.setdefault('load5_critical', 1.5)
            check.setdefault('load15_warn', 0.8)
            check.setdefault('load15_critical', 0.9)

        if not check.get('skip', False):
            ret.append(check)
    return ret


class FilterModule(object):
    '''Jinja2 filters for common-role-tasks'''

    def filters(self):
        return {
            'monitoring_checks_append_common_role_tasks_config': append_common_role_tasks_config,
            'monitoring_checks_explicitize': explicitize,
        }

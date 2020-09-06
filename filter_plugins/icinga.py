import copy
import collections
import re


def update_dict(target, source):
    for key, value in source.iteritems():
        if isinstance(value, collections.Mapping):
            repl = update_dict(target.get(key, {}), value)
            target[key] = repl
        else:
            target[key] = source[key]
    return target


def map_distribution_to_image(distribution):
    distribution = distribution.lower()
    ret = 'unknown.gif'
    if distribution == 'debian':
        ret = 'base/debian.gif'
    elif distribution == 'gentoo':
        ret = 'vendors/gentoo.gif'
    elif distribution == 'hp':
        ret = 'vendors/hp-ux2.gif'
    elif distribution == 'openwrt':
        ret = 'vendors/linux40.gif'
    elif distribution == 'linux':
        ret = 'vendors/linux40.gif'
    return ret


def icinga_check(description, host, check, args=[], interval=None,
                 contact_groups=None, max_check_attempts=None,
                 flap_detection=None):
    non_default_setting_lines = ""

    # Set how often to run the check
    if interval is None:
        interval_length = None
    elif interval == 'hourly':
        interval_length = 60
    elif interval == 'daily':
        interval_length = 24*60
    else:
        try:
            interval_length = int(interval)
            interval = str(interval) + " (default: minutes)"
        except ValueError:
            raise RuntimeError(
                'Invalid value \'%s\' for interval given' % (interval))
    if interval_length:
        non_default_setting_lines += "\n  check_interval      %s  # (%s)" % (
            interval_length, interval)

    # Set which contact group to contact in case of issues
    if contact_groups is None:
        pass
    elif contact_groups == 'critical':
        non_default_setting_lines += "\n  contact_groups      %s" \
            % (contact_groups)
    else:
        raise RuntimeError('Invalid value \'%s\' for contact_groups given'
                           % (contact_groups))

    # Set how often to attempt checking
    if max_check_attempts is None:
        pass
    else:
        non_default_setting_lines += "\n  max_check_attempts  %d" \
            % (max_check_attempts)

    # Override flap detection if requested
    if flap_detection is not None:
        flap_detection = 1 if flap_detection else 0
        non_default_setting_lines += "\n  flap_detection_enabled %d" \
            % (flap_detection)

    command = "!".join(["check_%s" % (check)] + [unicode(arg) for arg in args])

    return """
define service {
  use                 generic-service
  host_name           %s
  service_description %s%s
  check_command       %s
}
""" % (host, description, non_default_setting_lines, command)


def icinga_nrpe_check(description, host, check, timeout=10, interval=None,
                      contact_groups=None, max_check_attempts=None,
                      flap_detection=None):
    return icinga_check(description, host, "nrpe_timeout",
                        [timeout, "nrpe_check_%s" % (check)],
                        interval=interval,
                        contact_groups=contact_groups,
                        max_check_attempts=max_check_attempts,
                        flap_detection=flap_detection)


def icinga_nrpe_raw_command(name, command):
    return "check_command[nrpe_check_%s]=%s" % (name, command)


def icinga_nrpe_command(name, command, arg="", raw=False):
    check_template = '/usr/lib/nagios/plugins/check_%s %s'
    return icinga_nrpe_raw_command(name,
                                   check_template % (command, arg))


def icinga_http_check(description, host, domain, expected_status_code=200,
                      uri='/', ssl=True, method='GET', data=None,
                      encode_data=False, expected_content='', dns=False,
                      port=None, max_seconds=''):
    name = 'http_vhost_' + (method.lower())
    if dns:
        name += '_dns'
    if ssl:
        name += '_ssl'
        if ssl is not True:
            name += ssl
    arguments = [domain, uri, expected_content]
    if data:
        name += '_data'
        if encode_data:
            if isinstance(data, str):
                data = urllib.quote_plus(data)
            else:
                data = urllib.urlencode(data)
        arguments += [data]
    name += '_' + str(expected_status_code)
    if port:
        name += '_port'
        arguments += [port]
    if not max_seconds:
        max_seconds = 2
    name += '_' + str(max_seconds) + 's'
    return icinga_check(description, host, name,
                        arguments)


def icinga_http_preconfigured_checks_get_config_unsplit_unresolved(key, configs):
    config = configs.get(key, {})

    if 'alias' in config:
        alias = config['alias']
        alias_config = icinga_http_preconfigured_checks_get_config_unsplit_unresolved(
            alias, configs)

        config = copy.deepcopy(config)
        update_dict(config, alias_config)
        del config['alias']

    return config



def icinga_http_preconfigured_checks_get_config_unsplit(web_host, configs):
    ret = {}
    for key in [
        web_host.split('.')[0],
        web_host,
        ]:
        config = icinga_http_preconfigured_checks_get_config_unsplit_unresolved(key, configs)

        ret = copy.deepcopy(ret)
        update_dict(ret, config)

    if not ret:
        ret = {"main": {}}

    return ret


def icinga_http_preconfigured_checks_get_config(web_host, configs):
    unsplit_config = icinga_http_preconfigured_checks_get_config_unsplit(
        web_host, configs)

    config_defaults = {
        'alias': None,
        'protocols': ['http', 'https'],
        'max_https_reqs_per_second': 10,
        'max_http_reqs_per_second': 0.1,
        'ssl': None,
        }

    config = {}
    for key in config_defaults.keys():
        config[key] = unsplit_config.get(key, config_defaults[key])

    checks = {}
    for key in unsplit_config.keys():
        if key not in config:
            checks[key] = unsplit_config.get(key, {})

    return config, checks


def icinga_http_preconfigured_checks_check(host, site, name, config={},
                                           use_suffix=False, dns=False,
                                           default_protocol='https', ssl=None):
    protocol = config.get('protocol', default_protocol)

    description = site + '/%s' % (protocol)
    if use_suffix:
        description += '/' + name

    max_seconds = config.get('max_seconds', '')
    method = config.get('method', 'GET')
    uri = config.get('uri', '/')
    ssl = (protocol != 'http') if ssl is None else str(ssl)
    port = config.get('port', None)
    data = config.get('data', None)
    encode_data = config.get('encode_data', False)
    expected_status_code = config.get('expected_status_code', 200)
    expected_content = config.get('expected_content', '')

    return icinga_http_check(
        description=description, host=host,
        domain=site, method=method, uri=uri, ssl=ssl,
        data=data, encode_data=encode_data,
        expected_status_code=expected_status_code,
        expected_content=expected_content,
        dns=dns, port=port, max_seconds=max_seconds)


def icinga_http_preconfigured_domain(host, kind, site, configs={},
                                     dns=False):
    ret = ''
    config, checks = icinga_http_preconfigured_checks_get_config(
        site, configs)

    protocols = config['protocols']
    ssl = config.get('ssl', None)

    default_protocol = 'https' if 'https' in protocols else 'http'
    use_suffix = (len(checks) > 1)
    for check_name, check_config in sorted(checks.iteritems()):
        ret += icinga_http_preconfigured_checks_check(
            host=host, site=site, name=check_name,
            config=check_config, use_suffix=use_suffix, dns=dns,
            default_protocol=default_protocol, ssl=ssl)

    if 'https' in protocols:
        description = site + '/cert'
        check = 'http_vhost_cert'
        if dns:
            check += '_dns'
        check += '_ssl'
        if ssl is not None:
            check += str(ssl)
        ret += '\n' + icinga_check(description=description, host=host,
                                   check=check, args=[site],
                                   interval='daily')

    if 'http' in protocols and 'https' in protocols:
        description = site + '/http/https redirect'
        description = ('%s/http/https redirect') % (site)
        ret += '\n' + icinga_http_check(description=description,
                                        host=host,
                                        domain=site,
                                        expected_status_code=301,
                                        ssl=False,
                                        dns=dns)

    # TODO: add checks for 5xx requests and total.count
    return ret


def icinga_http_preconfigured_checks(host, apache_sites=[], nginx_sites=[],
                                     unansiblized_sites=[], configs={},
                                     dns=False):
    ret = ''
    for kind, sites in sorted({
            'apache': apache_sites,
            'nginx': nginx_sites,
            None: unansiblized_sites,
            }.iteritems()):
        for site in sorted(sites):
            ret += icinga_http_preconfigured_domain(host, kind, site,
                                                    configs=configs,
                                                    dns=dns)
    return ret

def icinga_slug(string):
    return re.sub(r'[^a-zA-Z0-9]', r'_', string.lower())

def icinga_monitoring_check_config_nrpe_formatter(config):
    ret = ''
    slug=icinga_slug(config['name'])
    if config['type'] == 'disk':
        arg = '-w %s'  % (str(config['bytes_left_warn']))
        arg += ' -c %s'  % (str(config['bytes_left_critical']))
        arg += ' -W %s'  % (str(config['inodes_left_warn']))
        arg += ' -K %s'  % (str(config['inodes_left_critical']))
        arg += ' -e --exclude-type=tracefs'
        ret = icinga_nrpe_command(slug, 'disk', arg.strip())
    elif config['type'] == 'file_age':
        arg='-w %s -c %s %s' % (str(config['warn']), str(config['critical']), str(config['path']))
        ret = icinga_nrpe_command(slug, 'file_age', arg.strip())
    elif config['type'] == 'process':
        arg=''
        if 'command' in config:
            arg=' --command=%s' % (config['command'])
        if (str(config['min-procs']) + str(config['min-procs'])) != '':
            arg+=' --critical %s:%s' % (config['min-procs'], config['max-procs'])
        arg+=' --ppid=1'
        if config['user'] != 'omit':
            arg+=' --user=%s' % (config['user'])
        if 'argument' in config:
            arg+=' --argument-array=%s' % (config['argument'])
        ret = icinga_nrpe_command(slug, 'procs', arg.strip())
    elif config['type'] == 'website':
        ret = '# No nrpe counter-part for check ' + config['name']
    else:
        raise RuntimeError('Unknown check type "%s" in icinga_monitoring_check_config_nrpe_formatter' % (config['type']))
    return ret


def icinga_monitoring_check_config_check_formatter(config, inventory_hostname, website_configs):
    ret = ''
    slug=icinga_slug(config['name'])
    if config['type'] == 'disk':
        ret = icinga_nrpe_check(config['name'], inventory_hostname, slug)
    elif config['type'] == 'file_age':
        ret = icinga_nrpe_check(config['name'], inventory_hostname, slug)
    elif config['type'] == 'process':
        ret = icinga_nrpe_check(config['name'], inventory_hostname, slug)
    elif config['type'] == 'website':
        ret = icinga_http_preconfigured_domain(inventory_hostname, config['kind'], config['domain'], configs=website_configs, dns=config['dns'])
    else:
        raise RuntimeError('Unknown check type "%s" in icinga_monitoring_check_config_check_formatter' % (config['type']))
    return ret


class FilterModule(object):
    '''Filters for icinga'''

    def filters(self):
        return {
            'map_distribution_to_image': map_distribution_to_image,
            'icinga_check': icinga_check,
            'icinga_nrpe_check': icinga_nrpe_check,
            'icinga_nrpe_command': icinga_nrpe_command,
            'icinga_nrpe_raw_command': icinga_nrpe_raw_command,
            'icinga_http_check': icinga_http_check,
            'icinga_http_preconfigured_checks':
                icinga_http_preconfigured_checks,
            'icinga_monitoring_check_config_nrpe_formatter':
                icinga_monitoring_check_config_nrpe_formatter,
            'icinga_monitoring_check_config_check_formatter':
                icinga_monitoring_check_config_check_formatter,
        }

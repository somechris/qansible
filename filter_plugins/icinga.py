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


class FilterModule(object):
    '''Filters for icinga'''

    def filters(self):
        return {
            'map_distribution_to_image': map_distribution_to_image,
            'icinga_check': icinga_check,
            'icinga_nrpe_check': icinga_nrpe_check,
            'icinga_nrpe_command': icinga_nrpe_command,
            'icinga_nrpe_raw_command': icinga_nrpe_raw_command,
        }

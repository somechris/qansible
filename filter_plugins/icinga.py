def map_os_to_image(os):
    os = os.lower()
    ret = 'unknown.gif'
    if os == 'debian':
        ret = 'base/debian.gif'
    elif os == 'gentoo':
        ret = 'vendors/gentoo.gif'
    elif os == 'hp':
        ret = 'vendors/hp-ux2.gif'
    elif os == 'openwrt':
        ret = 'vendors/linux40.gif'
    elif os == 'linux':
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


class FilterModule(object):
    '''Filters for icinga'''

    def filters(self):
        return {
            'map_os_to_image': map_os_to_image,
            'icinga_check': icinga_check,
        }

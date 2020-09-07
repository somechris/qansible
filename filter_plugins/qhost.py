def icinga_format_notes_urls(hostvars):
    ret = ''

    key = 'dashboards'
    system_links = hostvars['qhost_system_links']
    if key in system_links:
        for link in system_links[key][:4]:
            url = link['url'].format(hostname=hostvars['inventory_hostname'], hostname_short=hostvars['inventory_hostname_short'])
            ret += " \'%s\'" % (url)

    return ret


def qhost_format_system_link_url(link, hostvars):
    hostname = hostvars['inventory_hostname']
    hostname_short = hostvars['inventory_hostname_short']
    url = link['url'].format(hostname=hostname, hostname_short=hostname_short)
    return url


class FilterModule(object):
    '''Filters for qhost'''

    def filters(self):
        return {
            'qhost_format_system_link_url': qhost_format_system_link_url,
        }

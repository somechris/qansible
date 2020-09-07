# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dashboard_metrics import add_metric
from dashboard_metrics import add_series_override
from dashboard_metrics import set_colors
from dashboard_metrics import set_yaxis_units
from dashboard_metrics import set_yaxis_maximum
from dashboard_metrics import set_fill
from dashboard_metrics import set_decimals
from dashboard_metrics import set_threshold
from dashboard_markdown import new as new_markdown
from dashboard_markdown import set_content
from dashboard_row import new as new_row
from dashboard_row import add_panel
from qhost import qhost_format_system_link_url
del sys.path[0]

def panel_host_metadata_text(host, hostvars, width=None):
    title = ''
    panel = new_markdown(title, width=width)

    content = '#### ' + hostvars['inventory_hostname'] + '\n'
    content += hostvars['qhost_description'] + '\n'

    set_content(panel, content)

    return panel

def panel_host_metadata_links(host, hostvars, width=None):
    title = 'Links to other Systems'
    panel = new_markdown(title, width=width)

    content = ''

    systems = []
    system_links = []
    link_keys = hostvars['qhost_system_links'].keys()
    link_keys.sort()
    for link_key in link_keys:
        links = []
        for link in hostvars['qhost_system_links'][link_key]:
            title = link['system']
            url = qhost_format_system_link_url(link, hostvars)
            links.append('[%s](%s)' % (title, url))

        if len(links):
            systems.append(link_key[0].upper() + link_key[1:])
            system_links.append(', '.join(links))
    if len(systems):
        content = '|' + ('|'.join(systems)) + '|\n'
        content += '|' + ('|'.join(['---'] * len(systems))) + '|\n'
        content += '|' + ('|'.join(system_links)) + '|\n'

    set_content(panel, content)

    return panel


def row_host_metadata(host, hostvars):
    title = 'Metadata'
    row = new_row(title)

    add_panel(row, panel_host_metadata_text(host, hostvars, width=3))
    add_panel(row, panel_host_metadata_links(host, hostvars, width=9))

    return row


class FilterModule(object):
    '''Ansible jinja2 filters for network graphs in dashboards'''

    def filters(self):
        return {
            }

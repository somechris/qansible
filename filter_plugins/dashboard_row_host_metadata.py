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
del sys.path[0]


def panel_host_metadata(host, hostvars, width=None):
    title = "Metadata"
    panel = new_markdown(title, width=width)

    lines = []

    def add_line(line):
        lines.append(line)

    def add_separator():
        add_line('')

    def add_kv(key, value):
        add_line('| %s | %s |' % (key, value))

    def add_kvk(key, value_key):
        add_kv(key, hostvars[value_key])

    def format_plain_link(name, src):
        return '[%s](%s)' % (name, src)

    def add_link(name, src):
        add_separator()
        add_line(format_plain_link(name, src))

    add_line('# %s' % (hostvars['inventory_hostname']))

    add_separator()  # --------------------------

    add_kv('Key', 'Value')
    add_kv('---', '---')
    add_kvk('Name', 'inventory_hostname')
    add_kvk('Description', 'qhost_description')

    link_keys = hostvars['host_links'].keys()
    link_keys.sort()
    for link_key in link_keys:
        links = []
        for link in hostvars['host_links'][link_key]:
            title = link['system']
            url = link['url'].format(hostname=hostvars['inventory_hostname'], hostname_short=hostvars['inventory_hostname_short'])
            links.append(format_plain_link(title, url))
        if len(links):
            add_kv(link_key[0].upper() + link_key[1:], ', '.join(links))

    add_separator()  # --------------------------

    set_content(panel, "\n".join(lines))

    return panel


def row_host_metadata(host, hostvars):
    title = 'Metadata'
    row = new_row(title)
    width=12

    add_panel(row, panel_host_metadata(host, hostvars, width=width))

    return row


class FilterModule(object):
    '''Ansible jinja2 filters for network graphs in dashboards'''

    def filters(self):
        return {
            }

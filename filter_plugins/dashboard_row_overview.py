# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dashboard_row_cpu import panel_cpu
from dashboard_row_load import panel_load
from dashboard_row_memory import panel_memory
from dashboard_row_network import panel_network_bytes
from dashboard_row import new as new_row
from dashboard_row import add_panel
del sys.path[0]


def row_overview(host, cpu_count=False, collapsed=None, repeat=None):
    title = 'Performance Characteristics'
    row = new_row(title, collapsed=collapsed, repeat=repeat)
    width = 3

    add_panel(row, panel_load(host, width=width, cpu_count=cpu_count))
    add_panel(row, panel_cpu(host, width=width))
    add_panel(row, panel_memory(host, width=width))
    add_panel(row, panel_network_bytes(host, width=width, title='Network'))

    return row


class FilterModule(object):
    '''Ansible jinja2 filters for overview panels in dashboards'''

    def filters(self):
        return {
            'dashboard_row_overview': row_overview,
            }

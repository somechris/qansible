# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dashboard_row_cpu import row_cpu
from dashboard_row_disk import row_disk
from dashboard_row_graphite import row_graphite
from dashboard_row_host_metadata import row_host_metadata
from dashboard_row_load import row_load
from dashboard_row_memory import row_memory
from dashboard_row_network import row_network
from dashboard_row_overview import row_overview
from dashboard_row_processes import row_processes
from dashboard_graph import new as new_graph
from dashboard_metrics import add_metric
from dashboard_metrics import set_decimals
from dashboard_metrics import set_yaxis_units
from dashboard_metrics import zero_missing_points
from dashboard_row import new as new_row
from dashboard_row import add_panel
from dashboard_row import set_repeat
from dashboard_text import new as new_text
from dashboard_text import set_content
from dashboard import new as new_dashboard
from dashboard import add_tag
from dashboard import add_tags
from dashboard import add_row
from dashboard import add_template
from dashboard import set_basename
del sys.path[0]


def add_rows(dashboard, host, groups, hostvars, cpu_count):
    add_row(dashboard, row_host_metadata(host, hostvars))
    if 'unmanaged' not in groups:
        add_row(dashboard, row_overview(host, cpu_count=cpu_count, collapsed=False))
        add_row(dashboard, row_load(host, cpu_count=cpu_count))
        add_row(dashboard, row_cpu(host))
        add_row(dashboard, row_processes(host))
        add_row(dashboard, row_disk(host))
        add_row(dashboard, row_memory(host))
        add_row(dashboard, row_network(host))


def dashboard_host(host, groups=[], hostvars={}, cpu_count=False):
    dashboard = new_dashboard(host)
    set_basename(dashboard, 'host-dashboard-' + host)
    add_tags(dashboard, ['host', host])
    for group in groups:
        if group.startswith('website_') and group.endswith('_server_apache'):
            group = None
        elif group.startswith('website_') and group.endswith('_server'):
            group = '.'.join(group.split('_')[1:-1])
        elif group.startswith('static_website_') and group.endswith('s'):
            group = '.'.join(group.split('_')[2:])[:-1]

        if group:
            add_tag(dashboard, group)

    add_rows(dashboard, host, groups, hostvars, cpu_count)

    return dashboard


class FilterModule(object):
    '''Ansible jinja2 filters for grafana load graphs'''

    def filters(self):
        return {
            'dashboard_host': dashboard_host,
            }
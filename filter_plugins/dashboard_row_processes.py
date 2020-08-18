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
from dashboard_graph import new as new_graph
from dashboard_row import new as new_row
from dashboard_row import add_panel
del sys.path[0]


def panel_processes(host, running=True, total=True, width=None):
    title = 'Processes'
    if running and not total:
        title += ' running'
    elif total and not running:
        title += ' total'
    panel = new_graph(title, width=width)

    if running:
        add_metric(panel, host, 'loadavg.processes_running', 'processes running')
    if total:
        add_metric(panel, host, 'loadavg.processes_total', 'processes total')
    set_colors(panel, {
            'processes running': '#7eb26d',
            'processes total': '#eab839',
            })

    return panel


def row_processes(host):
    title = 'Processes'
    row = new_row(title)
    width=4

    add_panel(row, panel_processes(host, total=False, width=width))
    add_panel(row, panel_processes(host, running=False, width=width))
    add_panel(row, panel_processes(host, width=width))

    return row


class FilterModule(object):
    '''Ansible jinja2 filters for process graphs in dashboards'''

    def filters(self):
        return {
            }

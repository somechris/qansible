# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dashboard_metrics import add_metric
from dashboard_metrics import add_series_override
from dashboard_metrics import set_colors
from dashboard_metrics import set_yaxis_labels
from dashboard_metrics import set_yaxis_maximum
from dashboard_metrics import set_fill
from dashboard_metrics import set_decimals
from dashboard_metrics import set_threshold
from dashboard_graph import new as new_graph
from dashboard_row import new as new_row
from dashboard_row import add_panel
del sys.path[0]


def set_threshold_w_fallback(panel, cpu_count, host=None):
    color = 'rgb(216, 27, 27)'
    if cpu_count:
        set_threshold(panel, cpu_count, color)
        set_yaxis_maximum(panel, 'left', int(cpu_count)*5./4)
    elif host:
        add_metric(panel, host, 'cpu.cpu_count', 'CPUs')
        add_series_override(panel, '/CPUs/', {'linewidth': 2.5})
        set_colors(panel, {'CPUs': color})


def panel_load(host, cpu_count=False, width=None):
    title = "Load"
    panel = new_graph(title, width=width)

    add_metric(panel, host, 'loadavg.15', 'Load 15m')
    add_metric(panel, host, 'loadavg.01', 'Load 1m')

    set_decimals(panel, 2)
    set_fill(panel, 0)
    set_yaxis_labels(panel, "load")
    add_series_override(panel, '/CPUs/', {'linewidth': 3})
    add_series_override(panel, '/Load 15/', {'linewidth': 0, 'fill': 4})

    set_threshold_w_fallback(panel, cpu_count, host)

    return panel


def panel_load_kind(host, kind=1, cpu_count=False):
    title = "Load %sm" % (kind)
    panel = new_graph(title)

    add_metric(panel, host, 'loadavg.%s' % (str(kind).zfill(2)), 'Load %sm' % kind)

    set_decimals(panel, 2)
    set_threshold_w_fallback(panel, cpu_count, host)

    return panel


def row_load(host, cpu_count):
    title = 'Load'
    row = new_row(title)

    for kind in [1, 5, 15]:
        add_panel(row, panel_load_kind(host, kind, cpu_count))

    return row


class FilterModule(object):
    '''Ansible jinja2 filters for load graphs in Grafana'''

    def filters(self):
        return {
            }

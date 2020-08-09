# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grafana_scaffolding import update_dict
from grafana_scaffolding import get_default_graph
from grafana_scaffolding import get_default_row
from grafana_scaffolding import add_row
from grafana_metrics import add_metric
from grafana_metrics import connect_missing_points
from grafana_metrics import set_colors
from grafana_metrics import set_content
from grafana_metrics import set_decimals
from grafana_metrics import set_fill
from grafana_metrics import set_point_mode
from grafana_metrics import set_stacked_mode
from grafana_metrics import set_threshold
from grafana_metrics import set_yaxis_helper
from grafana_metrics import set_yaxis_labels
from grafana_metrics import set_yaxis_maximum
from grafana_metrics import set_yaxis_minimum
from grafana_metrics import set_yaxis_units
from grafana_metrics import switch_to_right_axis
from grafana_metrics import zero_missing_points
del sys.path[0]


MAX_CPU=900

def grafana_panel_cpu(host, span=3):
    title = "CPU %"
    ret = get_default_graph(title, span)

    add_metric(ret, host, 'cpu.total.user')
    add_metric(ret, host, 'cpu.total.nice')
    add_metric(ret, host, 'cpu.total.system')
    add_metric(ret, host, 'cpu.total.iowait')
    add_metric(ret, host, 'cpu.total.irq')
    add_metric(ret, host, 'cpu.total.softirq')
    add_metric(ret, host, 'cpu.total.steal')
    add_metric(ret, host, 'cpu.total.idle')

    set_yaxis_units(ret, "percent")
    set_yaxis_maximum(ret, 'left', MAX_CPU) # Add max to limit effect of outliers.
    set_stacked_mode(ret)
    set_colors(ret, {
            "idle": "#3F2B5B",
            "iowait": "#BA43A9",
            "softirq": "#1F78C1",
            "steal": "#0A50A1",
            })
    return ret


def grafana_panel_cpu_kind(host, kind, color, span=3):
    title = kind
    ret = get_default_graph(title, span)

    add_metric(ret, host, 'cpu.total.%s' % kind)

    set_yaxis_units(ret, "percent")
    set_yaxis_maximum(ret, 'left', MAX_CPU) # Add max to limit effect of outliers.
    set_stacked_mode(ret)
    set_colors(ret, {
            kind: color,
            })
    return ret


def grafana_add_row_cpu(dashboard, host, repeated=False, collapse=True):
    span = 3
    title = 'CPU'
    row = get_default_row(title, host, repeated, collapse)
    update_dict(row, {
            "panels": [
                grafana_panel_cpu_kind(host, 'user', '#7EB26D', span=span),
                grafana_panel_cpu_kind(host, 'nice', '#EAB839', span=span),
                grafana_panel_cpu_kind(host, 'system', '#6ED0E0', span=span),
                grafana_panel_cpu_kind(host, 'iowait', '#BA43A9', span=span),
                grafana_panel_cpu_kind(host, 'irq', '#E24D42', span=span),
                grafana_panel_cpu_kind(host, 'softirq', '#1F78C1', span=span),
                grafana_panel_cpu_kind(host, 'steal', '#0A50A1', span=span),
                grafana_panel_cpu_kind(host, 'idle', '#3F2B5B', span=span),
                ],
            })
    return add_row(dashboard, row)


class FilterModule(object):
    '''Ansible jinja2 filters for grafana cpu graphs'''

    def filters(self):
        return {
            'grafana_add_row_cpu': grafana_add_row_cpu,
            }

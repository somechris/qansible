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


def grafana_panel_memory(host, span=3):
    title = "Memory"
    ret = get_default_graph(title, span)

    add_metric(ret, host, ['memory.MemTotal', '#B', '#C', '#D'], 'Used w/o Buffers and Cache', sum='diff')
    add_metric(ret, host, 'memory.Buffers')
    add_metric(ret, host, 'memory.Cached')
    add_metric(ret, host, 'memory.MemFree', 'Free')

    set_stacked_mode(ret)
    set_yaxis_units(ret, "bytes")
    set_colors(ret, {
            "Buffers": "#1F78C1",
            "Cached": "#0A50A1",
            "Free": "#3F2B5B",
            })

    return ret


def grafana_panel_memory_kind(host, metric, label=None, color=None, span=3):
    if metric == 'used':
        title = 'Used w/o Buffers and Cache'
        label = title
    elif label:
        title = label
    else:
        title = metric
        label = title
    ret = get_default_graph(title, span)

    if metric == 'used':
        add_metric(ret, host, ['memory.MemTotal', '#B', '#C', '#D'], label, sum='diff')
        add_metric(ret, host, 'memory.Buffers', visible=False)
        add_metric(ret, host, 'memory.Cached', visible=False)
        add_metric(ret, host, 'memory.MemFree', visible=False)
    else:
        add_metric(ret, host, 'memory.%s' % metric, label)

    set_stacked_mode(ret)
    set_yaxis_units(ret, "bytes")
    if color:
        set_colors(ret, {
                label: color
                })

    return ret


def grafana_add_row_memory(dashboard, host, repeated=False, collapse=True):
    span = 3
    title = 'Memory'
    row = get_default_row(title, host, repeated, collapse)
    update_dict(row, {
            "panels": [
                grafana_panel_memory_kind(host, 'used', span=span),
                grafana_panel_memory_kind(host, 'Buffers', color='#1F78C1', span=span),
                grafana_panel_memory_kind(host, 'Cached', color='#0A50A1', span=span),
                grafana_panel_memory_kind(host, 'MemFree', label='Free', color='#3F2B5B', span=span),
                ],
            })
    return add_row(dashboard, row)


class FilterModule(object):
    '''Ansible jinja2 filters for grafana memory graphs'''

    def filters(self):
        return {
            'grafana_add_row_memory': grafana_add_row_memory,
            }

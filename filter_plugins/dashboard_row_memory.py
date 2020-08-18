# -*- coding: utf-8 -*-

import os
import sys
import copy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dashboard_metrics import add_metric
from dashboard_metrics import add_series_override
from dashboard_metrics import set_colors
from dashboard_metrics import set_yaxis_labels
from dashboard_metrics import set_yaxis_units
from dashboard_metrics import set_fill
from dashboard_metrics import set_decimals
from dashboard_metrics import set_stacked_mode
from dashboard_graph import new as new_graph
from dashboard_row import new as new_row
from dashboard_row import add_panel
del sys.path[0]

COLORS={
    "Buffers": "#1F78C1",
    "Cached": "#0A50A1",
    "Free": "#3F2B5B",
    }

DEFAULT_METRICS=[
    'used',
    'Buffers',
    'Cached',
    'MemFree',
    ]

def panel_memory(host, metrics=DEFAULT_METRICS, width=None, title=None):
    if not isinstance(metrics, list):
        metrics = [metrics]

    if title is None:
        if metrics == DEFAULT_METRICS:
            title = 'Memory'
        elif metrics == ['used']:
            title = 'Used w/o Buffers and Cache'
        else:
            title = ','.join(metrics)

    panel = new_graph(title, width=width)

    if 'used' in metrics:
        add_metric(panel, host, ['memory.MemTotal', '#B', '#C', '#D'], 'Used w/o Buffers and Cache', sum='diff')
        add_metric(panel, host, 'memory.Buffers', visible=('Buffers' in metrics))
        add_metric(panel, host, 'memory.Cached', visible=('Cached' in metrics))
        add_metric(panel, host, 'memory.MemFree', 'Free', visible=('MemFree' in metrics))
        metrics = copy.copy(metrics)
        for metric in ['used', 'Buffers', 'Cached', 'MemFree']:
            if metric in metrics:
                metrics.remove(metric)

    for metric in metrics:
        if metric == 'MemFree':
            label = 'Free'
        else:
            label = metric

        add_metric(panel, host, 'memory.%s' % metric, label)

    set_stacked_mode(panel)
    set_yaxis_units(panel, "bytes")
    set_colors(panel, COLORS)

    return panel


def row_memory(host):
    title = 'Memory'
    row = new_row(title)

    for metric in DEFAULT_METRICS:
        add_panel(row, panel_memory(host, [metric], width=3))

    return row


class FilterModule(object):
    '''Ansible jinja2 filters for memory graphs in dashboards'''

    def filters(self):
        return {
            }

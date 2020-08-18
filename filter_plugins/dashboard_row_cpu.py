# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dashboard_metrics import add_metric
from dashboard_metrics import set_colors
from dashboard_metrics import set_stacked_mode
from dashboard_metrics import set_yaxis_maximum
from dashboard_metrics import set_yaxis_units
from dashboard_graph import new as new_graph
from dashboard_row import new as new_row
from dashboard_row import add_panel
del sys.path[0]


MAX_CPU=9

COLORS = {
  'user': '#7EB26D',
  'nice': '#EAB839',
  'system': '#6ED0E0',
  'iowait': '#BA43A9',
  'irq': '#E24D42',
  'softirq': '#1F78C1',
  'steal': '#0A50A1',
  'guest': '#999999',
  'guest_nice': '#CCCCCC',
  'idle': '#3F2B5B',
  }

KINDS=[
    'user',
    'nice',
    'system',
    'iowait',
    'irq',
    'softirq',
    'steal',
    'guest',
    'guest_nice',
    'idle',
    ]

def panel_cpu(host, title=None, kinds=KINDS, width=None):
    if not isinstance(kinds, list):
        kinds = [kinds]

    if title is None:
        title = 'CPU'
        if kinds != ['*'] and kinds != KINDS:
            title += ' [' + (','.join(kinds)) + ']'

    panel = new_graph(title, width=width)

    for kind in kinds:
        add_metric(panel, host, 'cpu.total.%s' % kind)

    set_yaxis_units(panel, 'percent')
    set_stacked_mode(panel)
    set_colors(panel, COLORS)
    return panel


def row_cpu(host):
    title = 'CPU'
    row = new_row(title)
    width = 3

    for kind in KINDS:
        add_panel(row, panel_cpu(host, title=kind,kinds=[kind], width=width))

    return row


class FilterModule(object):
    '''Ansible jinja2 filters for cpu graphs in dashboards'''

    def filters(self):
        return {
            }

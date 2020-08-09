# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grafana_scaffolding import update_dict
from grafana_scaffolding import get_default_graph
from grafana_scaffolding import get_default_row
from grafana_scaffolding import add_row
from grafana_metrics import add_metric
from grafana_metrics import add_series_override
from grafana_metrics import set_decimals
from grafana_metrics import set_fill
from grafana_metrics import set_yaxis_labels
from grafana_metrics import set_threshold
del sys.path[0]


def grafana_add_row_load(dashboard, host, cpu_count=False, repeated=False, collapse=True):
    global default_row
    span = 4
    title = 'Load'
    row = get_default_row(title, host, repeated, collapse)
    update_dict(row, {
            "panels": [
                grafana_panel_load_kind(host, span=span, kind=1, cpu_count=cpu_count),
                grafana_panel_load_kind(host, span=span, kind=5, cpu_count=cpu_count),
                grafana_panel_load_kind(host, span=span, kind=15,cpu_count=cpu_count),
                ],
            })
    return add_row(dashboard, row)

def grafana_panel_load(host, span=3, cpu_count=False):
    title = "Load"
    ret = get_default_graph(title, span)

    add_metric(ret, host, 'loadavg.15', 'Load 15m')
    add_metric(ret, host, 'loadavg.01', 'Load 1m')

    set_decimals(ret, 2)
    set_fill(ret, 0)
    set_yaxis_labels(ret, "load")
    add_series_override(ret, '/CPUs/', {'linewidth': 3})
    add_series_override(ret, '/Load 15/', {'linewidth': 0, 'fill': 4})

    set_threshold(ret, cpu_count, host)

    return ret


def grafana_panel_load_kind(host, span=3, kind=1, cpu_count=False):
    title = "Load 1m"
    ret = get_default_graph(title, span)

    add_metric(ret, host, 'loadavg.%s' % (str(kind).zfill(2)), 'Load %sm' % kind)

    set_decimals(ret, 2)
    set_threshold(ret, cpu_count)

    return ret


class FilterModule(object):
    '''Ansible jinja2 filters for grafana load graphs'''

    def filters(self):
        return {
            'grafana_add_row_load': grafana_add_row_load,
            }

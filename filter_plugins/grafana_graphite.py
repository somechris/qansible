# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grafana_scaffolding import update_dict
from grafana_scaffolding import get_default_graph
from grafana_scaffolding import get_default_text
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

def grafana_add_row_graphite(dashboard, host, add=True, repeated=False, collapse=True):
    span = 4
    title = 'Graphite'
    row = get_default_row(title, host, repeated, collapse)
    update_dict(row, {
            "panels": [
                grafana_panel_graphite_cache(host, span=span),
                grafana_panel_graphite_updates(host, span=span),
                grafana_panel_graphite_monitors(host, span=span),
                ],
            })
    return add_row(dashboard, row) if add else dashboard


def grafana_panel_graphite_cache(host, span=4):
    title = "Cache"
    ret = get_default_graph(title, span)

    add_metric(ret, host, "graphite.carbon.agents.*.cache.queries")
    add_metric(ret, host, "graphite.carbon.agents.*.cache.queues")

    return ret


def grafana_panel_graphite_updates(host, span=4):
    title = "Updates"
    ret = get_default_graph(title, span)

    add_metric(ret, host, "graphite.carbon.agents.*.metricsReceived")
    add_metric(ret, host, "graphite.carbon.agents.*.committedPoints")
    add_metric(ret, host, "graphite.carbon.agents.*.updateOperations")

    return ret


def grafana_panel_graphite_monitors(host, span=4):
    title = "Monitors"
    ret = get_default_graph(title, span)

    add_metric(ret, host, "graphite.carbon.agents.*.creates")
    add_metric(ret, host, "graphite.carbon.agents.*.errors")

    return ret


class FilterModule(object):
    '''Ansible jinja2 filters for grafana graphite graphs'''

    def filters(self):
        return {
            'grafana_add_row_graphite': grafana_add_row_graphite,
            }

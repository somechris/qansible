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


def panel_graphite_cache(host, width=None):
    title = "Cache"
    panel = new_graph(title, width=width)

    add_metric(panel, host, "graphite.carbon.agents.*.cache.queries")
    add_metric(panel, host, "graphite.carbon.agents.*.cache.queues")

    return panel


def panel_graphite_updates(host, width=None):
    title = "Updates"
    panel = new_graph(title, width=width)

    add_metric(panel, host, "graphite.carbon.agents.*.metricsReceived")
    add_metric(panel, host, "graphite.carbon.agents.*.committedPoints")
    add_metric(panel, host, "graphite.carbon.agents.*.updateOperations")

    return panel


def panel_graphite_monitors(host, width=None):
    title = "Monitors"
    panel = new_graph(title, width=width)

    add_metric(panel, host, "graphite.carbon.agents.*.creates")
    add_metric(panel, host, "graphite.carbon.agents.*.errors")

    return panel

def row_graphite(host):
    title = 'Graphite'
    row = new_row(title)
    width=4

    add_panel(row, panel_graphite_cache(host, width=width))
    add_panel(row, panel_graphite_updates(host, width=width))
    add_panel(row, panel_graphite_monitors(host, width=width))

    return row


class FilterModule(object):
    '''Ansible jinja2 filters for Graphite graphs in dashboards'''

    def filters(self):
        return {
            'dashboard_row_graphite': row_graphite,
            }

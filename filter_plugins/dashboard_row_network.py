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


def panel_network_bytes(host, title='Network bytes', width=None):
    panel = new_graph(title, width=width)

    add_metric(panel, host, 'network.*.rx_byte', [-2, -1])
    add_metric(panel, host, 'network.*.tx_byte', [-2, -1])

    set_yaxis_units(panel, "Bps")

    return panel


def panel_network_packets(host, width=None):
    title = 'Network packets'
    panel = new_graph(title, width=width)

    add_metric(panel, host, 'network.*.rx_packets', [-2, -1])
    add_metric(panel, host, 'network.*.tx_packets', [-2, -1])

    set_yaxis_units(panel, "pps")

    return panel


def panel_network_drop_and_errors(host, width=None):
    title = 'Network packets'
    panel = new_graph(title, width=width)

    add_metric(panel, host, 'network.*.rx_drop', [-2, -1])
    add_metric(panel, host, 'network.*.rx_errors', [-2, -1])
    add_metric(panel, host, 'network.*.tx_drop', [-2, -1])
    add_metric(panel, host, 'network.*.tx_errors', [-2, -1])

    return panel


def row_network(host):
    title = 'Network'
    row = new_row(title)
    width=4

    add_panel(row, panel_network_bytes(host, width=width))
    add_panel(row, panel_network_packets(host, width=width))
    add_panel(row, panel_network_drop_and_errors(host, width=width))

    return row


class FilterModule(object):
    '''Ansible jinja2 filters for network graphs in dashboards'''

    def filters(self):
        return {
            }

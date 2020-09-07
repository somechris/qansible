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

def panel_ready(host, width=None):
    panel = new_graph('Ready?', width=width)

    add_metric(panel, host, 'jetdirect.ready', 'Printer Ready')
    add_metric(panel, host, 'jetdirect.status', 'Printer Status')
    add_metric(panel, host, 'jetdirect.*.*.ready', [-3,-2])

    return panel


def panel_equivalent_a4_impressions(host, width=None):
    panel = new_graph('Equvalent impressions A4', width=width)

    add_metric(panel, host, 'jetdirect.usage.equivalent_impressions_a4_letter.*.*')

    return panel


def panel_impressions(host, width=None):
    panel = new_graph('Actual Impressions', width=width)

    add_metric(panel, host, 'jetdirect.usage.impressions.*.*')

    add_series_override(panel, '/units/', {'legend': False, 'hiddenSeries': True})

    return panel


def panel_sources(host, width=None):
    panel = new_graph('Sources', width=width)

    add_metric(panel, host, 'jetdirect.usage.source.*.*', [-2])

    return panel


def row_hp_printer_overview(host):
    width = 3

    row = new_row('Overview', collapsed=False)
    add_panel(row, panel_ready(host, width=width))
    add_panel(row, panel_equivalent_a4_impressions(host, width=width))
    add_panel(row, panel_impressions(host, width=width))
    add_panel(row, panel_sources(host, width=width))

    return row


class FilterModule(object):
    '''Ansible jinja2 filters for HP printer overview rows in dashboards'''

    def filters(self):
        return {
            }

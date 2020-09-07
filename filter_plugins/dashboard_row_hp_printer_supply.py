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

BASIC_COLORS = {
  'black_cartridge': '#FFFFFF',
  'cyan_cartridge': '#00FFFF',
  'yellow_cartridge': '#FFFF00',
  'magenta_cartridge': '#FF00FF',
  'image_fuser_kit': '#FF0000',
  'image_transfer_kit': '#00FF00',
  'toner_collection_unit': '#8080FF',
  }

EXTENDED_COLORS = {}

def set_extended_colors(panel):
    if not EXTENDED_COLORS:
        for key, value in BASIC_COLORS.iteritems():
            for suffix in [
                '',
                '.ready',
                '.percent_remaining',
                '.pages_printed',
                '.pages_remaining',
                ]:
                EXTENDED_COLORS[key + suffix] = value
    set_colors(panel, EXTENDED_COLORS)

def panel_supply(host, supply, supply_aspect, metric_base, metric_end, width=None, alias=None):
    if alias is None:
        alias = [-2, -1]
    panel = new_graph('%s %s' % (supply, supply_aspect), width=width)

    add_metric(panel, host, '%s.%s' % (metric_base, metric_end), alias)

    set_extended_colors(panel)

    return panel


def panel_supply_ready(host, supply, metric_base, width=None, alias=None):
    return panel_supply(host, supply, 'Ready?', metric_base, 'ready', width=width, alias=alias)


def panel_supply_percent_remaining(host, supply, metric_base, width=None, alias=None):
    return panel_supply(host, supply, 'Percent Remaining', metric_base, 'percent_remaining', width=width, alias=alias)


def panel_supply_pages_printed(host, supply, metric_base, width=None, alias=None):
    return panel_supply(host, supply, 'Pages Printed', metric_base, 'pages_printed', width=width, alias=alias)


def panel_supply_pages_remaining(host, supply, metric_base, width=None, alias=None):
    return panel_supply(host, supply, 'Pages Remaining', metric_base, 'pages_remaining', width=width, alias=alias)


def row_hp_printer_supply(host, title, supply=None, collapsed=None, percent=True, pages=True):
    alias = None
    if supply is None:
        supply = title.lower().replace(' ', '_')
    elif supply == '*':
        alias = [-2]
    metric_base = 'jetdirect.supply.%s' % (supply)
    width = 3

    row = new_row('Supply: %s' % title, collapsed=collapsed)
    add_panel(row, panel_supply_ready(host, title, metric_base, width, alias))
    if percent:
        add_panel(row, panel_supply_percent_remaining(host, title, metric_base, width, alias))
    if pages:
        add_panel(row, panel_supply_pages_printed(host, title, metric_base, width, alias))
        add_panel(row, panel_supply_pages_remaining(host, title, metric_base, width, alias))

    return row


class FilterModule(object):
    '''Ansible jinja2 filters for HP printer supply rows in dashboards'''

    def filters(self):
        return {
            }

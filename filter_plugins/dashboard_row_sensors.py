# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dashboard_metrics import add_metric
from dashboard_metrics import set_colors
from dashboard_metrics import set_stacked_mode
from dashboard_metrics import set_yaxis_labels
from dashboard_metrics import set_yaxis_minimum
from dashboard_metrics import set_yaxis_units
from dashboard_graph import new as new_graph
from dashboard_row import new as new_row
from dashboard_row import add_panel
del sys.path[0]


MAX_CPU=9

def panel_bus(host, width=None):
    title = 'Device changes per bus'
    panel = new_graph(title, width=width)

    add_metric(panel, host, 'sensors.bus.*', der=True)

    set_yaxis_labels(panel, 'changed devices')
    set_yaxis_minimum(panel, 'left', None)
    return panel


def panel_sensor_group(host, title, group, unit, width=None):
    panel = new_graph(title, width=width)

    add_metric(panel, host, 'sensors.%s.*.*' % (group))

    set_yaxis_units(panel, unit)
    return panel


def row_sensors(host):
    title = 'Hardware sensors'
    row = new_row(title)
    width = 3

    add_panel(row, panel_bus(host, width=width))
    add_panel(row, panel_sensor_group(host, title='Temperature', group='temp', unit='celsius', width=width))
    add_panel(row, panel_sensor_group(host, title='Cooling', group='fan', unit='rotrpm', width=width))
    add_panel(row, panel_sensor_group(host, title='Voltage', group='voltage', unit='volt', width=width))

    return row


class FilterModule(object):
    '''Ansible jinja2 filters for sensor graphs in dashboards'''

    def filters(self):
        return {
            }

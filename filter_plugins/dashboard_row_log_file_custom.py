# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dashboard_row_log_file_shared import new
from dashboard_row_log_file_shared import metric_base
from dashboard_metrics import add_metric
from dashboard_metrics import set_yaxis_labels
from dashboard_metrics import set_yaxis_units
from dashboard_graph import new as new_graph
from dashboard_row import add_panel
from dashboard_metrics import zero_missing_points
del sys.path[0]

def panel_count(host, base, kinds=['*'], prefix='All', by=None, width=None, zero_missing=False):
    title = prefix + ' Log Lines'
    if by:
        title += ' by ' + by
    panel = new_graph(title, width=width)

    for kind in kinds:
        add_metric(panel, host, '%s.%s.count' % (base, kind), [-2])

    set_yaxis_labels(panel, "Lines/min")
    zero_missing_points(panel)

    return panel


def panel_length_average(host, base, width=None):
    title = "Average Line Length"
    panel = new_graph(title, width=width)

    add_metric(panel, host, '%s.total.length.average' % (base), 'Bytes')

    set_yaxis_units(panel, "bytes")

    return panel


def row_log_file_custom(host, log_file):
    row = new(host, log_file)

    base = metric_base(log_file)
    add_panel(row, panel_count(host, base, width=6))
    add_panel(row, panel_length_average(host, base, width=6))
    return row


class FilterModule(object):
    '''Ansible jinja2 filters for Apache graphs in dashboards'''

    def filters(self):
        return {
            }

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
from dashboard_metrics import set_point_mode
from dashboard_metrics import set_stacked_mode
from dashboard_metrics import set_threshold
from dashboard_metrics import set_yaxis_labels
from dashboard_metrics import switch_to_right_axis
from dashboard_metrics import zero_missing_points
from dashboard_metrics import connect_missing_points
from dashboard_graph import new as new_graph
from dashboard_markdown import new as new_markdown
from dashboard_markdown import set_content
from dashboard_row import new as new_row
from dashboard_row import add_panel
from dashboard_websites_shared import METHODS
from dashboard_websites_shared import TIMINGS
from dashboard_websites_shared import web_metric_base
from dashboard import add_row
del sys.path[0]


def panel_website_timing_per_method_detailed(host, metric_base, method, width=None):
    title = 'Method %s' % (method)
    panel = new_graph(title, width=width)

    for p in TIMINGS:
        add_metric(panel, host, '%s.method.%s.duration.%s' % (metric_base, method, p[0]), p[1])

    connect_missing_points(panel)
    set_point_mode(panel)
    set_yaxis_units(panel, "ms")

    return panel


def row_website_timing_per_method(host, engine, website, aspect):
    title = '%s %s timing per method' % (website, ' (' + aspect + ')' if aspect else '')
    row = new_row(title)
    width = 3

    metric_base = web_metric_base(engine, website, aspect)
    for method in METHODS:
        add_panel(row,  panel_website_timing_per_method_detailed(host, metric_base, method, width=width))

    return row


class FilterModule(object):
    '''Ansible jinja2 filters for timing by method in dashboards'''

    def filters(self):
        return {
            }

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
from dashboard_websites_shared import STATUSES
from dashboard_websites_shared import METHODS
from dashboard_websites_shared import TIMINGS
from dashboard_websites_shared import web_metric_base
from dashboard import add_row
del sys.path[0]


def panel_website_requests_per_status(host, metric_base, status, alias, width=None):
    if status == '*':
        title = 'All available statuses'
        alias = [-2]
    else:
        title = 'Status %s (%s)' % (status, alias)
        alias = '%s - %s' % (status, alias)
    panel = new_graph(title, width=width)

    add_metric(panel, host, "%s.status.%s.count" % (metric_base, status), alias, scale=True)

    set_yaxis_labels(panel, 'req/s')
    zero_missing_points(panel)

    return panel


def row_website_status_details(host, engine, website, aspect):
    title = '%s %s status details' % (
        website,
        ' (' + aspect + ')' if aspect else '')
    row = new_row(title)
    width = 3

    metric_base = web_metric_base(engine, website, aspect)
    for status in STATUSES + [
        ('*', None),
        ]:
        add_panel(row, panel_website_requests_per_status(host, metric_base, status[0], status[1], width=width))

    return row


class FilterModule(object):
    '''Ansible jinja2 filters for website volume KPIs in dashboards'''

    def filters(self):
        return {
            }

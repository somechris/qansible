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


def panel_website_requests_total(host, metric_base, width=None):
    title = "Total requests"
    panel = new_graph(title, width=width)

    add_metric(panel, host, '%s.total.count' % (metric_base), 'Requests', scale=True)

    set_yaxis_labels(panel, "req/s")

    return panel


def panel_website_requests_per_status_group(host, metric_base, width=None):
    title = "Requests per HTTP response status"
    panel = new_graph(title, width=width)

    add_metric(panel, host, '%s.status.1xx.count' % (metric_base), '1xx - Informational', scale=True)
    add_metric(panel, host, '%s.status.2xx.count' % (metric_base), '2xx - Success', scale=True)
    add_metric(panel, host, '%s.status.3xx.count' % (metric_base), '3xx - Redirection', scale=True)
    add_metric(panel, host, '%s.status.4xx.count' % (metric_base), '4xx - Client error', scale=True)
    add_metric(panel, host, '%s.status.5xx.count' % (metric_base), '5xx - Server error', scale=True)
    add_metric(panel, host, '%s.status.unparsable.count' % (metric_base), 'Unparsable', scale=True)

    set_yaxis_labels(panel, "req/s")

    return panel


def panel_website_requests_per_method(host, metric_base, width=None):
    title = "Requests per HTTP method"
    panel = new_graph(title, width=width)

    for method in METHODS:
        add_metric(panel, host, '%s.method.%s.count' % (metric_base, method), [-2], scale=True)

    set_yaxis_labels(panel, "req/s")

    return panel


def panel_website_requests_per_user(host, metric_base, width=None):
    title = "Requests per User"
    panel = new_graph(title, width=width)

    add_metric(panel, host, '%s.user.*.count' % (metric_base), [-2], scale=True)

    set_yaxis_labels(panel, 'req/s')
    zero_missing_points(panel)

    return panel


def row_website_volume_kpi(host, engine, website, aspect):
    title = '%s %s volume KPI' % (
        website,
        (' (' + aspect + ')') if aspect else '')
    row = new_row(title)
    width=3

    metric_base = web_metric_base(engine, website, aspect)
    add_panel(row, panel_website_requests_total(host, metric_base, width=width))
    add_panel(row, panel_website_requests_per_status_group(host, metric_base, width=width))
    add_panel(row, panel_website_requests_per_method(host, metric_base, width=width))
    add_panel(row, panel_website_requests_per_user(host, metric_base, width=width))

    return row


class FilterModule(object):
    '''Ansible jinja2 filters for website volume KPIs in dashboards'''

    def filters(self):
        return {
            }

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
from dashboard_row_website_ssl import row_website_ssl
from dashboard_row_website_status_details import row_website_status_details
from dashboard_row_website_timing_kpi import row_website_timing_kpi
from dashboard_row_website_timing_per_method import row_website_timing_per_method
from dashboard_row_website_timing_per_status import row_website_timing_per_status
from dashboard_row_website_volume_kpi import row_website_volume_kpi
from dashboard_websites_shared import METHODS
from dashboard_websites_shared import STATUSES
from dashboard_websites_shared import web_metric_base
from dashboard_row import new as new_row
from dashboard_row import add_panel
from dashboard_row import set_weight
from dashboard import add_row
del sys.path[0]

FALLBACK_SITES=[
    'other_vhosts',
    'fallback',
    'default',
    ]

def panel_websites(host, websites, width=None):
    title = 'Hosted websites'
    ret = new_markdown(title, width=width)

    def format(website):
        ret = ''
        if website == 'default':
            ret = website
        else:
            ret = "[" + website + "](https://" + website + ")"
        ret = '* ' + ret
        return ret
    set_content(ret, "\n".join([format(website) for website in websites]))

    return ret


def panel_website_total_requests(host, engine, width=None):
    title = 'Total requests served'
    panel = new_graph(title, width=width)

    add_metric(panel, host, ['logs.%s.*.*.total.count' % (engine), 'logs.%s.*.total.count' % (engine)], 'Total requests', scale=True)
    add_metric(panel, host, 'logs.%s.*.*.total.count' % (engine), [-4, -3], scale=True)
    add_metric(panel, host, 'logs.%s.*.total.count' % (engine), [-3], scale=True)

    set_yaxis_labels(panel, "req/s")

    return panel


def rows_website_variant(host, engine, website, aspect=None, timing=True, ssl=False):
    rows = [
        row_website_volume_kpi(host, engine, website, aspect),
        row_website_status_details(host, engine, website, aspect),
        ]
    if ssl:
        rows.append(row_website_ssl(host, engine, website, aspect))
    if timing:
        rows += [
            row_website_timing_kpi(host, engine, website, aspect),
            row_website_timing_per_status(host, engine, website, aspect),
            row_website_timing_per_method(host, engine, website, aspect),
            ]

    weight_prefix = 'website-%s-%s-%s-' % (
        'late' if website in FALLBACK_SITES else 'early',
        website,
        'encrypted' if aspect == 'https' else 'unencrypted')
    number = 2000
    for row in rows:
        set_weight(row, weight_prefix + str(number))
        number += 1000
    return rows


def rows_website(host, engine, website):
    rows = []
    is_fallback = (website in FALLBACK_SITES)
    if is_fallback:
        rows += rows_website_variant(host, engine, website, timing=False)
    else:
        rows += rows_website_variant(host, engine, website, aspect='https', ssl=True)
        rows += rows_website_variant(host, engine, website, aspect='http', ssl=False)
    return rows


class FilterModule(object):
    '''Ansible jinja2 filters for Apache graphs in dashboards'''

    def filters(self):
        return {
            'dashboard_rows_website': rows_website,
            }

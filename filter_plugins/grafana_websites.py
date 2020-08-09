# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grafana_scaffolding import update_dict
from grafana_scaffolding import get_default_graph
from grafana_scaffolding import get_default_text
from grafana_scaffolding import get_default_row
from grafana_scaffolding import add_row
from grafana_metrics import add_metric
from grafana_metrics import connect_missing_points
from grafana_metrics import set_colors
from grafana_metrics import set_content
from grafana_metrics import set_decimals
from grafana_metrics import set_fill
from grafana_metrics import set_point_mode
from grafana_metrics import set_stacked_mode
from grafana_metrics import set_threshold
from grafana_metrics import set_yaxis_helper
from grafana_metrics import set_yaxis_labels
from grafana_metrics import set_yaxis_maximum
from grafana_metrics import set_yaxis_minimum
from grafana_metrics import set_yaxis_units
from grafana_metrics import switch_to_right_axis
from grafana_metrics import zero_missing_points
del sys.path[0]


def grafana_web_metric_base(engine, website, aspect):
    website = website.replace('.', '_').replace('-', '_')
    aspect = ('.' + aspect if aspect else '')
    return 'logs.%s.%s%s' % (engine, website, aspect)


def grafana_panel_website_requests_total(host, metric_base, span=3):
    title = "Total requests"
    ret = get_default_graph(title, span)

    add_metric(ret, host, '%s.total.count' % (metric_base), 'Requests', scale=True)

    set_yaxis_labels(ret, "req/s")

    return ret


def grafana_panel_website_requests_per_status_group(host, metric_base, span=3):
    title = "Requests per HTTP response status"
    ret = get_default_graph(title, span)

    add_metric(ret, host, '%s.status.1xx.count' % (metric_base), '1xx - Informational', scale=True)
    add_metric(ret, host, '%s.status.2xx.count' % (metric_base), '2xx - Success', scale=True)
    add_metric(ret, host, '%s.status.3xx.count' % (metric_base), '3xx - Redirection', scale=True)
    add_metric(ret, host, '%s.status.4xx.count' % (metric_base), '4xx - Client error', scale=True)
    add_metric(ret, host, '%s.status.5xx.count' % (metric_base), '5xx - Server error', scale=True)
    add_metric(ret, host, '%s.status.unparsable.count' % (metric_base), 'Unparsable', scale=True)

    set_yaxis_labels(ret, "req/s")

    return ret


def grafana_panel_website_requests_per_method(host, metric_base, span=3):
    title = "Requests per HTTP method"
    ret = get_default_graph(title, span)

    add_metric(ret, host, '%s.method.CONNECT.count' % (metric_base), [-2], scale=True)
    add_metric(ret, host, '%s.method.DELETE.count' % (metric_base), [-2], scale=True)
    add_metric(ret, host, '%s.method.GET.count' % (metric_base), [-2], scale=True)
    add_metric(ret, host, '%s.method.HEAD.count' % (metric_base), [-2], scale=True)
    add_metric(ret, host, '%s.method.OPTIONS.count' % (metric_base), [-2], scale=True)
    add_metric(ret, host, '%s.method.POST.count' % (metric_base), [-2], scale=True)
    add_metric(ret, host, '%s.method.PUT.count' % (metric_base), [-2], scale=True)
    add_metric(ret, host, '%s.method.TRACE.count' % (metric_base), [-2], scale=True)
    add_metric(ret, host, '%s.method.unparsable.count' % (metric_base), 'Unparsable', scale=True)

    set_yaxis_labels(ret, 'req/s')

    return ret


def grafana_panel_website_requests_per_user(host, metric_base, span=3):
    title = "Requests per User"
    ret = get_default_graph(title, span)

    add_metric(ret, host, '%s.user.*.count' % (metric_base), [-2], scale=True)

    set_yaxis_labels(ret, 'req/s')
    zero_missing_points(ret)

    return ret


def grafana_panel_website_requests_per_status(host, metric_base, status, alias, span=3):
    if status == '*':
        title = 'All available statuses'
        alias = [-2]
    else:
        title = 'Status %s (%s)' % (status, alias)
        alias = '%s - %s' % (status, alias)
    ret = get_default_graph(title, span)

    add_metric(ret, host, "%s.status.%s.count" % (metric_base, status), alias, scale=True)

    set_yaxis_labels(ret, "req/s")

    return ret


def grafana_panel_website_timing_total(host, metric_base, span=4):
    title = "Total request timings"
    ret = get_default_graph(title, span)

    add_metric(ret, host, '%s.total.duration.*' % (metric_base), [-1])

    connect_missing_points(ret)
    set_point_mode(ret)
    set_yaxis_units(ret, "ms")

    return ret


def grafana_panel_website_timing_per_status_group(host, metric_base, span=4):
    title = "q50 request timings per status group"
    ret = get_default_graph(title, span)

    add_metric(ret, host, '%s.status.1xx.duration.q50' % (metric_base), '1xx - Informational')
    add_metric(ret, host, '%s.status.2xx.duration.q50' % (metric_base), '2xx - Success')
    add_metric(ret, host, '%s.status.3xx.duration.q50' % (metric_base), '3xx - Redirection')
    add_metric(ret, host, '%s.status.4xx.duration.q50' % (metric_base), '4xx - Client error')
    add_metric(ret, host, '%s.status.5xx.duration.q50' % (metric_base), '5xx - Server error')
    add_metric(ret, host, '%s.status.unparsable.duration.q50' % (metric_base), 'Unparsable')

    connect_missing_points(ret)
    set_point_mode(ret)
    set_yaxis_units(ret, "ms")

    return ret


def grafana_panel_website_timing_per_method(host, metric_base, span=4):
    title = "q50 request timings per HTTP method"
    ret = get_default_graph(title, span)

    add_metric(ret, host, '%s.method.CONNECT.duration.q50' % (metric_base), [-3])
    add_metric(ret, host, '%s.method.DELETE.duration.q50' % (metric_base), [-3])
    add_metric(ret, host, '%s.method.GET.duration.q50' % (metric_base), [-3])
    add_metric(ret, host, '%s.method.HEAD.duration.q50' % (metric_base), [-3])
    add_metric(ret, host, '%s.method.OPTIONS.duration.q50' % (metric_base), [-3])
    add_metric(ret, host, '%s.method.POST.duration.q50' % (metric_base), [-3])
    add_metric(ret, host, '%s.method.PUT.duration.q50' % (metric_base), [-3])
    add_metric(ret, host, '%s.method.TRACE.duration.q50' % (metric_base), [-3])
    add_metric(ret, host, '%s.method.unparsable.duration.q50' % (metric_base), 'Unparsable')

    connect_missing_points(ret)
    set_point_mode(ret)
    set_yaxis_units(ret, "ms")

    return ret


def grafana_panel_website_timing_per_status(host, metric_base, status, alias, span=3):
    title = 'Status %s (%s)' % (status, alias)
    ret = get_default_graph(title, span)

    for p in [
            ['average', 'avg'],
            ['q01', 'q01'],
            ['q05', 'q05'],
            ['q50', 'q50'],
            ['q95', 'q95'],
            ['q99', 'q99'],
            ['unparsable', 'unp'],
            ]:
        add_metric(ret, host, '%s.status.%s.duration.%s' % (metric_base, status, p[0]), p[1])

    connect_missing_points(ret)
    set_point_mode(ret)
    set_yaxis_units(ret, "ms")

    return ret


def grafana_panel_website_timing_q50_per_status(host, metric_base, span=3):
    title = "q50 for all available statuses"
    ret = get_default_graph(title, span)

    add_metric(ret, host, '%s.status.*.duration.q50' % (metric_base), [-3])

    connect_missing_points(ret)
    set_point_mode(ret)
    set_yaxis_units(ret, "ms")

    return ret


def grafana_panel_website_timing_per_method_detailed(host, metric_base, method, alias=None, span=3):
    if not alias:
        alias = method
    title = 'Method %s' % (alias)
    ret = get_default_graph(title, span)

    for p in [
            ['average', 'avg'],
            ['q01', 'q01'],
            ['q05', 'q05'],
            ['q50', 'q50'],
            ['q95', 'q95'],
            ['q99', 'q99'],
            ['unparsable', 'unp'],
            ]:
        add_metric(ret, host, '%s.method.%s.duration.%s' % (metric_base, method, p[0]), p[1])

    connect_missing_points(ret)
    set_point_mode(ret)
    set_yaxis_units(ret, "ms")

    return ret


def grafana_panel_website_ssl(host, aspect, metric_base, span=4):
    title = 'SSL %ss' % (aspect)
    ret = get_default_graph(title, span)

    add_metric(ret, host, '%s.ssl.%s.*.count' % (metric_base, aspect.replace(' ', '_').lower()), alias=[8], scale=True)

    set_yaxis_labels(ret, "req/s")
    zero_missing_points(ret)

    return ret

def grafana_panel_website_total_requests(host, engine, span=4):
    title = "Total requests served"
    ret = get_default_graph(title, span)

    add_metric(ret, host, ['logs.%s.*.*.total.count' % (engine), 'logs.%s.*.total.count' % (engine)], 'Total requests', scale=True)
    add_metric(ret, host, 'logs.%s.*.*.total.count' % (engine), [-4, -3], scale=True)
    add_metric(ret, host, 'logs.%s.*.total.count' % (engine), [-3], scale=True)

    set_yaxis_labels(ret, "req/s")

    return ret


def grafana_panel_websites(host, websites, span=4):
    title = "Hosted websites"
    ret = get_default_text(title, span)

    set_content(ret, "\n".join([("* "+website) for website in websites]))

    return ret


def grafana_add_row_website_volume_kpi(dashboard, host, engine, website, aspect=None, repeated=False, collapse=True, add=True, title_prefix=None):
    span = 3
    title = '%s%s %s volume KPI' % (
        (title_prefix + ' ') if title_prefix else '',
        website,
        ' (' + aspect + ')' if aspect else '')
    row = get_default_row(title, host, repeated, collapse)
    metric_base = grafana_web_metric_base(engine, website, aspect)
    update_dict(row, {
            "panels": [
                grafana_panel_website_requests_total(host, metric_base, span=span),
                grafana_panel_website_requests_per_status_group(host, metric_base, span=span),
                grafana_panel_website_requests_per_method(host, metric_base, span=span),
                grafana_panel_website_requests_per_user(host, metric_base, span=span),
                ],
            })
    return add_row(dashboard, row) if add else dashboard


def grafana_add_row_website_status_details(dashboard, host, engine, website, aspect=None, repeated=False, collapse=True, add=True, title_prefix=None):
    span = 3
    title = '%s%s %s status details' % (
        (title_prefix + ' ') if title_prefix else '',
        website,
        ' (' + aspect + ')' if aspect else '')
    row = get_default_row(title, host, repeated, collapse)
    metric_base = grafana_web_metric_base(engine, website, aspect)
    update_dict(row, {
            "panels": [
                grafana_panel_website_requests_per_status(host, metric_base, '200', 'OK', span=span),
                grafana_panel_website_requests_per_status(host, metric_base, '206', 'Partial Content', span=span),
                grafana_panel_website_requests_per_status(host, metric_base, '301', 'Moved Permanently', span=span),
                grafana_panel_website_requests_per_status(host, metric_base, '302', 'Found', span=span),
                grafana_panel_website_requests_per_status(host, metric_base, '304', 'Not Modified', span=span),
                grafana_panel_website_requests_per_status(host, metric_base, '401', 'Unauthorized', span=span),
                grafana_panel_website_requests_per_status(host, metric_base, '404', 'Not Found', span=span),
                grafana_panel_website_requests_per_status(host, metric_base, '500', 'Internal Server Error', span=span),
                grafana_panel_website_requests_per_status(host, metric_base, '502', 'Bad Gateway', span=span),
                grafana_panel_website_requests_per_status(host, metric_base, '503', 'Service Unavailable', span=span),
                grafana_panel_website_requests_per_status(host, metric_base, '504', 'Gateway Timeout', span=span),
                grafana_panel_website_requests_per_status(host, metric_base, '*', None, span=span),
                ],
            })
    return add_row(dashboard, row) if add else dashboard


def grafana_add_row_website_ssl(dashboard, host, engine, website, aspect, repeated=False, collapse=True, add=True):
    span = 4
    title = '%s %s SSL' % (website, ' (' + aspect + ')' if aspect else '')
    row = get_default_row(title, host, repeated, collapse)
    metric_base = grafana_web_metric_base(engine, website, aspect)
    update_dict(row, {
            "panels": [
                grafana_panel_website_ssl(host, 'Protocol', metric_base, span=span),
                grafana_panel_website_ssl(host, 'Ciphersuite', metric_base, span=span),
                grafana_panel_website_ssl(host, 'Client Serial', metric_base, span=span),
                ],
            })
    return add_row(dashboard, row) if add else dashboard


def grafana_add_row_website_timing_kpi(dashboard, host, engine, website, aspect, repeated=False, collapse=True, add=True):
    span = 4
    title = '%s %s timing KPI' % (website, ' (' + aspect + ')' if aspect else '')
    row = get_default_row(title, host, repeated, collapse)
    metric_base = grafana_web_metric_base(engine, website, aspect)
    update_dict(row, {
            "panels": [
                grafana_panel_website_timing_total(host, metric_base, span=span),
                grafana_panel_website_timing_per_status_group(host, metric_base, span=span),
                grafana_panel_website_timing_per_method(host, metric_base, span=span),
                ],
            })
    return add_row(dashboard, row) if add else dashboard


def grafana_add_row_website_timing_status_details(dashboard, host, engine, website, aspect, repeated=False, collapse=True, add=True):
    span = 3
    title = '%s %s timing status details' % (website, ' (' + aspect + ')' if aspect else '')
    row = get_default_row(title, host, repeated, collapse)
    metric_base = grafana_web_metric_base(engine, website, aspect)
    update_dict(row, {
            "panels": [
                grafana_panel_website_timing_per_status(host, metric_base, '200', 'OK', span=span),
                grafana_panel_website_timing_per_status(host, metric_base, '206', 'Partial Content', span=span),
                grafana_panel_website_timing_per_status(host, metric_base, '301', 'Moved Permanently', span=span),
                grafana_panel_website_timing_per_status(host, metric_base, '302', 'Found', span=span),
                grafana_panel_website_timing_per_status(host, metric_base, '304', 'Not Modified', span=span),
                grafana_panel_website_timing_per_status(host, metric_base, '401', 'Unauthorized', span=span),
                grafana_panel_website_timing_per_status(host, metric_base, '404', 'Not Found', span=span),
                grafana_panel_website_timing_per_status(host, metric_base, '500', 'Internal Server Error', span=span),
                grafana_panel_website_timing_per_status(host, metric_base, '502', 'Bad Gateway', span=span),
                grafana_panel_website_timing_per_status(host, metric_base, '503', 'Service Unavailable', span=span),
                grafana_panel_website_timing_per_status(host, metric_base, '504', 'Gateway Timeout', span=span),
                grafana_panel_website_timing_q50_per_status(host, metric_base, span=span),
                ],
            })
    return add_row(dashboard, row) if add else dashboard


def grafana_add_row_website_timing_method_details(dashboard, host, engine, website, aspect, repeated=False, collapse=True, add=True):
    span = 3
    title = '%s %s timing method details' % (website, ' (' + aspect + ')' if aspect else '')
    row = get_default_row(title, host, repeated, collapse)
    metric_base = grafana_web_metric_base(engine, website, aspect)
    update_dict(row, {
            "panels": [
                grafana_panel_website_timing_per_method_detailed(host, metric_base, 'CONNECT', span=span),
                grafana_panel_website_timing_per_method_detailed(host, metric_base, 'DELETE', span=span),
                grafana_panel_website_timing_per_method_detailed(host, metric_base, 'GET', span=span),
                grafana_panel_website_timing_per_method_detailed(host, metric_base, 'HEAD', span=span),
                grafana_panel_website_timing_per_method_detailed(host, metric_base, 'OPTIONS', span=span),
                grafana_panel_website_timing_per_method_detailed(host, metric_base, 'POST', span=span),
                grafana_panel_website_timing_per_method_detailed(host, metric_base, 'PUT', span=span),
                grafana_panel_website_timing_per_method_detailed(host, metric_base, 'TRACE', span=span),
                grafana_panel_website_timing_per_method_detailed(host, metric_base, 'unparsable', 'Unparsable', span=span),
                ],
            })
    return add_row(dashboard, row) if add else dashboard


def grafana_add_rows_website(dashboard, host, engine, website, aspect=None, timing=True, repeated=False, collapse=True, ssl=False):
    dashboard = grafana_add_row_website_volume_kpi(dashboard, host, engine, website, aspect, repeated=repeated, collapse=collapse)
    dashboard = grafana_add_row_website_status_details(dashboard, host, engine, website, aspect, repeated=repeated, collapse=collapse)
    if ssl:
        dashboard = grafana_add_row_website_ssl(dashboard, host, engine, website, aspect, repeated=repeated, collapse=collapse)
    if timing:
        dashboard = grafana_add_row_website_timing_kpi(dashboard, host, engine, website, aspect, repeated=repeated, collapse=collapse)
        dashboard = grafana_add_row_website_timing_status_details(dashboard, host, engine, website, aspect, repeated=repeated, collapse=collapse)
        dashboard = grafana_add_row_website_timing_method_details(dashboard, host, engine, website, aspect, repeated=repeated, collapse=collapse)
    return dashboard


class FilterModule(object):
    '''Ansible jinja2 filters for grafana apache graphs'''

    def filters(self):
        return {}

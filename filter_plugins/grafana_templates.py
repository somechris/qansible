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

import json
import copy
import re

# timepicker.time_options are not picked up by Grafana. The seem to be
# hard-coded in the version we use. But Grafana examples configure
# that setting. So we follow that lead. Hopefully it will get picked
# up in future versions.
default_dashboard = {
    "editable": False,
    "gnetId": None,
    "links": [],
    "originalTitle": "untitled",
    "rows": [],
    "schemaVersion": 12,
    "sharedCrosshair": True,
    "style": "dark",
    "tags": [],
    "timezone": "utc",
    "timepicker": {
        "enable": True,
        "time_options": [
            "5m",
            "15m",
            "30m",
            "1h",
            "3h",
            "6h",
            "12h",
            "24h",
            "2d",
            "7d",
            "30d",
            "60d",
            "90d",
            "1y",
            "2y",
            "5y",
            ],
        "refresh_intervals": [
            "1m",
            "5m",
            "15m",
            "30m",
            "1h",
            "2h",
            "1d",
            ],
        },
    "title": "untitled",
    "version": 0,
    }


def dump_json(obj):
    """Format an object as json string

    Parameters
    ----------
    obj: Any type accepted by json.dump

    Return
    ------
    string: the formatted JSON string
    """
    return json.dumps(obj, indent=4, sort_keys=True)


def explode_ec2_tag(tag):
    return ['reg:' + tag[4:-1], 'az:' + tag[-1:]]


def param_to_template_value(param):
    text = param
    if param == 'All':
        value = '$__all'
    else:
        value = param
    return {
        "text": text,
        "value": value,
        }


def grafana_web_metric_base(engine, website, aspect):
    website = website.replace('.', '_').replace('-', '_')
    aspect = ('.' + aspect if aspect else '')
    return 'logs.%s.%s%s' % (engine, website, aspect)


def set_default_period(obj, period):
    """Sets default time period for metrics in dashboards"""
    obj["time"] = {
        "from": "now-" + period,
        "to": "now"
        }


def grafana_init_dashboard(jinja_param, title='Dashboard', tags=[],
                           templates=[], default_period=None):
    """Initialized a Grafana dashboard

    Parameters
    ----------
    jinja_param: anything
      ignored
    title: string
      The title for the dashboard
    tags: list of strings
      The tags for the dashboard
    default_period: string
      The default time period to show metrics for (E.g.: '30d')

    Return
    ------
    object: The dashboard definition
    """

    extension = []
    for tag in tags:
        # In order to allow better selection of different aspects
        # directly from the inventory, the inventory attaches the
        # groups 'ec2', 'ec2-us-west-2', 'ec2-us-west-2a' for a host
        # in the 'ec2-us-west-2a' availability zone. Showing all those
        # tags in Grafana make the tag list really long and cover up
        # part of the host name. Hence, we look for the full length
        # tag (E.g.: 'ec2-us-west-2a' and explode it into 'ec2',
        # 'reg:us-west-2', 'az:a' tags. Thereby, the tag list does not
        # need that much space any longer, and we can still drill down
        # along different ec2 dimensions.
        if tag.startswith('ec2-') and tag[-3] == '-':
            # We've found a full ec2 tag. Explode it!
            extension.extend(explode_ec2_tag(tag))

        # Extract more dense tags for websites:
        if tag.startswith('website_') and tag.endswith('_server'):
            extension.extend([tag[8:-7]])
    tags += extension

    # Filter out tags that we're not interested in. That's ec2 inventory groups and some hand picked
    tags = [tag for tag in tags if not tag.startswith('ec2-') and
            not tag.startswith('website_') and
            tag not in [
                'aws1',              # Unneeded, as all hosts should have it
                'jmxtrans',          # Unneeded, as it is just a helper application
                'ldap-servers',      # Unneeded, as it is only one right now
                'rted-api',          # Unneeded, as we have tag with domain anyways
                'reprepro-servers',  # Unneeded, as it is only one right now
                ]]

    dashboard = copy.deepcopy(default_dashboard)
    dashboard['title'] = title
    dashboard['originalTitle'] = title
    dashboard['tags'] = sorted(tags)

    if default_period is not None:
        set_default_period(dashboard, default_period)

    if templates:
        dashboard['templating'] = {
            "list": []
            }
    for template in templates:
        if isinstance(template, dict):
            values = template.get('values', [])
            if values:
                if template.get('name') == 'host':
                    values = [value.split('.', 2)[0] for value in values]
                values = ['All'] + values
                current = values[1]
            else:
                current = '<empty>'

            dashboard['templating']['list'].append(
                {
                    "current": param_to_template_value(current),
                    "hideLabel": (template.get("label", None) is None),
                    "includeAll": True,
                    "label": template.get("label", "Label"),
                    "multi": True,
                    "name": template.get("name"),
                    "options": [param_to_template_value(value) for value in values],
                    "query": ",".join(values),
                    "refresh": 0,
                    "regex": "",
                    "tags": [],
                    "type": "custom",
                    "useTags": False,
                    }
                )
        elif template == 'host':
            dashboard['templating']['list'].append(
                {
                    "current": param_to_template_value('All'),
                    "includeAll": True,
                    "label": "Hosts",
                    "multi": True,
                    "name": "host",
                    "options": [],
                    "query": "hosts.*",
                    "refresh": 1,
                    "regex": "",
                    "tags": [],
                    "type": "query",
                    "useTags": False,
                    }
                )

    return dashboard


def grafana_dump_dashboard(dashboard):
    """Turns a dashboard object into a string

    Parameters
    ----------
    dashboard: object
      The aggregated dashboard definition

    Return
    ------
    string: the formatted dashboard configuration
    """
    return dump_json(dashboard)


def grafana_add_rows_apache(dashboard, host, websites, add=True, repeated=False, collapse=True, fallback_sites=True):
    if add:
        dashboard = grafana_add_row_apache(dashboard, host, websites, repeated=repeated, collapse=collapse)
        for website in sorted(websites):
            dashboard = grafana_add_rows_website(dashboard, host, 'apache', website, 'https', repeated=repeated, collapse=collapse, ssl=True)
            dashboard = grafana_add_rows_website(dashboard, host, 'apache', website, 'http', repeated=repeated, collapse=collapse)
        if fallback_sites:
            dashboard = grafana_add_rows_website(dashboard, host, 'apache', 'other_vhosts', timing=False, repeated=repeated, collapse=collapse)
            dashboard = grafana_add_rows_website(dashboard, host, 'apache', 'fallback', timing=False, repeated=repeated, collapse=collapse)
    return dashboard


def grafana_add_rows_nginx(dashboard, host, websites, add=True, repeated=False, collapse=True, fallback_sites=True):
    if add:
        dashboard = grafana_add_row_nginx(dashboard, host, websites, repeated=repeated, collapse=collapse)
        for website in sorted(websites):
            dashboard = grafana_add_rows_website(dashboard, host, 'nginx', website, 'http', repeated=repeated, collapse=collapse)
            dashboard = grafana_add_rows_website(dashboard, host, 'nginx', website, 'https', repeated=repeated, collapse=collapse, ssl=True)
        if fallback_sites:
            dashboard = grafana_add_rows_website(dashboard, host, 'nginx', 'localhost', timing=False, repeated=repeated, collapse=collapse)
            dashboard = grafana_add_rows_website(dashboard, host, 'nginx', 'fallback', timing=False, repeated=repeated, collapse=collapse)
    return dashboard


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


def grafana_add_row_time(dashboard, host, repeated=False, collapse=True):
    span = 3
    title = 'Time'
    row = get_default_row(title, host, repeated, collapse)
    update_dict(row, {
            "panels": [
                grafana_panel_time_sync(host, span=span),
                grafana_panel_time_kind(host, span=span),
                grafana_panel_time_status(host, span=span),
                grafana_panel_time_difference(host, span=span),
                ],
            })
    return add_row(dashboard, row)


def grafana_add_row_graphite(dashboard, host, add=True, repeated=False, collapse=True):
    span = 4
    title = 'Graphite'
    row = get_default_row(title, host, repeated, collapse)
    update_dict(row, {
            "panels": [
                grafana_panel_graphite_cache(host, span=span),
                grafana_panel_graphite_updates(host, span=span),
                grafana_panel_graphite_monitors(host, span=span),
                ],
            })
    return add_row(dashboard, row) if add else dashboard

def grafana_add_row_apache(dashboard, host, websites, add=True, collapse=True, repeated=False):
    span = 4
    title = "Apache"
    row = get_default_row(title, host, repeated, collapse)
    update_dict(row, {
            "panels": [
                grafana_panel_apache_workers_basic(host),
                grafana_panel_apache_troughput(host),
                grafana_panel_apache_connections(host),
                grafana_panel_apache_scorecard(host),
                grafana_panel_website_total_requests(host, 'apache', span=span),
                grafana_panel_websites(host, websites),
                ],
            })
    return add_row(dashboard, row) if add else dashboard


def grafana_add_row_nginx(dashboard, host, websites, add=True, collapse=True, repeated=False):
    span = 4
    title = "Nginx"
    row = get_default_row(title, host, repeated, collapse)
    update_dict(row, {
            "panels": [
                grafana_panel_nginx_workers_basic(host),
                grafana_panel_nginx_connections(host),
                grafana_panel_nginx_requests(host),
                grafana_panel_nginx_workers_detailed(host),
                grafana_panel_website_total_requests(host, 'nginx', span=span),
                grafana_panel_websites(host, websites),
                ],
            })
    return add_row(dashboard, row) if add else dashboard


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


def grafana_panel_time_sync(host, span=3):
    title = "Synchronization"
    ret = get_default_graph(title, span)

    add_metric(ret, host, 'time.synchronized', 'Synchronized')
    add_metric(ret, host, 'time.stratum', 'Stratum')

    return ret


def grafana_panel_time_kind(host, span=3):
    title = "Kinds"
    ret = get_default_graph(title, span)

    add_metric(ret, host, 'time.kind.*')

    return ret


def grafana_panel_time_status(host, span=3):
    title = "Statuses"
    ret = get_default_graph(title, span)

    add_metric(ret, host, 'time.status.*')

    return ret


def grafana_panel_time_difference(host, span=3):
    title = "Time difference"
    ret = get_default_graph(title, span)

    add_metric(ret, host, 'time.difference.*')

    set_yaxis_minimum(ret, 'left', None)
    set_yaxis_units(ret, left='s')

    return ret


def grafana_panel_graphite_cache(host, span=4):
    title = "Cache"
    ret = get_default_graph(title, span)

    add_metric(ret, host, "graphite.carbon.agents.*.cache.queries")
    add_metric(ret, host, "graphite.carbon.agents.*.cache.queues")

    return ret


def grafana_panel_graphite_updates(host, span=4):
    title = "Updates"
    ret = get_default_graph(title, span)

    add_metric(ret, host, "graphite.carbon.agents.*.metricsReceived")
    add_metric(ret, host, "graphite.carbon.agents.*.committedPoints")
    add_metric(ret, host, "graphite.carbon.agents.*.updateOperations")

    return ret


def grafana_panel_graphite_monitors(host, span=4):
    title = "Monitors"
    ret = get_default_graph(title, span)

    add_metric(ret, host, "graphite.carbon.agents.*.creates")
    add_metric(ret, host, "graphite.carbon.agents.*.errors")

    return ret


def grafana_panel_apache_troughput(host, span=4):
    title = "Accesses"
    ret = get_default_graph(title, span)

    add_metric(ret, host, 'apache.localhost.TotalAccesses', 'Accesses', scale=True, nnder=True)
    # 17.06666 = 1024/60
    add_metric(ret, host, 'apache.localhost.TotalkBytes', 'Bytes', scale=(1024./60), nnder=True)

    set_yaxis_units(ret, right="Bps")
    switch_to_right_axis(ret, "Bytes")

    return ret


def grafana_panel_website_total_requests(host, engine, span=4):
    title = "Total requests served"
    ret = get_default_graph(title, span)

    add_metric(ret, host, ['logs.%s.*.*.total.count' % (engine), 'logs.%s.*.total.count' % (engine)], 'Total requests', scale=True)
    add_metric(ret, host, 'logs.%s.*.*.total.count' % (engine), [-4, -3], scale=True)
    add_metric(ret, host, 'logs.%s.*.total.count' % (engine), [-3], scale=True)

    set_yaxis_labels(ret, "req/s")

    return ret


def grafana_panel_apache_workers_basic(host, span=4):
    title = "Workers (basic)"
    ret = get_default_graph(title, span)

    add_metric(ret, host, 'apache.localhost.BusyWorkers', 'Busy')
    add_metric(ret, host, 'apache.localhost.IdleWorkers', 'Idle')

    set_stacked_mode(ret)

    return ret


def grafana_panel_apache_connections(host, span=4):
    title = "Connections"
    ret = get_default_graph(title, span)

    add_metric(ret, host, 'apache.localhost.ConnsTotal', 'Total')
    add_metric(ret, host, 'apache.localhost.ConnsAsyncClosing', 'Async Closing')
    add_metric(ret, host, 'apache.localhost.ConnsAsyncKeepAlive', 'Async Keep-Alive')
    add_metric(ret, host, 'apache.localhost.ConnsAsyncWriting', 'Async Writing')

    return ret


def grafana_panel_apache_scorecard(host, span=4):
    title = "Workers (detailed)"
    ret = get_default_graph(title, span)

    add_metric(ret, host, 'apache.localhost.IdleWorkers', 'Idle')
    add_metric(ret, host, 'apache.localhost.StartingWorkers', 'Starting')
    add_metric(ret, host, 'apache.localhost.ReadingWorkers', 'Reading')
    add_metric(ret, host, 'apache.localhost.WritingWorkers', 'Writing')
    add_metric(ret, host, 'apache.localhost.KeepaliveWorkers', 'Keep-Alive')
    add_metric(ret, host, 'apache.localhost.DnsWorkers', 'Dns')
    add_metric(ret, host, 'apache.localhost.ClosingWorkers', 'Closing')
    add_metric(ret, host, 'apache.localhost.LoggingWorkers', 'Logging')
    add_metric(ret, host, 'apache.localhost.FinishingWorkers', 'Finishing')
    add_metric(ret, host, 'apache.localhost.CleanupWorkers', 'Cleanup')
    add_metric(ret, host, 'apache.localhost.EmptyWorkerSlots', 'Empty')

    set_stacked_mode(ret)

    return ret


def grafana_panel_websites(host, websites, span=4):
    title = "Hosted websites"
    ret = get_default_text(title, span)

    set_content(ret, "\n".join([("* "+website) for website in websites]))

    return ret


def grafana_panel_nginx_workers_basic(host, span=4):
    title = "Workers (basic)"
    ret = get_default_graph(title, span)

    add_metric(ret, host, ['nginx.act_reads', 'nginx.act_writes'], 'Busy')
    add_metric(ret, host, 'nginx.act_waits', 'Idle')

    set_stacked_mode(ret)

    return ret


def grafana_panel_nginx_connections(host, span=4):
    title = "Connections"
    ret = get_default_graph(title, span)

    add_metric(ret, host, 'nginx.active_connections', 'Active connections')
    add_metric(ret, host, 'nginx.conn_accepted', 'Accepted connections')
    add_metric(ret, host, 'nginx.conn_handled', 'Handled connections')

    return ret


def grafana_panel_nginx_requests(host, span=4):
    title = "Requests"
    ret = get_default_graph(title, span)

    add_metric(ret, host, 'nginx.req_handled', 'Handled requests')
    add_metric(ret, host, 'nginx.req_per_conn', 'Requests per connection')

    switch_to_right_axis(ret, "Requests per connection")

    return ret


def grafana_panel_nginx_workers_detailed(host, span=4):
    title = "Workers (detailed)"
    ret = get_default_graph(title, span)

    add_metric(ret, host, 'nginx.act_waits', 'Idle')
    add_metric(ret, host, 'nginx.act_reads', 'Reading')
    add_metric(ret, host, 'nginx.act_writes', 'Writing')

    set_stacked_mode(ret)

    return ret


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



FILTERS = {
    'grafana_create_dashboard': grafana_init_dashboard,
    'grafana_dump_dashboard': grafana_dump_dashboard,
    'grafana_add_rows_apache': grafana_add_rows_apache,
    'grafana_add_rows_nginx': grafana_add_rows_nginx,
    'grafana_add_rows_website': grafana_add_rows_website,
    'grafana_add_row_time': grafana_add_row_time,
    'grafana_add_row_graphite': grafana_add_row_graphite,
    'grafana_add_row_apache': grafana_add_row_apache,
    'grafana_add_row_nginx': grafana_add_row_nginx,
    }


class FilterModule(object):
    '''Ansible jinja2 filter for hashing strings to numbers and mod-ing them'''

    def filters(self):
        return FILTERS

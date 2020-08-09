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
from grafana_websites import grafana_add_rows_website
from grafana_websites import grafana_panel_website_total_requests
from grafana_websites import grafana_panel_websites
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





FILTERS = {
    'grafana_create_dashboard': grafana_init_dashboard,
    'grafana_dump_dashboard': grafana_dump_dashboard,
    'grafana_add_rows_nginx': grafana_add_rows_nginx,
    'grafana_add_row_time': grafana_add_row_time,
    'grafana_add_row_nginx': grafana_add_row_nginx,
    }


class FilterModule(object):
    '''Ansible jinja2 filter for hashing strings to numbers and mod-ing them'''

    def filters(self):
        return FILTERS

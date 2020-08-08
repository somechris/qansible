# -*- coding: utf-8 -*-

import json
import copy
import collections
import re

MAX_CPU=900

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
PANELS = 0
default_panel = {
}
default_yaxis = {
    "format": "short",
    "label": None,
    "logBase": 1,
    "max": None,
    "min": 0,
    "show": True
}
default_graph = {
    "type": "graph",
    "nullPointMode": "null",
    "targets": [],
    "tooltip": {
        "value_type": "individual",
        },
    "yaxes": [
        copy.deepcopy(default_yaxis),
        copy.deepcopy(default_yaxis),
        ]
}
default_text = {
    "type": "text",
    "editable": False,
    "mode": "markdown",
}
default_row = {
    "editable": False,
    "showTitle": True,
    "height": "250px",
    "collapse": True,
}

RETENTION_DAY_RESOLUTION = '20y'
RETENTION_HOUR_RESOLUTION = '1y'
RETENTION_MINUTE_RESOLUTION = '10d'
RETENTION_HOUR_RESOLUTION_LONG = '5y'
RETENTION_MINUTE_RESOLUTION_LONG = '60d'


def resolve_retention(retention):
    ret = retention
    if isinstance(retention, list):
        lst = [resolve_retention(item) for item in retention]
        ret = ','.join(lst)
    elif retention == 'min':
        ret = '1m:%s' % (RETENTION_MINUTE_RESOLUTION)
    elif retention == 'min_long':
        ret = '1m:%s' % (RETENTION_MINUTE_RESOLUTION_LONG)
    elif retention == 'hour':
        ret = '1h:%s' % (RETENTION_HOUR_RESOLUTION)
    elif retention == 'hour_long':
        ret = '1h:%s' % (RETENTION_HOUR_RESOLUTION_LONG)
    elif retention == 'day':
        ret = '1d:%s' % (RETENTION_DAY_RESOLUTION)
    return ret


METRIC_RETENTIONS = [
    {
        'name': 'daily',
        'match': '.*per.day.*',
        'retentions': resolve_retention(['day']),
    },
    {
        'name': 'daily_weekday',
        'match': '.*per.weekday.*',
        'retentions': resolve_retention(['day']),
    },
    {
        'name': 'hourly',
        'match': '.*per.hour.*',
        'retentions': resolve_retention(['hour', 'day']),
    },
    {
        'name': 'temporary_ec2ohndp06',
        'comment': '2017-09-27 Temporary increase for ec2ohndp06 to allow Andy to test outlier detection (see 2017-09-06 email)',
        'match': '.*hosts.ec2ohndp06.*',
        'retentions': resolve_retention(['min_long', 'hour_long', 'day']),
    },
    {
        'name': 'temporary_ec2vconp01',
        'comment': '2017-09-27 Temporary increase for ec2vconp01 to allow Andy to test outlier detection (see 2017-09-06 email)',
        'match': '.*hosts.ec2vconp01.*',
        'retentions': resolve_retention(['min_long', 'hour_long', 'day']),
    },
    {
        'name': 'temporary_ec2vmosp01',
        'comment': '2017-09-27 Temporary increase for ec2vmosp01 to allow Andy to test outlier detection (see 2017-09-06 email)',
        'match': '.*hosts.ec2vmosp01.*',
        'retentions': resolve_retention(['min_long', 'hour_long', 'day']),
    },
    {
        'name': 'default_1min_for_1day',
        'match': '.*',
        'retentions': resolve_retention(['min', 'hour', 'day']),
    },
]


def get_metric_retentions(dummy=''):
    return METRIC_RETENTIONS


def retention_key(retention):
    retention = normalize_period(retention)
    key = '0%s' % (retention)
    if retention == '1min':
        key = '3'
    elif retention == '1h':
        key = '2'
    elif retention == '1d':
        key = '1'
    else:
        raise RuntimeError('Unknown retention "%s"' % (retention))
    return key


def get_metric_resolution(host=None, metric=None, kind='hosts'):
    ret = 'unknown'
    if host:
        metric_list = get_metric_list(host=host, metric=metric, kind=kind)
        ret = get_metric_resolution(metric=metric_list)
    elif isinstance(metric, list):
        ret = set([get_metric_resolution(metric=item) for item in metric])
        ret = [item for item in ret]
        ret.sort(key=retention_key)
        if len(ret) == 1:
            ret = ret[0]
    else:
        for retention in METRIC_RETENTIONS:
            if re.compile(retention['match']).match(metric):
                ret = retention['retentions'].split(',')[0].split(':')[0]
                break
    return normalize_period(ret)


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


def update_dict(target, source):
    for key, value in source.iteritems():
        if isinstance(value, collections.Mapping):
            repl = update_dict(target.get(key, {}), value)
            target[key] = repl
        else:
            target[key] = source[key]
    return target


def get_default_panel(title, span):
    global PANELS
    PANELS += 1
    ret = copy.deepcopy(default_panel)
    ret["id"] = PANELS
    ret['title'] = title
    ret['span'] = span
    return ret


def get_default_graph(title, span):
    ret = get_default_panel(title, span)
    ret.update(copy.deepcopy(default_graph))
    return ret


def set_content(obj, content):
    obj["content"] = content


def get_default_text(title, span):
    ret = get_default_panel(title, span)
    ret.update(copy.deepcopy(default_text))
    return ret


def get_default_row(title, host, repeated, collapse):
    ret = copy.deepcopy(default_row)
    if repeated:
        title += " (" + host + ")"
        ret['repeat'] = repeated
    ret['title'] = title
    ret['collapse'] = collapse
    return ret


def set_yaxis_helper(obj, axis, key, value):
    if axis == 'left':
        axis_idx = 0
    else:
        axis_idx = 1
    obj['yaxes'][axis_idx][key] = value


def set_yaxis_units(obj, left='short', right='short'):
    key = 'format'
    set_yaxis_helper(obj, 'left', key, left)
    set_yaxis_helper(obj, 'right', key, right)


def set_yaxis_labels(obj, left, right=None):
    key = 'label'
    set_yaxis_helper(obj, 'left', key, left)
    if right:
        set_yaxis_helper(obj, 'right', key, right)


def set_yaxis_minimum(obj, axis, value):
    set_yaxis_helper(obj, axis, 'min', value)


def set_yaxis_maximum(obj, axis, value):
    set_yaxis_helper(obj, axis, 'max', value)


def set_fill(obj, fill):
    obj["fill"] = fill


def set_stacked_mode(obj):
    obj["stack"] = True
    # Translucent stacked graphs are misleading. Hence we down down
    # translucency.
    set_fill(obj, 8)


def set_colors(obj, colors):
    obj["aliasColors"] = colors


def set_point_mode(obj):
    obj["points"] = True
    obj["pointradius"] = 0.5


def add_series_override(obj, alias, override):
    if "seriesOverrides" not in obj:
        obj["seriesOverrides"] = []

    override_obj = {
        "alias": alias,
        }

    for k, v in override.iteritems():
        override_obj[k] = v

    obj["seriesOverrides"].append(override_obj)


def switch_to_right_axis(obj, alias):
    add_series_override(obj, alias, {"yaxis": 2})


def connect_missing_points(obj):
    obj["nullPointMode"] = "connected"


def zero_missing_points(obj):
    obj["nullPointMode"] = "null as zero"


def set_decimals(obj, decimals):
    obj["decimals"] = decimals


def set_default_period(obj, period):
    """Sets default time period for metrics in dashboards"""
    obj["time"] = {
        "from": "now-" + period,
        "to": "now"
        }


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


def add_row(dashboard, row):
    if not isinstance(dashboard, dict):
        dashboard = {}
    if 'rows' not in dashboard:
        dashboard['rows'] = []
    dashboard['rows'].append(row)
    return dashboard


def grafana_add_row_overview(dashboard, host, cpu_count=False, repeated=False, collapse=True):
    global default_row
    span = 3
    title = 'Performance Characteristics'
    row = get_default_row(title, host, repeated, collapse)
    update_dict(row, {
            "panels": [
                grafana_panel_load(host, span=span, cpu_count=cpu_count),
                grafana_panel_cpu(host, span=span),
                grafana_panel_memory(host, span=span),
                grafana_panel_network_bytes(host, span=span, title='Network'),
                ],
            })
    return add_row(dashboard, row)


def grafana_add_row_cpu(dashboard, host, repeated=False, collapse=True):
    global default_row
    span = 3
    title = 'CPU'
    row = get_default_row(title, host, repeated, collapse)
    update_dict(row, {
            "panels": [
                grafana_panel_cpu_kind(host, 'user', '#7EB26D', span=span),
                grafana_panel_cpu_kind(host, 'nice', '#EAB839', span=span),
                grafana_panel_cpu_kind(host, 'system', '#6ED0E0', span=span),
                grafana_panel_cpu_kind(host, 'iowait', '#BA43A9', span=span),
                grafana_panel_cpu_kind(host, 'irq', '#E24D42', span=span),
                grafana_panel_cpu_kind(host, 'softirq', '#1F78C1', span=span),
                grafana_panel_cpu_kind(host, 'steal', '#0A50A1', span=span),
                grafana_panel_cpu_kind(host, 'idle', '#3F2B5B', span=span),
                ],
            })
    return add_row(dashboard, row)


def grafana_add_row_memory(dashboard, host, repeated=False, collapse=True):
    global default_row
    span = 3
    title = 'Memory'
    row = get_default_row(title, host, repeated, collapse)
    update_dict(row, {
            "panels": [
                grafana_panel_memory_kind(host, 'used', span=span),
                grafana_panel_memory_kind(host, 'Buffers', color='#1F78C1', span=span),
                grafana_panel_memory_kind(host, 'Cached', color='#0A50A1', span=span),
                grafana_panel_memory_kind(host, 'MemFree', label='Free', color='#3F2B5B', span=span),
                ],
            })
    return add_row(dashboard, row)


def grafana_add_row_load(dashboard, host, cpu_count=False, repeated=False, collapse=True):
    global default_row
    span = 4
    title = 'Load'
    row = get_default_row(title, host, repeated, collapse)
    update_dict(row, {
            "panels": [
                grafana_panel_load_01(host, span=span, cpu_count=cpu_count),
                grafana_panel_load_05(host, span=span, cpu_count=cpu_count),
                grafana_panel_load_15(host, span=span, cpu_count=cpu_count),
                ],
            })
    return add_row(dashboard, row)


def grafana_add_row_host_metadata(dashboard, host, hostvars, repeated=False, collapse=True):
    global default_row
    span = 12
    title = 'Metadata'
    row = get_default_row(title, host, repeated, collapse)
    update_dict(row, {
            "panels": [
                grafana_panel_host_metadata(host, hostvars, span=span),
                ],
            })
    return add_row(dashboard, row)


def grafana_add_row_processes(dashboard, host, repeated=False, collapse=True):
    global default_row
    span = 4
    title = 'Processes'
    row = get_default_row(title, host, repeated, collapse)
    update_dict(row, {
            "panels": [
                grafana_panel_processes_running(host, span=span),
                grafana_panel_processes_total(host, span=span),
                grafana_panel_processes_both(host, span=span),
                ],
            })
    return add_row(dashboard, row)


def grafana_add_row_disk(dashboard, host, repeated=False, collapse=True):
    global default_row
    span = 4
    title = 'Disk I/O'
    row = get_default_row(title, host, repeated, collapse)
    update_dict(row, {
            "panels": [
                grafana_panel_diskspace_bytes(host, span=span),
                grafana_panel_diskspace_percent(host, span=span),
                grafana_panel_iostat_queue_length(host, span=span),
                grafana_panel_iostat_iops(host, span=span),
                grafana_panel_iostat_throughput(host, span=span),
                grafana_panel_iostat_waiting(host, span=span),
                ],
            })
    return add_row(dashboard, row)


def grafana_add_row_network(dashboard, host, repeated=False, collapse=True):
    global default_row
    span = 4
    title = 'Network'
    row = get_default_row(title, host, repeated, collapse)
    update_dict(row, {
            "panels": [
                grafana_panel_network_bytes(host, span=span),
                grafana_panel_network_packets(host, span=span),
                grafana_panel_network_drop_and_errors(host, span=span),
                ],
            })
    return add_row(dashboard, row)


def grafana_add_row_time(dashboard, host, repeated=False, collapse=True):
    global default_row
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
    global default_row
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
    global default_row
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
    global default_row
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
    global default_row
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
    global default_row
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
    global default_row
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
    global default_row
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
    global default_row
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
    global default_row
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


def add_metric_raw(obj, metric, visible=True):
    obj['targets'].append(
        {
            "target": metric,
            "hide": (not visible),
            }
        )


def normalize_period(summarize):
    ret = summarize
    if ret == 'minute' or ret == 'minutely' or ret == '1m':
        ret = '1min'
    elif ret == 'hour' or ret == 'hourly':
        ret = '1h'
    elif ret == 'day' or ret == 'daily':
        ret = '1d'
    elif not ret:
        ret = None
    return ret


def get_metric_list(host, metric, kind='hosts'):
    if isinstance(metric, list):
        metric_list = [(single_metric if single_metric.startswith('#')
                       else '%s.%s.%s' % (kind, host, single_metric))
                       for single_metric in metric]
    else:
        metric = '%s.%s.%s' % (kind, host, metric)
        metric_list = [metric]

    return metric_list


def grafana_format_metric(host, metric, alias=None, scale=False, nnder=False, der=False, visible=True, sum='sum', kind='hosts', keepLastValue=True, timeShift=None, summarize=None):
    """Add a metric to a panel

    Parameters
    ----------
    host: string
      the name of the host to get this metric for
    scale: bool or float
      (Default: False)
      If True, the series gets scaled by 1/60 (i.e.: minute to second
        conversion).
      If False, the series does not get scaled.
      If a float, the series gets scaled by that factor
    metric: string, list
      If string, the metric to add (without the leading 'hosts.<hostname>.'.
      If list, the metrics (each without the leading 'hosts.<hostname>.')
        that should get summed (of diffed; see 'sum' parameter).
    alias: None, string, list, dict
      (Default: None)
      If empty, the metric is aliased by 'aliasByMetric'.
      If a string, the metric is aliased by this string
      If a list, the metric is aliased by aliasByNode with this list as
        parameter.
      If a dict, and its 'kind' key is 'sub', then the metric is aliased by
        'aliasSub'. The value at 'match' is used as match, the value at
        'replacement' is used as replacement.
    nnder: bool
      (Default: False)
      If True, the non-negative derivative of the metric gets added instead
      of the metric itself.
    der: bool
      (Default: False)
      If True, the derivative of the metric gets added instead of the
      metric itself. Most of the time, you want the non-negative
      derivative. See the nnder parameter.
    sum: string
      (Default: sum)
      This parameter sets how metrics are aggregated, if the metrics
      parameter is a list. 'sum' means that the series get summed, 'diff'
      means that the series get diffed. 'divide' means that the series
      get divided to compute a ratio.
    kind: string
      (Default: 'hosts')
      The kind of metric. Use 'hosts' for host metrics and 'services'
      for service metrics.
    keepLastValue: boolean
      (Default: True)
      If true, apply keepLastValue to derivatives. That way, holes in
      the data are smoothed over and lines are not broken.
    timeShift: string
      (Default: None)
      If not none, shift metric by this value
    summarize: string
      (Default: None)
      If not None, summarize metrics to this time interval

    Return
    ------
    string
      name of the formatted graphite metric
    """
    metric_list = get_metric_list(host, metric, kind)
    if isinstance(metric, list):
        metric = '%sSeries(%s)' % (sum, ",".join(metric_list))
    else:
        metric = metric_list[0]

    if scale:
        if scale is True:
            metric = 'scale(%s, 0.016666666)' % (metric)
        else:
            metric = 'scale(%s, %f)' % (metric, scale)

    if summarize is not None:
        default_resolution = get_metric_resolution(metric=metric_list)
        if summarize != default_resolution:
            metric = 'summarize(%s, "%s")' % (metric, summarize)
    if (nnder or der) and keepLastValue:
        metric = 'keepLastValue(%s)' % (metric)
    if nnder:
        metric = 'nonNegativeDerivative(%s)' % (metric)
    if der:
        metric = 'derivative(%s)' % (metric)
    if timeShift:
        metric = 'timeShift(%s, "%s")' % (metric, timeShift)

    if alias:
        if isinstance(alias, list):
            alias_str = ", ".join([str(idx) for idx in alias])

            metric = 'aliasByNode(%s, %s)' % (metric, alias_str)
        elif isinstance(alias, dict):
            if alias['kind'] == 'sub':
                metric = 'aliasSub(%s, \'%s\', \'%s\')' % (metric, alias['match'], alias['replacement'])
            else:
                raise RuntimeError('dict without kind==sub for metric %s' % metric)
        else:
            metric = 'alias(%s, \'%s\')' % (metric, alias)
    else:
        metric = 'aliasByMetric(%s)' % (metric)

    return metric


def add_metric(obj, host, metric, alias=None, scale=False, nnder=False, der=False, visible=True, sum='sum', kind='hosts', keepLastValue=True, timeShift=None, summarize=None):
    """Add a metric to a panel

    Parameters
    ----------
    obj: dict
      the Panel to add the metric to
    The remaining parameters are the same as for
    `grafana_format_metric`

    Return
    ------
    dict
      obj with the metric added
    """
    metric = grafana_format_metric(
        host, metric, alias, scale, nnder, der, visible, sum, kind,
        keepLastValue, timeShift, summarize=summarize)
    add_metric_raw(obj, metric, visible=visible)


def set_threshold(obj, threshold, host=None):
    if threshold:
        update_dict(obj, {
                "grid": {
                    "threshold1": int(threshold),
                    "threshold1Color": "rgb(216, 27, 27)",
                    "thresholdLine": True
                    },
                })
        set_yaxis_maximum(obj, 'left', int(threshold)*5./4)
    elif host:
        add_metric(obj, host, ['cpu.total.*'], 'CPUs', scale=0.01)


def grafana_panel_load(host, span=3, cpu_count=False):
    title = "Load"
    ret = get_default_graph(title, span)

    add_metric(ret, host, 'loadavg.15', 'Load 15m')
    add_metric(ret, host, 'loadavg.01', 'Load 1m')

    set_decimals(ret, 2)
    set_fill(ret, 0)
    set_yaxis_labels(ret, "load")
    add_series_override(ret, '/CPUs/', {'linewidth': 3})
    add_series_override(ret, '/Load 15/', {'linewidth': 0, 'fill': 4})

    set_threshold(ret, cpu_count, host)

    return ret


def grafana_panel_host_metadata(host, hostvars, span=12):
    title = "Metadata"
    ret = get_default_text(title, span)

    lines = []

    def add_line(line):
        lines.append(line)

    def add_separator():
        add_line('')

    def add_kv(key, value):
        add_line('| %s | %s |' % (key, value))

    def add_kvk(key, value_key):
        add_kv(key, hostvars[value_key])

    def add_link(name, src):
        add_separator()
        add_line('[%s](%s)' % (name, src))

    add_line('# %s' % (hostvars['inventory_hostname']))

    add_separator()  # --------------------------

    add_kv('Key', 'Value')
    add_kv('---', '---')
    add_kvk('Name', 'inventory_hostname')

    add_separator()  # --------------------------

    add_link('This host in Icinga', 'https://%s/cgi-bin/icinga/status.cgi?host=%s' % (hostvars['icinga_server_web_host'], hostvars['inventory_hostname']))

    set_content(ret, "\n".join(lines))

    return ret


def grafana_panel_load_01(host, span=3, cpu_count=False):
    title = "Load 1m"
    ret = get_default_graph(title, span)

    add_metric(ret, host, 'loadavg.01', 'Load 1m')

    set_decimals(ret, 2)
    set_threshold(ret, cpu_count)

    return ret


def grafana_panel_load_05(host, span=3, cpu_count=False):
    title = "Load 5m"
    ret = get_default_graph(title, span)

    add_metric(ret, host, 'loadavg.05', 'Load 5m')

    set_decimals(ret, 2)
    set_threshold(ret, cpu_count)

    return ret


def grafana_panel_load_15(host, span=3, cpu_count=False):
    title = "Load 15m"
    ret = get_default_graph(title, span)

    add_metric(ret, host, 'loadavg.15', 'Load 15m')

    set_decimals(ret, 2)
    set_threshold(ret, cpu_count)

    return ret


def grafana_panel_processes_running(host, span=3):
    title = "Processes running"
    ret = get_default_graph(title, span)

    add_metric(ret, host, 'loadavg.processes_running', 'Processes running')

    return ret


def grafana_panel_processes_total(host, span=3):
    title = "Processes total"
    ret = get_default_graph(title, span)

    add_metric(ret, host, 'loadavg.processes_total', 'Processes total')

    return ret


def grafana_panel_processes_both(host, span=3):
    title = "Processes"
    ret = get_default_graph(title, span)

    add_metric(ret, host, 'loadavg.processes_running', 'running')
    add_metric(ret, host, 'loadavg.processes_total', 'total')

    return ret


def grafana_panel_cpu(host, span=3):
    title = "CPU %"
    ret = get_default_graph(title, span)

    add_metric(ret, host, 'cpu.total.user')
    add_metric(ret, host, 'cpu.total.nice')
    add_metric(ret, host, 'cpu.total.system')
    add_metric(ret, host, 'cpu.total.iowait')
    add_metric(ret, host, 'cpu.total.irq')
    add_metric(ret, host, 'cpu.total.softirq')
    add_metric(ret, host, 'cpu.total.steal')
    add_metric(ret, host, 'cpu.total.idle')

    set_yaxis_units(ret, "percent")
    set_yaxis_maximum(ret, 'left', MAX_CPU) # Add max to limit effect of outliers.
    set_stacked_mode(ret)
    set_colors(ret, {
            "idle": "#3F2B5B",
            "iowait": "#BA43A9",
            "softirq": "#1F78C1",
            "steal": "#0A50A1",
            })
    return ret


def grafana_panel_cpu_kind(host, kind, color, span=3):
    title = kind
    ret = get_default_graph(title, span)

    add_metric(ret, host, 'cpu.total.%s' % kind)

    set_yaxis_units(ret, "percent")
    set_yaxis_maximum(ret, 'left', MAX_CPU) # Add max to limit effect of outliers.
    set_stacked_mode(ret)
    set_colors(ret, {
            kind: color,
            })
    return ret


def grafana_panel_memory(host, span=3):
    title = "Memory"
    ret = get_default_graph(title, span)

    add_metric(ret, host, ['memory.MemTotal', '#B', '#C', '#D'], 'Used w/o Buffers and Cache', sum='diff')
    add_metric(ret, host, 'memory.Buffers')
    add_metric(ret, host, 'memory.Cached')
    add_metric(ret, host, 'memory.MemFree', 'Free')

    set_stacked_mode(ret)
    set_yaxis_units(ret, "bytes")
    set_colors(ret, {
            "Buffers": "#1F78C1",
            "Cached": "#0A50A1",
            "Free": "#3F2B5B",
            })

    return ret


def grafana_panel_memory_kind(host, metric, label=None, color=None, span=3):
    if metric == 'used':
        title = 'Used w/o Buffers and Cache'
        label = title
    elif label:
        title = label
    else:
        title = metric
        label = title
    ret = get_default_graph(title, span)

    if metric == 'used':
        add_metric(ret, host, ['memory.MemTotal', '#B', '#C', '#D'], label, sum='diff')
        add_metric(ret, host, 'memory.Buffers', visible=False)
        add_metric(ret, host, 'memory.Cached', visible=False)
        add_metric(ret, host, 'memory.MemFree', visible=False)
    else:
        add_metric(ret, host, 'memory.%s' % metric, label)

    set_stacked_mode(ret)
    set_yaxis_units(ret, "bytes")
    if color:
        set_colors(ret, {
                label: color
                })

    return ret


def grafana_panel_network_bytes(host, span=3, title='Network bytes'):
    ret = get_default_graph(title, span)

    add_metric(ret, host, 'network.*.rx_byte', [-2, -1])
    add_metric(ret, host, 'network.*.tx_byte', [-2, -1])

    set_yaxis_units(ret, "Bps")

    return ret


def grafana_panel_network_packets(host, span=3):
    title = "Network packets"
    ret = get_default_graph(title, span)

    add_metric(ret, host, 'network.*.rx_packets', [-2, -1])
    add_metric(ret, host, 'network.*.tx_packets', [-2, -1])

    set_yaxis_units(ret, "pps")

    return ret


def grafana_panel_network_drop_and_errors(host, span=3):
    title = "Network drop & errors"
    ret = get_default_graph(title, span)

    add_metric(ret, host, 'network.*.rx_drop', [-2, -1])
    add_metric(ret, host, 'network.*.rx_errors', [-2, -1])
    add_metric(ret, host, 'network.*.tx_drop', [-2, -1])
    add_metric(ret, host, 'network.*.tx_errors', [-2, -1])

    set_yaxis_units(ret, "pps")

    return ret


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


def grafana_panel_diskspace_bytes(host, span=4):
    title = "Disk bytes available"
    ret = get_default_graph(title, span)

    add_metric(ret, host, "diskspace.*.byte_avail", [-2])

    set_yaxis_units(ret, "bytes")

    return ret


def grafana_panel_diskspace_percent(host, span=4):
    title = "Disk % free"
    ret = get_default_graph(title, span)

    add_metric(ret, host, "diskspace.*.byte_percentfree", [-2])

    set_yaxis_units(ret, "percent")

    return ret


def grafana_panel_iostat_queue_length(host, span=4):
    title = "Avg. Queue length"
    ret = get_default_graph(title, span)

    add_metric(ret, host, "iostat.*.average_queue_length", [-2])

    return ret


def grafana_panel_iostat_iops(host, span=4):
    title = "IOPS"
    ret = get_default_graph(title, span)

    add_metric(ret, host, 'iostat.*.reads_per_second', {
            'kind': 'sub',
            'match': "^.*\\.([^.]*)\\.([^._]*)_[^.]*$",
            'replacement': "\\1 \\2"})
    add_metric(ret, host, 'iostat.*.writes_per_second', {
            'kind': 'sub',
            'match': "^.*\\.([^.]*)\\.([^._]*)_[^.]*$",
            'replacement': '\\1 \\2'})

    return ret


def grafana_panel_iostat_throughput(host, span=4):
    title = "Disk throughput"
    ret = get_default_graph(title, span)

    add_metric(ret, host, "iostat.*.read_byte_per_second", {
            'kind': 'sub',
            'match': "^.*\\.([^.]*)\\.([^._]*)_[^.]*$",
            'replacement': "\\1 \\2"})
    add_metric(ret, host, "iostat.*.write_byte_per_second", {
            'kind': 'sub',
            'match': "^.*\\.([^.]*)\\.([^._]*)_[^.]*$",
            'replacement': "\\1 \\2"})

    set_yaxis_units(ret, "Bps")

    return ret


def grafana_panel_iostat_waiting(host, span=4):
    title = "IO awaits"
    ret = get_default_graph(title, span)

    add_metric(ret, host, 'iostat.*.read_await', {
            'kind': 'sub',
            'match': "^.*\\.([^.]*)\\.([^._]*)_[^.]*$",
            'replacement': "\\1 \\2"})
    add_metric(ret, host, 'iostat.*.write_await', {
            'kind': 'sub',
            'match': "^.*\\.([^.]*)\\.([^._]*)_[^.]*$",
            'replacement': "\\1 \\2"})

    return ret


def grafana_panel_graphite_cache(host, span=4):
    title = "Cache"
    ret = get_default_graph(title, span)

    add_metric(ret, host, "carbon.agents.*.cache.queries")
    add_metric(ret, host, "carbon.agents.*.cache.queues")

    return ret


def grafana_panel_graphite_updates(host, span=4):
    title = "Updates"
    ret = get_default_graph(title, span)

    add_metric(ret, host, "carbon.agents.*.metricsReceived")
    add_metric(ret, host, "carbon.agents.*.committedPoints")
    add_metric(ret, host, "carbon.agents.*.updateOperations")

    return ret


def grafana_panel_graphite_monitors(host, span=4):
    title = "Monitors"
    ret = get_default_graph(title, span)

    add_metric(ret, host, "carbon.agents.*.creates")
    add_metric(ret, host, "carbon.agents.*.errors")

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
    'grafana_add_row_overview': grafana_add_row_overview,
    'grafana_add_row_load': grafana_add_row_load,
    'grafana_add_row_host_metadata': grafana_add_row_host_metadata,
    'grafana_add_row_cpu': grafana_add_row_cpu,
    'grafana_add_row_memory': grafana_add_row_memory,
    'grafana_add_row_processes': grafana_add_row_processes,
    'grafana_add_row_disk': grafana_add_row_disk,
    'grafana_add_row_network': grafana_add_row_network,
    'grafana_add_row_time': grafana_add_row_time,
    'grafana_add_row_graphite': grafana_add_row_graphite,
    'grafana_add_row_apache': grafana_add_row_apache,
    'grafana_add_row_nginx': grafana_add_row_nginx,
    'grafana_format_metric': grafana_format_metric,
    'grafana_get_metric_retentions': get_metric_retentions,
    }


class FilterModule(object):
    '''Ansible jinja2 filter for hashing strings to numbers and mod-ing them'''

    def filters(self):
        return FILTERS

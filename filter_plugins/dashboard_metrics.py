import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from misc import update_dict
del sys.path[0]

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


def add_metric_raw(panel, metric, visible=True):
    panel['targets'].append(
        {
            "target": metric,
            "hide": (not visible),
            }
        )


def add_metric(panel, host, metric, alias=None, scale=False, nnder=False, der=False, visible=True, sum='sum', kind='hosts', keepLastValue=True, timeShift=None, summarize=None):
    """Add a metric to a panel

    Parameters
    ----------
    panel: dict
      the Panel to add the metric to
    The remaining parameters are the same as for
    `format_metric`

    Return
    ------
    dict
      panel with the metric added
    """
    metric = format_metric(
        host, metric, alias=alias, scale=scale, nnder=nnder, der=der, sum=sum, kind=kind,
        keepLastValue=keepLastValue, timeShift=timeShift, summarize=summarize)
    add_metric_raw(panel, metric, visible=visible)


def format_metric(host, metric, alias=None, scale=False, nnder=False, der=False, sum='sum', kind='hosts', keepLastValue=True, timeShift=None, summarize=None):
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


def get_metric_list(host, metric, kind='hosts'):
    if isinstance(metric, list):
        metric_list = [(single_metric if single_metric.startswith('#')
                       else '%s.%s.%s' % (kind, host, single_metric))
                       for single_metric in metric]
    else:
        metric = '%s.%s.%s' % (kind, host, metric)
        metric_list = [metric]

    return metric_list


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


def set_decimals(panel, decimals):
    panel["decimals"] = decimals


def set_fill(panel, fill):
    panel["fill"] = fill


def set_yaxis_helper(panel, axis, key, value):
    if 'yaxes' not in panel:
        panel['yaxes']=[{}, {}]
    if axis == 'left':
        axis_idx = 0
    else:
        axis_idx = 1
    panel['yaxes'][axis_idx][key] = value


def set_yaxis_units(panel, left='short', right='short'):
    key = 'format'
    set_yaxis_helper(panel, 'left', key, left)
    set_yaxis_helper(panel, 'right', key, right)


def set_yaxis_labels(panel, left, right=None):
    key = 'label'
    set_yaxis_helper(panel, 'left', key, left)
    if right:
        set_yaxis_helper(panel, 'right', key, right)


def set_yaxis_minimum(panel, axis, value):
    set_yaxis_helper(panel, axis, 'min', value)


def set_yaxis_maximum(panel, axis, value):
    set_yaxis_helper(panel, axis, 'max', value)


def set_stacked_mode(panel):
    panel["stack"] = True
    # Translucent stacked graphs are misleading. Hence we down down
    # translucency.
    set_fill(panel, 8)


def set_colors(panel, colors):
    panel["aliasColors"] = colors


def set_point_mode(panel):
    panel["points"] = True
    panel["pointradius"] = 0.5


def add_series_override(panel, alias, override):
    if "seriesOverrides" not in panel:
        panel["seriesOverrides"] = []

    obj = {
        "alias": alias,
        }

    for k, v in override.iteritems():
        obj[k] = v

    panel["seriesOverrides"].append(obj)


def switch_to_right_axis(panel, alias):
    add_series_override(panel, alias, {"yaxis": 2})


def connect_missing_points(panel):
    panel["nullPointMode"] = "connected"


def zero_missing_points(panel):
    panel["nullPointMode"] = "null as zero"


def set_threshold(panel, value, color):
    panel["threshold"] = {
        'value': value,
        'color': color,
        }


class FilterModule(object):
    '''Ansible jinja2 filters for metrics in graph panels of dashboards'''

    def filters(self):
        return {
            }

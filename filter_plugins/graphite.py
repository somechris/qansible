# -*- coding: utf-8 -*-

import json
import copy
import collections
import re

RETENTION_DAY_RESOLUTION = '25y'
RETENTION_HOUR_RESOLUTION = '1y'
RETENTION_MINUTE_RESOLUTION = '10d'


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
        'comment': 'metrics that are available only daily',
        'match': '.*daily.*',
        'retentions': resolve_retention(['day']),
    },
    {
        'name': 'hourly',
        'comment': 'metrics that are available only hourly',
        'match': '.*hourly.*',
        'retentions': resolve_retention(['hour', 'day']),
    },
    {
        'name': 'default',
        'comment': 'default fallback config',
        'match': '.*',
        'retentions': resolve_retention(['min', 'hour', 'day']),
    },
]


def get_metric_retentions(dummy=''):
    return METRIC_RETENTIONS


class FilterModule(object):
    '''Ansible jinja2 filter for hashing strings to numbers and mod-ing them'''

    def filters(self):
        return {
            'graphite_get_metric_retentions': get_metric_retentions,
            }

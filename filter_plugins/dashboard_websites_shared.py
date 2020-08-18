# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
del sys.path[0]


METHODS = [
    'CONNECT',
    'DELETE',
    'GET',
    'HEAD',
    'OPTIONS',
    'POST',
    'PUT',
    'TRACE',
    'unparsable',
    ]


STATUSES = [
    ('200', 'OK'),
    ('206', 'Partial Content'),
    ('301', 'Moved Permanently'),
    ('302', 'Found'),
    ('304', 'Not Modified'),
    ('401', 'Unauthorized'),
    ('404', 'Not Found'),
    ('500', 'Internal Server Error'),
    ('502', 'Bad Gateway'),
    ('503', 'Service Unavailable'),
    ('504', 'Gateway Timeout'),
    ]

TIMINGS = [
    ('average', 'avg'),
    ('q01', 'q01'),
    ('q05', 'q05'),
    ('q50', 'q50'),
    ('q95', 'q95'),
    ('q99', 'q99'),
    ('unparsable', 'unp'),
    ]

def web_metric_base(engine, website, aspect):
    website = website.replace('.', '_').replace('-', '_')
    aspect = ('.' + aspect if aspect else '')
    return 'logs.%s.%s%s' % (engine, website, aspect)


class FilterModule(object):
    '''Ansible jinja2 filters for shared website filters in dashboards'''

    def filters(self):
        return {
            }

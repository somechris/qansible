# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dashboard_row import new as new_row
from dashboard_row import set_weight
del sys.path[0]


def new(host, log_file):
    row = new_row(log_file['description'])

    set_weight(row, log_file['slug'])

    return row


def metric_base(log_file):
    return 'logs.' + log_file['group'] + '.' + log_file['item']


class FilterModule(object):
    '''Ansible jinja2 filters for Apache graphs in dashboards'''

    def filters(self):
        return {
            }

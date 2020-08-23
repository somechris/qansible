# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dashboard_row_log_file_custom import row_log_file_custom
del sys.path[0]


def row_log_file(host, log_file):
    return row_log_file_custom(host, log_file)


def rows_log_files(host, log_files):
    return [row_log_file(host, log_file) for log_file in log_files]


class FilterModule(object):
    '''Ansible jinja2 filters for Apache graphs in dashboards'''

    def filters(self):
        return {
            'dashboard_rows_log_files': rows_log_files,
            }

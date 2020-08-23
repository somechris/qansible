# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dashboard_row_log_file_shared import new
from dashboard_row_log_file_shared import metric_base
from dashboard_row_log_file_custom import panel_count
from dashboard_metrics import add_metric
from dashboard_metrics import set_yaxis_labels
from dashboard_metrics import set_yaxis_units
from dashboard_graph import new as new_graph
from dashboard_row import add_panel
del sys.path[0]

def row_log_file_python(host, log_file):
    row = new(host, log_file)

    base = metric_base(log_file)
    add_panel(row, panel_count(host, base, kinds=['CRITICAL', 'ERROR'], width=4))
    add_panel(row, panel_count(host, base, kinds=['WARNING', 'unparsable'], width=4))
    add_panel(row, panel_count(host, base, width=4))
    return row


class FilterModule(object):
    '''Ansible jinja2 filters for Apache graphs in dashboards'''

    def filters(self):
        return {
            }

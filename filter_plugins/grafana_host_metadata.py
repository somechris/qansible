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

def grafana_add_row_host_metadata(dashboard, host, hostvars, repeated=False, collapse=True):
    span = 12
    title = 'Metadata'
    row = get_default_row(title, host, repeated, collapse)
    update_dict(row, {
            "panels": [
                grafana_panel_host_metadata(host, hostvars, span=span),
                ],
            })
    return add_row(dashboard, row)


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


class FilterModule(object):
    '''Ansible jinja2 filters for grafana metadata graphs'''

    def filters(self):
        return {
            'grafana_add_row_host_metadata': grafana_add_row_host_metadata,
            }

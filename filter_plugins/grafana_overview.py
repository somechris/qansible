# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grafana_scaffolding import update_dict
from grafana_scaffolding import get_default_graph
from grafana_scaffolding import get_default_row
from grafana_scaffolding import add_row
from grafana_load import grafana_panel_load
from grafana_cpu import grafana_panel_cpu
from grafana_memory import grafana_panel_memory
from grafana_network import grafana_panel_network_bytes
del sys.path[0]

def grafana_add_row_overview(dashboard, host, cpu_count=False, repeated=False, collapse=True):
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




class FilterModule(object):
    '''Ansible jinja2 filters for grafana overview graphs'''

    def filters(self):
        return {
            'grafana_add_row_overview': grafana_add_row_overview,
            }

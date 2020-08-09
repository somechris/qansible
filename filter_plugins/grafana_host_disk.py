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

def grafana_add_row_disk(dashboard, host, repeated=False, collapse=True):
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


class FilterModule(object):
    '''Ansible jinja2 filters for grafana disk graphs'''

    def filters(self):
        return {
            'grafana_add_row_disk': grafana_add_row_disk,
            }

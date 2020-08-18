# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dashboard_metrics import add_metric
from dashboard_metrics import add_series_override
from dashboard_metrics import set_colors
from dashboard_metrics import set_yaxis_units
from dashboard_metrics import set_yaxis_maximum
from dashboard_metrics import set_fill
from dashboard_metrics import set_decimals
from dashboard_metrics import set_threshold
from dashboard_graph import new as new_graph
from dashboard_row import new as new_row
from dashboard_row import add_panel
del sys.path[0]


def panel_diskspace_bytes(host, width=None):
    title = 'Disk bytes available'
    panel = new_graph(title, width=width)

    add_metric(panel, host, "diskspace.*.byte_avail", [-2])

    set_yaxis_units(panel, "bytes")

    return panel


def panel_diskspace_percent(host, width=None):
    title = 'Disk % free'
    panel = new_graph(title, width=width)

    add_metric(panel, host, "diskspace.*.byte_percentfree", [-2])

    set_yaxis_units(panel, "percent")

    return panel


def panel_iostat_queue_length(host, width=None):
    title = 'Avg. Queue length'
    panel = new_graph(title, width=width)

    add_metric(panel, host, "iostat.*.average_queue_length", [-2])

    return panel


def panel_iostat_iops(host, width=None):
    title = "IOPS"
    panel = new_graph(title, width=width)

    add_metric(panel, host, 'iostat.*.reads_per_second', {
            'kind': 'sub',
            'match': "^.*\\.([^.]*)\\.([^._]*)_[^.]*$",
            'replacement': "\\1 \\2"})
    add_metric(panel, host, 'iostat.*.writes_per_second', {
            'kind': 'sub',
            'match': "^.*\\.([^.]*)\\.([^._]*)_[^.]*$",
            'replacement': '\\1 \\2'})

    return panel


def panel_iostat_throughput(host, width=None):
    title = "Disk throughput"
    panel = new_graph(title, width=width)

    add_metric(panel, host, "iostat.*.read_byte_per_second", {
            'kind': 'sub',
            'match': "^.*\\.([^.]*)\\.([^._]*)_[^.]*$",
            'replacement': "\\1 \\2"})
    add_metric(panel, host, "iostat.*.write_byte_per_second", {
            'kind': 'sub',
            'match': "^.*\\.([^.]*)\\.([^._]*)_[^.]*$",
            'replacement': "\\1 \\2"})

    set_yaxis_units(panel, "Bps")

    return panel


def panel_iostat_waiting(host, width=None):
    title = "IO awaits"
    panel = new_graph(title, width=width)

    add_metric(panel, host, 'iostat.*.read_await', {
            'kind': 'sub',
            'match': "^.*\\.([^.]*)\\.([^._]*)_[^.]*$",
            'replacement': "\\1 \\2"})
    add_metric(panel, host, 'iostat.*.write_await', {
            'kind': 'sub',
            'match': "^.*\\.([^.]*)\\.([^._]*)_[^.]*$",
            'replacement': "\\1 \\2"})

    return panel

def row_disk(host):
    title = 'Disk I/O'
    row = new_row(title)
    width=4

    add_panel(row, panel_diskspace_bytes(host, width=width))
    add_panel(row, panel_diskspace_percent(host, width=width))
    add_panel(row, panel_iostat_queue_length(host, width=width))
    add_panel(row, panel_iostat_iops(host, width=width))
    add_panel(row, panel_iostat_throughput(host, width=width))
    add_panel(row, panel_iostat_waiting(host, width=width))

    return row


class FilterModule(object):
    '''Ansible jinja2 filters for disk graphs in dashboards'''

    def filters(self):
        return {
            }

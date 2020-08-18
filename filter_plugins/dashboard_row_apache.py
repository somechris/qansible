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
from dashboard_metrics import set_stacked_mode
from dashboard_metrics import set_threshold
from dashboard_metrics import switch_to_right_axis
from dashboard_websites import panel_website_total_requests
from dashboard_websites import panel_websites
from dashboard_graph import new as new_graph
from dashboard_row import new as new_row
from dashboard_row import add_panel
del sys.path[0]


def panel_apache_workers_basic(host, width=None):
    title = "Workers (basic)"
    panel = new_graph(title, width=width)

    add_metric(panel, host, 'apache.localhost.BusyWorkers', 'Busy')
    add_metric(panel, host, 'apache.localhost.IdleWorkers', 'Idle')

    set_stacked_mode(panel)

    return panel


def panel_apache_throughput(host, width=None):
    title = "Accesses"
    panel = new_graph(title, width=width)

    add_metric(panel, host, 'apache.localhost.TotalAccesses', 'Accesses', scale=True, nnder=True)
    # 17.06666 = 1024/60
    add_metric(panel, host, 'apache.localhost.TotalkBytes', 'Bytes', scale=(1024./60), nnder=True)

    set_yaxis_units(panel, right="Bps")
    switch_to_right_axis(panel, "Bytes")

    return panel


def panel_apache_connections(host, width=None):
    title = "Connections"
    panel = new_graph(title, width=width)

    add_metric(panel, host, 'apache.localhost.ConnsTotal', 'Total')
    add_metric(panel, host, 'apache.localhost.ConnsAsyncClosing', 'Async Closing')
    add_metric(panel, host, 'apache.localhost.ConnsAsyncKeepAlive', 'Async Keep-Alive')
    add_metric(panel, host, 'apache.localhost.ConnsAsyncWriting', 'Async Writing')

    set_yaxis_units(panel, right="Bps")
    switch_to_right_axis(panel, "Bytes")

    return panel


def panel_apache_scorecard(host, width=None):
    title = "Workers (detailed)"
    panel = new_graph(title, width=width)

    add_metric(panel, host, 'apache.localhost.IdleWorkers', 'Idle')
    add_metric(panel, host, 'apache.localhost.StartingWorkers', 'Starting')
    add_metric(panel, host, 'apache.localhost.ReadingWorkers', 'Reading')
    add_metric(panel, host, 'apache.localhost.WritingWorkers', 'Writing')
    add_metric(panel, host, 'apache.localhost.KeepaliveWorkers', 'Keep-Alive')
    add_metric(panel, host, 'apache.localhost.DnsWorkers', 'Dns')
    add_metric(panel, host, 'apache.localhost.ClosingWorkers', 'Closing')
    add_metric(panel, host, 'apache.localhost.LoggingWorkers', 'Logging')
    add_metric(panel, host, 'apache.localhost.FinishingWorkers', 'Finishing')
    add_metric(panel, host, 'apache.localhost.CleanupWorkers', 'Cleanup')
    add_metric(panel, host, 'apache.localhost.EmptyWorkerSlots', 'Empty')

    set_stacked_mode(panel)

    return panel


def row_apache(host, websites):
    title = 'Apache'
    row = new_row(title)
    width=4

    add_panel(row, panel_apache_workers_basic(host, width=width))
    add_panel(row, panel_apache_throughput(host, width=width))
    add_panel(row, panel_apache_connections(host, width=width))
    add_panel(row, panel_apache_scorecard(host, width=width))
    add_panel(row, panel_website_total_requests(host, 'apache', width=width))
    add_panel(row, panel_websites(host, websites, width=width))

    return row


class FilterModule(object):
    '''Ansible jinja2 filters for Apache graphs in dashboards'''

    def filters(self):
        return {
            'dashboard_row_apache': row_apache,
            }

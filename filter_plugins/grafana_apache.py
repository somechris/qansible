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
from grafana_websites import grafana_add_rows_website
from grafana_websites import grafana_panel_website_total_requests
from grafana_websites import grafana_panel_websites
del sys.path[0]


def grafana_panel_apache_troughput(host, span=4):
    title = "Accesses"
    ret = get_default_graph(title, span)

    add_metric(ret, host, 'apache.localhost.TotalAccesses', 'Accesses', scale=True, nnder=True)
    # 17.06666 = 1024/60
    add_metric(ret, host, 'apache.localhost.TotalkBytes', 'Bytes', scale=(1024./60), nnder=True)

    set_yaxis_units(ret, right="Bps")
    switch_to_right_axis(ret, "Bytes")

    return ret


def grafana_panel_apache_workers_basic(host, span=4):
    title = "Workers (basic)"
    ret = get_default_graph(title, span)

    add_metric(ret, host, 'apache.localhost.BusyWorkers', 'Busy')
    add_metric(ret, host, 'apache.localhost.IdleWorkers', 'Idle')

    set_stacked_mode(ret)

    return ret


def grafana_panel_apache_connections(host, span=4):
    title = "Connections"
    ret = get_default_graph(title, span)

    add_metric(ret, host, 'apache.localhost.ConnsTotal', 'Total')
    add_metric(ret, host, 'apache.localhost.ConnsAsyncClosing', 'Async Closing')
    add_metric(ret, host, 'apache.localhost.ConnsAsyncKeepAlive', 'Async Keep-Alive')
    add_metric(ret, host, 'apache.localhost.ConnsAsyncWriting', 'Async Writing')

    return ret


def grafana_panel_apache_scorecard(host, span=4):
    title = "Workers (detailed)"
    ret = get_default_graph(title, span)

    add_metric(ret, host, 'apache.localhost.IdleWorkers', 'Idle')
    add_metric(ret, host, 'apache.localhost.StartingWorkers', 'Starting')
    add_metric(ret, host, 'apache.localhost.ReadingWorkers', 'Reading')
    add_metric(ret, host, 'apache.localhost.WritingWorkers', 'Writing')
    add_metric(ret, host, 'apache.localhost.KeepaliveWorkers', 'Keep-Alive')
    add_metric(ret, host, 'apache.localhost.DnsWorkers', 'Dns')
    add_metric(ret, host, 'apache.localhost.ClosingWorkers', 'Closing')
    add_metric(ret, host, 'apache.localhost.LoggingWorkers', 'Logging')
    add_metric(ret, host, 'apache.localhost.FinishingWorkers', 'Finishing')
    add_metric(ret, host, 'apache.localhost.CleanupWorkers', 'Cleanup')
    add_metric(ret, host, 'apache.localhost.EmptyWorkerSlots', 'Empty')

    set_stacked_mode(ret)

    return ret


def grafana_add_row_apache(dashboard, host, websites, add=True, collapse=True, repeated=False):
    span = 4
    title = "Apache"
    row = get_default_row(title, host, repeated, collapse)
    update_dict(row, {
            "panels": [
                grafana_panel_apache_workers_basic(host),
                grafana_panel_apache_troughput(host),
                grafana_panel_apache_connections(host),
                grafana_panel_apache_scorecard(host),
                grafana_panel_website_total_requests(host, 'apache', span=span),
                grafana_panel_websites(host, websites),
                ],
            })
    return add_row(dashboard, row) if add else dashboard


def grafana_add_rows_apache(dashboard, host, websites, add=True, repeated=False, collapse=True, fallback_sites=True):
    if add:
        dashboard = grafana_add_row_apache(dashboard, host, websites, repeated=repeated, collapse=collapse)
        for website in sorted(websites):
            dashboard = grafana_add_rows_website(dashboard, host, 'apache', website, 'https', repeated=repeated, collapse=collapse, ssl=True)
            dashboard = grafana_add_rows_website(dashboard, host, 'apache', website, 'http', repeated=repeated, collapse=collapse)
        if fallback_sites:
            dashboard = grafana_add_rows_website(dashboard, host, 'apache', 'other_vhosts', timing=False, repeated=repeated, collapse=collapse)
            dashboard = grafana_add_rows_website(dashboard, host, 'apache', 'fallback', timing=False, repeated=repeated, collapse=collapse)
    return dashboard


class FilterModule(object):
    '''Ansible jinja2 filters for grafana apache graphs'''

    def filters(self):
        return {
            'grafana_add_row_apache': grafana_add_row_apache,
            'grafana_add_rows_apache': grafana_add_rows_apache,
            }

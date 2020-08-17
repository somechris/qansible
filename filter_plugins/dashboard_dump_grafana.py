# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from misc import dump_json
from misc import update_dict
from dashboard import finalize as generic_finalize_dashboard
del sys.path[0]

import copy
import collections

default_panel = {
}

default_yaxis = {
    "format": "short",
    "label": None,
    "logBase": 1,
    "max": None,
    "min": 0,
    "show": True
}

default_graph = {
    "type": "graph",
    "nullPointMode": "null",
    "targets": [],
    "tooltip": {
        "value_type": "individual",
        },
    "yaxes": [{}, {}],
}

default_yaxis = {
    "format": "short",
    "label": None,
    "logBase": 1,
    "max": None,
    "min": 0,
    "show": True
}

default_text = {
    "type": "text",
    "editable": False,
    "mode": "markdown",
}

default_row = {
    "editable": False,
    "showTitle": True,
    "height": "250px",
}

# timepicker.time_options are not picked up by Grafana. The seem to be
# hard-coded in the version we use. But Grafana examples configure
# that setting. So we follow that lead. Hopefully it will get picked
# up in future versions.
default_dashboard = {
    "editable": False,
    "gnetId": None,
    "links": [],
    "originalTitle": "untitled",
    "schemaVersion": 12,
    "sharedCrosshair": True,
    "style": "dark",
    "timezone": "utc",
    "timepicker": {
        "enable": True,
        "time_options": [
            "5m",
            "15m",
            "30m",
            "1h",
            "3h",
            "6h",
            "12h",
            "24h",
            "2d",
            "7d",
            "30d",
            "60d",
            "90d",
            "1y",
            "2y",
            "5y",
            ],
        "refresh_intervals": [
            "1m",
            "5m",
            "15m",
            "30m",
            "1h",
            "2h",
            "1d",
            ],
        },
    "version": 0,
    }

#---------------------------------------------

def id_generator():
    next=1
    while True:
        yield next
        next += 1

def id_service():
    ids = id_generator()
    def id_getter():
        return next(ids)
    return id_getter


def finalize_panel(panel, next_id):
    if panel['type'] == 'graph':
        panel = update_dict(copy.deepcopy(default_graph), panel)
        panel['yaxes'][0] = update_dict(copy.deepcopy(default_yaxis), panel['yaxes'][0])
        panel['yaxes'][1] = update_dict(copy.deepcopy(default_yaxis), panel['yaxes'][1])
    elif panel['type'] == 'text':
        panel = update_dict(copy.deepcopy(default_text), panel)

    panel = update_dict(copy.deepcopy(default_panel), panel)
    if 'id' not in panel:
        panel['id'] = next_id()
    return panel


def finalize_row(row, next_id):
    row = update_dict(copy.deepcopy(default_row), row)

    row['panels'] = [finalize_panel(panel, next_id) for panel in row['panels']]

    return row

def finalize_dashboard(dashboard):
    next_id = id_service()

    dashboard = generic_finalize_dashboard(dashboard)
    dashboard = update_dict(copy.deepcopy(default_dashboard), dashboard)

    dashboard['rows'] = [finalize_row(row, next_id) for row in dashboard['rows']]

    dashboard['originalTitle'] = dashboard['title']
    del dashboard['basename']

    return dashboard

def dump(dashboard):
    dashboard = finalize_dashboard(dashboard)
    return dump_json(dashboard)


FILTERS = {
    'dashboard_dump_grafana': dump,
    }


class FilterModule(object):
    '''Ansible jinja2 filters for grafana scaffolding'''

    def filters(self):
        return FILTERS

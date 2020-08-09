# -*- coding: utf-8 -*-

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
    "yaxes": [
        copy.deepcopy(default_yaxis),
        copy.deepcopy(default_yaxis),
        ]
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
    "collapse": True,
}


def update_dict(target, source):
    for key, value in source.iteritems():
        if isinstance(value, collections.Mapping):
            repl = update_dict(target.get(key, {}), value)
            target[key] = repl
        else:
            target[key] = source[key]
    return target


PANELS = 0
def get_default_panel(title, span):
    global PANELS
    PANELS += 1
    ret = copy.deepcopy(default_panel)
    ret["id"] = PANELS
    ret['title'] = title
    ret['span'] = span
    return ret


def get_default_text(title, span):
    ret = get_default_panel(title, span)
    ret.update(copy.deepcopy(default_text))
    return ret


def get_default_graph(title, span):
    ret = get_default_panel(title, span)
    ret.update(copy.deepcopy(default_graph))
    return ret


def get_default_row(title, host, repeated, collapse):
    ret = copy.deepcopy(default_row)
    if repeated:
        title += " (" + host + ")"
        ret['repeat'] = repeated
    ret['title'] = title
    ret['collapse'] = collapse
    return ret


def add_row(dashboard, row):
    if not isinstance(dashboard, dict):
        dashboard = {}
    if 'rows' not in dashboard:
        dashboard['rows'] = []
    dashboard['rows'].append(row)
    return dashboard


class FilterModule(object):
    '''Ansible jinja2 filters for grafana scaffolding'''

    def filters(self):
        return {
            }

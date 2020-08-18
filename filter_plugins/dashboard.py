# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dashboard_row import finalize as finalize_row
del sys.path[0]

import json
import copy
import re

DEFAULT_ROW_WEIGHT=1000*1000

default_dashboard = {
    "rows": [],
    "tags": [],
    }

def new(title='Untitled dashboard', basename=None):
    """Prepares a new dashboard object

    Parameters
    ----------
    title: string
      The title for the dashboard

    Return
    ------
    object: The dashboard object
    """

    dashboard = copy.deepcopy(default_dashboard)
    dashboard['title'] = title

    if basename is None:
        basename = title.lower()
        basename = re.sub(r'[^a-z0-9.]', '_', basename)
    dashboard['basename'] = basename

    return dashboard


def add_template(dashboard, template):
    if 'templates' not in dashboard:
        dashboard['templates'] = []
    dashboard['templates'].append(template)


def add_tag(dashboard, tag):
    dashboard['tags'].append(tag)


def add_tags(dashboard, tags=[]):
    for tag in tags:
        add_tag(dashboard, tag)


def set_basename(dashboard, basename):
    dashboard['basename'] = basename


def add_row(dashboard, row, weight=DEFAULT_ROW_WEIGHT):
    dashboard['rows'].append({'weight': float(weight), 'row': row})
    return dashboard


def finalize(dashboard):
    ret = copy.deepcopy(dashboard)

    # sort rows by weight
    ret['rows'].sort(key=lambda e : e['weight'])

    # unbox rows
    ret['rows'] = [finalize_row(row['row']) for row in ret['rows']]

    # Ordering, deduping, and normalizing tags
    ret['tags'] = list(set([tag.replace('_', '-') for tag in ret['tags']]))
    ret['tags'].sort()

    return ret


FILTERS = {
    'dashboard_add_row': add_row,
    }


class FilterModule(object):
    '''Ansible jinja2 filters for generic dashboarding'''

    def filters(self):
        return FILTERS

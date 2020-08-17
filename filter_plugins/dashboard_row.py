# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dashboard_panel import finalize as finalize_panel
del sys.path[0]

import json
import copy
import re

DEFAULT_PANEL_WEIGHT=1000*1000

default_row = {
    "collapsed": True,
    "panels": [],
    }

def new(title='Untitled row'):
    """Prepares a new dashboard row object

    Parameters
    ----------
    title: string
      The title for the dashboard row

    Return
    ------
    object: The dashboard row object
    """

    row = copy.deepcopy(default_row)
    row['title'] = title

    return row

def add_panel(row, panel, weight=DEFAULT_PANEL_WEIGHT):
    row['panels'].append({'weight': float(weight), 'panel': panel})
    return row


def finalize(row):
    ret = copy.deepcopy(row)

    # sort panels by weight
    ret['panels'].sort(key = lambda e : e['weight'])

    # unbox panels
    ret['panels'] = [finalize_panel(panel['panel']) for panel in ret['panels']]

    return ret


FILTERS = {
    }


class FilterModule(object):
    '''Ansible jinja2 filters for rows in dashboards'''

    def filters(self):
        return FILTERS

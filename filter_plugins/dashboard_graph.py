# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dashboard_panel import new as new_panel
from misc import update_dict
del sys.path[0]

import json
import copy
import re

default_graph = {
    'type': 'graph',
    'targets': [],
 }

def new(title='Untitled graph panel', width=None):
    """Prepares a new graph panel object

    Parameters
    ----------
    title: string
      The title for the graph panel

    Return
    ------
    object: The graph panel object
    """

    panel = new_panel(title=title, width=width)
    panel = update_dict(panel, copy.deepcopy(default_graph))

    return panel


FILTERS = {
    }


class FilterModule(object):
    '''Ansible jinja2 filters for graph panels in dashboard rows'''

    def filters(self):
        return FILTERS

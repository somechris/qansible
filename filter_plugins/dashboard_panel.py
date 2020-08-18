# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
del sys.path[0]

import json
import copy
import re

default_panel = {
    'type': 'panel',
}


def new(title='Untitled untyped panel', width=None):
    """Prepares a new panel object

    Parameters
    ----------
    title: string
      The title for the panel

    Return
    ------
    object: The panel object
    """

    panel = copy.deepcopy(default_panel)
    panel['title'] = title
    panel['width'] = width if width is not None else 4

    return panel


def set_width(panel, width):
    panel['width'] = width


def finalize(panel):
    return panel


FILTERS = {
    }


class FilterModule(object):
    '''Ansible jinja2 filters for generic panels in dashboard rows'''

    def filters(self):
        return FILTERS

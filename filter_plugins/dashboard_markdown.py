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

default_markdown = {
    'type': 'markdown',
    'content': '',
}


def new(title='Untitled markdown panel', width=None):
    """Prepares a new markdown panel object

    Parameters
    ----------
    title: string
      The title for the markdown panel

    Return
    ------
    object: The markdown panel object
    """

    panel = new_panel(title=title, width=width)
    panel = update_dict(panel, copy.deepcopy(default_markdown))

    return panel


def set_content(panel, content):
    """Prepares a new markdown panel object

    Parameters
    ----------
    panel: markdown panel object
      The panel to add the markdown to
    content: string
      The title for the markdown panel

    Return
    ------
    object: The markdown panel object
    """

    panel['content'] = content

    return panel


FILTERS = {
    }


class FilterModule(object):
    '''Ansible jinja2 filters for markdown panels in dashboard rows'''

    def filters(self):
        return FILTERS

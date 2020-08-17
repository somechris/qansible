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

default_text = {
    'type': 'text',
    'content': '',
}


def new(title='Untitled text panel'):
    """Prepares a new text panel object

    Parameters
    ----------
    title: string
      The title for the text panel

    Return
    ------
    object: The text panel object
    """

    panel = new_panel(title=title)
    panel = update_dict(panel, copy.deepcopy(default_text))

    return panel


def set_content(panel, content):
    """Prepares a new text panel object

    Parameters
    ----------
    panel: text panel object
      The panel to add the text to
    content: string
      The title for the text panel

    Return
    ------
    object: The text panel object
    """

    panel['content'] = content

    return panel


FILTERS = {
    }


class FilterModule(object):
    '''Ansible jinja2 filters for text panels in dashboard rows'''

    def filters(self):
        return FILTERS

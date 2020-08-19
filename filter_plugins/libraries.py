# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dashboard_graph import new as new_graph
from dashboard_metrics import add_metric
from dashboard_metrics import set_decimals
from dashboard_metrics import set_yaxis_units
from dashboard_metrics import zero_missing_points
from dashboard_row import new as new_row
from dashboard_row import add_panel
from dashboard_row import set_repeat
from dashboard_text import new as new_text
from dashboard_text import set_content
from dashboard import new as new_dashboard
from dashboard import add_tags
from dashboard import add_row
from dashboard import add_template
from dashboard import set_basename
del sys.path[0]


def panel_library_next_due_date(library):
    panel = new_graph('Next due date')

    add_metric(panel, 'libraries', library + '.lent_items.next_due_date_days', [2], kind='services')

    set_yaxis_units(panel, "d")

    return panel


def panel_library_lent_items_total(library):
    panel = new_graph('Lent items total')

    add_metric(panel, 'libraries', library + '.lent_items.current.total', [2], kind='services')

    return panel


def panel_library_lent_items_categories(library):
    panel = new_graph('Lent items by category')

    add_metric(panel, 'libraries', library + '.lent_items.current.category.*', [6], kind='services')

    zero_missing_points(panel)

    return panel


def row_library(title, library):
    row = new_row(title)

    add_panel(row, panel_library_next_due_date(library))
    add_panel(row, panel_library_lent_items_total(library))
    add_panel(row, panel_library_lent_items_categories(library))

    return row


def dashboard_libraries(title):
    dashboard = new_dashboard(title)
    set_basename(dashboard, 'services-libraries')
    add_tags(dashboard, ['service', 'libraries'])
    add_template(dashboard, {
            'type': 'query',
            'label': 'Libraries',
            'name': 'library',
            'query': 'services.libraries.*'
            })

    row = row_library('All libraries', '*')
    add_row(dashboard, row)

    row = row_library('Library', '$library')
    set_repeat(row, 'library')
    add_row(dashboard, row)

    return dashboard


class FilterModule(object):
    '''Ansible jinja2 filters for library dashboards'''

    def filters(self):
        return {
            'dashboard_libraries': dashboard_libraries,
            }

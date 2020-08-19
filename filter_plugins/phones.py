# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dashboard_graph import new as new_graph
from dashboard_metrics import add_metric
from dashboard_metrics import set_decimals
from dashboard_metrics import set_yaxis_units
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


def panel_phone_credit_use(phone):
    panel = new_graph('Credits use')
    add_metric(panel, 'phones', phone + '.credit', [2], scale=-1, nnder=True, kind='services')
    set_decimals(panel, 2)
    set_yaxis_units(panel, "currencyEUR")

    return panel


def panel_phone_credit_left(phone):
    panel = new_graph('Credits left')
    add_metric(panel, 'phones', phone + '.credit', [2], kind='services')
    set_decimals(panel, 2)
    set_yaxis_units(panel, "currencyEUR")

    return panel


def panel_phone_days_until_deactivation(phone):
    panel = new_graph('Days left until Deactivation')
    add_metric(panel, 'phones', phone + '.deactivation_days', [2], kind='services')
    set_yaxis_units(panel, "d")

    return panel


def row_phone(title, phone):
    row = new_row(title)

    add_panel(row, panel_phone_credit_use(phone))
    add_panel(row, panel_phone_credit_left(phone))
    add_panel(row, panel_phone_days_until_deactivation(phone))

    return row


def dashboard_phones(title):
    dashboard = new_dashboard(title)
    set_basename(dashboard, 'services-phones')
    add_tags(dashboard, ['service', 'phones'])
    add_template(dashboard, {
            'type': 'query',
            'label': 'Phones',
            'name': 'phone',
            'query': 'services.phones.*'
            })

    row = row_phone('All Phones', '*')
    add_row(dashboard, row)

    row = row_phone('Phone', '$phone')
    set_repeat(row, 'phone')
    add_row(dashboard, row)

    return dashboard


class FilterModule(object):
    '''Ansible jinja2 filters for phone dashboards'''

    def filters(self):
        return {
            'dashboard_phones': dashboard_phones,
            }

# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dashboard_row_hp_printer_overview import row_hp_printer_overview
from dashboard_row_hp_printer_supply import row_hp_printer_supply
del sys.path[0]


def rows_hp_printer(host):
    rows = []
    rows.append(row_hp_printer_overview(host))
    rows.append(row_hp_printer_supply(host, "All", supply='*', collapsed=False))
    rows.append(row_hp_printer_supply(host, "Black Cartridge"))
    rows.append(row_hp_printer_supply(host, "Cyan Cartridge"))
    rows.append(row_hp_printer_supply(host, "Yellow Cartridge"))
    rows.append(row_hp_printer_supply(host, "Magenta Cartridge"))
    rows.append(row_hp_printer_supply(host, "Image Fuser Kit", pages=False))
    rows.append(row_hp_printer_supply(host, "Image Transfer Kit", pages=False))
    rows.append(row_hp_printer_supply(host, "Toner Collection Unit", percent=False, pages=False))

    return rows


class FilterModule(object):
    '''Ansible jinja2 filters for HP printers in dashboards'''

    def filters(self):
        return {
            'dashboard_rows_hp_printer': rows_hp_printer,
            }

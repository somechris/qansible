import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from misc import is_undefined
del sys.path[0]

import re


DEFAULT_LOG_LEVEL='info'

def map_level(level, none, error, info, debug, all):
    map = {
        'none': none,
        'error': error,
        'info': info,
        'debug': debug,
        'all': all,
        }
    return map[level]


def map_level_numeric(level):
    map = {
        'none': 60,
        'error': 40,
        'info': 20,
        'debug': 10,
        'all': 0,
        }
    return map[level]


def map_level_python(level):
    map = {
        'none': 'CRITICAL',
        'error': 'ERROR',
        'info': 'INFO',
        'debug': 'DEBUG',
        'all': 'DEBUG',
        }
    return map[level]


def map_level_java_jul(level):
    map = {
        'none': 'OFF',
        'error': 'SEVERE',
        'info': 'INFO',
        'debug': 'FINE',
        'all': 'ALL',
        }
    return map[level]


def map_level_java_log4j(level):
    map = {
        'none': 'OFF',
        'error': 'ERROR',
        'info': 'INFO',
        'debug': 'DEBUG',
        'all': 'ALL',
        }
    return map[level]


def level_includes(level, margin):
    return map_level_numeric(level) <= map_level_numeric(margin)


def expand_log_file(log_file):
    if not isinstance(log_file, dict):
        log_file = {'file': log_file}

    log_file.setdefault('description', 'Custom log file at ' + log_file['file'])
    log_file.setdefault('format', 'custom')
    log_file.setdefault('group', 'ungrouped')
    log_file.setdefault('item', re.sub('[.-/]+', '_', log_file['file']))
    log_file.setdefault('slug', log_file['group'] + '-' + log_file['item'])
    log_file.setdefault('skip', False)

    return log_file


def expand_log_files(log_files):
    ret = [expand_log_file(log_file) for log_file in log_files]
    ret = [log_file for log_file in ret if not log_file['skip']]
    return ret


def expand_log_file_for_common_task_rules(log_file, config):
    if not isinstance(log_file, dict):
        log_file = {'file': log_file}

    log_file.setdefault('group', config['role'])

    return expand_log_file(log_file)


def expand_log_files_for_common_task_rules(log_files, config):
    return [expand_log_file_for_common_task_rules(log_file, config) for log_file in log_files]


class FilterModule(object):
    '''Misc ansible jinja2 filter'''

    def filters(self):
        return {
            'logging_level_includes': level_includes,
            'logging_map_level': map_level,
            'logging_map_level_numeric': map_level_numeric,
            'logging_map_level_python': map_level_python,
            'logging_map_level_java_jul': map_level_java_jul,
            'logging_map_level_java_log4j': map_level_java_log4j,
            'logging_expand_log_files': expand_log_files,
            'logging_expand_log_files_for_common_task_rules': expand_log_files_for_common_task_rules,
            }

import collections
import itertools
import re
import json

def update_dict(target, source, merge_lists=False):
    for key, value in source.iteritems():
        if isinstance(value, collections.Mapping):
            repl = update_dict(target.get(key, {}), value)
            target[key] = repl
        if merge_lists and isinstance(value, list) \
                and isinstance(target.get(key, 0), list):
            target[key] += value
        else:
            target[key] = source[key]
    return target


def merge_list_of_lists(list_of_lists):
    return [i for i in itertools.chain.from_iterable(list_of_lists)]


def attrs(iterable, name):
    return [e[name] for e in iterable if name in e]


def slug(name, delimiter='-', title=False, capital=False):
    slug = name
    slug = re.sub('[^a-zA-Z0-9 ]+', ' ', slug)
    slug = re.sub('  *', ' ', slug)
    slug = slug.lower()
    if capital:
        slug=slug.capitalize()
    if title:
        slug=slug.title()
    slug = re.sub(' ', delimiter, slug)
    return slug

# Returns the role_name, if the filter sees it the first time, and
# "pass" otherwise.
ROLE_NAME_COUNTERS={}
def role_name_pass_if_already_included(role_name):
    global ROLE_NAME_COUNTERS
    counter = ROLE_NAME_COUNTERS.get(role_name,0)
    ROLE_NAME_COUNTERS[role_name] = counter + 1
    return "pass" if counter else role_name


def split(input, separator):
    return input.split(separator)

def is_list(input):
    return isinstance(input, list)


def repeat(base, length):
    return (base * (int(length/len(base)) + 1))[:length]


def whitespace(length):
    return repeat(' ', length)


def prepend_all_items(list, prepend):
    return [prepend + item for item in list]


def replace_if_whole_string_matches(source, needle, replacement):
    return replacement if source == needle else source

def replace_omit_string(source, replacement):
    return replace_if_whole_string_matches(source, 'omit', replacement)

def dump_json(obj):
    """Format an object as json string

    Parameters
    ----------
    obj: Any type accepted by json.dump

    Return
    ------
    string: the formatted JSON string
    """
    return json.dumps(obj, indent=2, sort_keys=True)


def var_shim_init(initial_value):
    return {'val': initial_value}


def var_shim_set(var, value):
    var['val'] = value
    return ''


def var_shim_add(var, value):
    var['val'] += value
    return ''


def var_shim_get(var):
    return var['val']


class FilterModule(object):
    '''Misc ansible jinja2 filter'''

    def filters(self):
        return {
            'attrs': attrs,
            'dump_json': dump_json,
            'update_dict': update_dict,
            'merge_list_of_lists': merge_list_of_lists,
            'slug': slug,
            'role_name_pass_if_already_included': role_name_pass_if_already_included,
            'split': split,
            'is_list': is_list,
            'repeat': repeat,
            'whitespace': whitespace,
            'prepend_all_items': prepend_all_items,
            'replace_if_whole_string_matches': replace_if_whole_string_matches,
            'replace_omit_string': replace_omit_string,
            'var_shim_init': var_shim_init,
            'var_shim_set': var_shim_set,
            'var_shim_add': var_shim_add,
            'var_shim_get': var_shim_get,
        }

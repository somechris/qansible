import collections
import itertools


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


class FilterModule(object):
    '''Misc ansible jinja2 filter'''

    def filters(self):
        return {
            'update_dict': update_dict,
            'merge_list_of_lists': merge_list_of_lists,
        }

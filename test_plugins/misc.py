def starts_with(value, start):
    return value.startswith(start)


def starts_with_any(value, starts):
    return bool([start for start in starts if value.startswith(start)])


def starts_different_from(value, start):
    return not value.startswith(start)


def starts_different_from_all(value, starts):
    return not value.starts_with_any(starts)


def ending_with(value, start):
    return value.endswith(start)


def not_in(needle, haystack):
    return needle not in haystack


class TestModule(object):
    '''Ungrouped Ansible jinja2 tests'''

    def tests(self):
        return {
            'starts_with': starts_with,
            'starts_with_any': starts_with_any,
            'starts_different_from': starts_different_from,
            'starts_different_from_all': starts_different_from_all,
            'not_in': not_in,
            'ending_with': ending_with,
            }

import re

def to_group_name(candidate):
    ret = candidate
    ret = re.sub('[^a-zA-Z0-9_]+', '_', ret)
    return ret


def to_group_names(candidates):
    return [to_group_name(candidate) for candidate in candidates]


class FilterModule(object):
    """Ansible jinja2 filter for groups"""

    def filters(self):
        return {
            'to_group_name': to_group_name,
            'to_group_names': to_group_names,
        }

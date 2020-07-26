def map_os_to_image(os):
    os = os.lower()
    ret = 'unknown.git'
    if os == 'debian':
        ret = 'base/debian.gif'
    elif os == 'gentoo':
        ret = 'vendors/gentoo.gif'
    return ret


class FilterModule(object):
    '''Filters for icinga'''

    def filters(self):
        return {
            'map_os_to_image': map_os_to_image,
        }

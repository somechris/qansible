def map_os_to_image(os):
    os = os.lower()
    ret = 'unknown.gif'
    if os == 'debian':
        ret = 'base/debian.gif'
    elif os == 'gentoo':
        ret = 'vendors/gentoo.gif'
    elif os == 'hp':
        ret = 'vendors/hp-ux2.gif'
    elif os == 'openwrt':
        ret = 'vendors/linux40.gif'
    elif os == 'linux':
        ret = 'vendors/linux40.gif'
    return ret


class FilterModule(object):
    '''Filters for icinga'''

    def filters(self):
        return {
            'map_os_to_image': map_os_to_image,
        }

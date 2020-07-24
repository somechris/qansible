import crypt


# You can use
#
#   gpg --gen-random 2 200 | LC_ALL=C tr -d -c 'a-zA-Z0-9./' | cut -c 1-16
#
# to generate a good salt
def mkpasswd(password, salt, method='SHA512-CRYPT', add_text_method=True):
    if method == 'SHA512-CRYPT':
        if len(salt) != 16:
            raise RuntimeError("Salt has to be 16 characters in [a-zA-Z0-9./] for %s." % (method))
        hashed_password = crypt.crypt(password, "$6$%s" % (salt))
    else:
        raise NotImplementedError("Only SHA512-CRYPT is supported at " +
                                  "this point")
    ret = (('{%s}' % (method)) if add_text_method else '') + hashed_password
    return ret


def format_passwd_line(user, password, salt, uid='', gid='', gecos='', home='', shell='/bin/nologin', extra=''):
    items = []
    items += [user]
    items += [mkpasswd(password, salt)]
    items += [uid]
    items += [gid]
    items += [gecos]
    items += [home]
    items += [shell]
    if extra:
        items += [extra]
    return ':'.join(items)


class FilterModule(object):
    '''Password jinja2 filters'''

    def filters(self):
        return {
            'mkpasswd': mkpasswd,
            'format_passwd_line': format_passwd_line,
        }

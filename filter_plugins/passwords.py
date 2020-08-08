import crypt
import hashlib
import base64
import hmac


# You can use
#
#   gpg --gen-random 2 200 | LC_ALL=C tr -d -c 'a-zA-Z0-9./' | cut -c 1-16
#
# to generate a good salt
def mkpasswd(password, salt, method='SHA512-CRYPT', add_text_method=True):
    if len(password) < 12:
        # Warn about too short passwords
        raise RuntimeError("Please use at least 12 character long passwords. (The given one has only %d characters)" % (len(password)))
    if len(salt) < 16:
        # Warn about too short salts. We want to make sure they are long enough
        # to contribute to the difficulty.
        raise RuntimeError("Please use at least 16 characters as salt. ('%s' has only %d characters)" % (salt, len(salt)))
    if method == 'SHA512-CRYPT':
        if len(salt) != 16:
            raise RuntimeError("Salt has to be 16 characters in [a-zA-Z0-9./] for %s. ('%s' has %d characters)" % (method, salt, len(salt)))
        hashed_password = crypt.crypt(password, "$6$%s" % (salt))
    elif method == 'SSHA':  # SHA1 is broken, but SSHA is still ok-ish. If
        # possible, avoid SSHA and use something more secure
        hash = hashlib.sha1()
        hash.update(password)
        hash.update(salt)
        hashed_password = base64.b64encode(hash.digest() + str(salt))
    else:
        raise NotImplementedError("Only SHA512-CRYPT and SSHA are supported " +
                                  "at this point")
    ret = (('{%s}' % (method)) if add_text_method else '') + hashed_password
    return ret


def ssh_known_hosts_hash(host, hex_salt):
    if len(hex_salt) != 40:
        raise RuntimeError('hex_salt %s is %d characters long, but has to be 40 characters long' % (hex_salt, len(hex_salt)))
    salt = hex_salt.decode("hex")
    digest = hmac.new(salt, host, hashlib.sha1).digest()
    return '|1|%s|%s' % (base64.b64encode(salt), base64.b64encode(digest))


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
            'ssh_known_hosts_hash': ssh_known_hosts_hash,
        }

def ssl_config(type='compat', variant='openssl'):
    """Generates ciphersuite settings.

    Parameters
    ----------
    type:
      The kind of ciphersuit to get.
      Currently supported values are:
        - 'hardened' (for more restrictive, hardened setups)
        - 'compat' (for common setups)
        - 'relaxed' (for setups that favor ease of use over security)
    variant: string
      The backend for which to generate a ciphersuite.
      Currently supported values are:
        - openssl

    Return
    ------
    dict: The ciphersuite. It has the following keys
      ciphers - the ciphers
    """
    if variant == 'openssl':
        if type == 'hardened':
            ciphers = [
                '-ALL',
                'ECDHE-ECDSA-AES128-GCM-SHA256',
                'ECDHE-RSA-AES128-GCM-SHA256',
                'DHE-RSA-AES128-GCM-SHA256',
                'ECDHE-ECDSA-AES256-GCM-SHA384',
                'ECDHE-RSA-AES256-GCM-SHA384',
                'DHE-RSA-AES256-GCM-SHA384',
                '!aNULL',
                ]
        elif type == 'compat':
            ciphers = [
                'ECDHE-RSA-AES128-GCM-SHA256',
                'ECDHE-ECDSA-AES128-GCM-SHA256',
                'ECDHE-RSA-AES256-GCM-SHA384',
                'ECDHE-ECDSA-AES256-GCM-SHA384',
                'DHE-RSA-AES128-GCM-SHA256',
                'DHE-DSS-AES128-GCM-SHA256',
                'kEDH+AESGCM',
                'ECDHE-RSA-AES128-SHA256',
                'ECDHE-ECDSA-AES128-SHA256',
                'ECDHE-RSA-AES128-SHA',
                'ECDHE-ECDSA-AES128-SHA',
                'ECDHE-RSA-AES256-SHA384',
                'ECDHE-ECDSA-AES256-SHA384',
                'ECDHE-RSA-AES256-SHA',
                'ECDHE-ECDSA-AES256-SHA',
                'DHE-RSA-AES128-SHA256',
                'DHE-RSA-AES128-SHA',
                'DHE-DSS-AES128-SHA256',
                'DHE-RSA-AES256-SHA256',
                'DHE-DSS-AES256-SHA',
                'DHE-RSA-AES256-SHA',
                'AES128-GCM-SHA256',
                'AES256-GCM-SHA384',
                'AES128-SHA256',
                'AES256-SHA256',
                'AES128-SHA',
                'AES256-SHA',
                'AES',
                'CAMELLIA',
                'DES-CBC3-SHA',
                '!aNULL',
                '!eNULL',
                '!EXPORT',
                '!DES',
                '!RC4',
                '!MD5',
                '!PSK',
                '!aECDH',
                '!EDH-DSS-DES-CBC3-SHA',
                '!EDH-RSA-DES-CBC3-SHA',
                '!KRB5-DES-CBC3-SHA',
                ]
        else:
            raise RuntimeError('Unsupported cipher type \'%s\' for ssl_cipher'
                               % (type))
        ciphers = ':'.join(ciphers)
        protocols = ['TLSv1.2']
    elif variant == 'gnutls':
        if type == 'hardened':
            ciphers = [
                'SECURE128',
                '+SECURE192',
                '-VERS-ALL',
                '+VERS-TLS1.2',
                ]
        elif type == 'compat':
            ciphers = [
                'NORMAL',
                '%COMPAT',
                ]
        else:
            raise RuntimeError('Unsupported cipher type \'%s\' for ssl_cipher'
                               % (type))
        ciphers = ':'.join(ciphers)
        protocols = []
    else:
        raise RuntimeError('Unsupported cipher variant \'%s\' for ssl_cipher'
                           % (variant))
    ret = {
        'ciphers': ciphers,
        'protocols': protocols,
        }
    return ret


class FilterModule(object):
    """Ansible jinja2 filter for handling website definitions"""

    def filters(self):
        return {
            'ssl_config': ssl_config
        }

import md5


def hashing_mod(val=None, mod=60, add=0):
    """Add two values and compute a mod of them

    This function can be passed the hostname as val, and thereby
    allows to get a value that for a given host is constant for each
    Ansible run, but is different for different hosts.

    This property is useful when figuring out the minute when to run
    cron jobs, if the cronjob should be scheduled hourly on multiple
    hosts, but the hosts should schedule the job on different minutes

    Parameters
    ----------
    val: string, int, long
      The first value to add. If it is a string, it's md5sum is taken
      as value
    mod: int
      The modulus
    add: int
      The second value to add.

    Return
    ------
    int: (val + add) % mod
    """
    # Python3 does not provide `long`, so we need to shim it to make
    # flake8 pass on Python 3. But note that does not mean that this
    # filter is ready for Python3!
    try:
        long
    except NameError:
        long = int
    if not isinstance(val, (int, long)):
        try:
            val = int(val)
        except ValueError:
            hasher = md5.new()
            hasher.update(val)
            val = int(hasher.hexdigest(), 16)
    return ((val + add) % mod)


class FilterModule(object):
    '''Ansible jinja2 filter for hashing strings to numbers and mod-ing them'''

    def filters(self):
        return {
            'hashing_mod': hashing_mod
        }

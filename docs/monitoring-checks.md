# Monitoring checks

To allow switching between monitoring solutions, we don't hard-code monitoring
checks into the roles, but we instead collect the needed monitoring actions for
each role in the fact `monitoring_check_config`, and let the monitoring
solutions decide how to perform them.

`monitoring_check_config` is a list and each item defines a monitoring
action. Each action is either a string, or a dictionary. string definitions are
just abbrevations for dictionaries. A definition 'foo' is equivalent to the
dictionary

```
{
  'name': 'foo',
  'command': 'foo',
}
```

A dictionary definition has the following key/values:
* `name`: The check's name.
* `type`: (Default: `process`) The type of the check. Has to be one of `disk`,
  `load`, `port`, `process`, `file_age`, or `website`.
* `skip`: (Default: False) If true, this monitoring check gets skipped. This
  allows to easily turn some checks in a list of checks on/off.



## Type `disk`

The type `disk` checks the free disk spaces and free inodes. The following
additional key/values allow to specify what processes to expect:
* `bytes_left_warn`: (Default: 20%) Raise a warning, if less than this many
  bytes are free on a disk. If the setting ends in `%`, it is taken as
  percentage. Otherwise as number of MBs.
* `bytes_left_critical`: (Default: 10%) Raise a critical alert, if less than
  this many bytes are free on a disk. If the setting ends in `%`, it is taken as
  percentage. Otherwise as number of MBs.
* `inodes_left_warn`: (Default: 20%) Raise a warning, if less than this many
  inodes are free on a disk. If the setting ends in `%`, it is taken as
  percentage. Otherwise as number of MBs.
* `inodes_left_critical`: (Default: 10%) Raise a critical alert, if less than
  this many inodes are free on a disk. If the setting ends in `%`, it is taken as
  percentage. Otherwise as number of MBs.


## Type `file_age`

The type `file_age` checks that file has a recent modification timestamp.  The
following additional key/values allow to specify what processes to expect:
* `path`: (Default: The action's name) The path to the file to check argument.
* `warn`: (Default: 300) If the file is older than this many seconds, a warning
  is raised.
* `critical`: (Default: 300) If the file is older than this many seconds, a
  critical alert is raised.


## Type `load`

The type `load` checks the computing load on the host. The following additional
key/values allow to specify what processes to expect:
* `load1_warn`: (Default: 2) Raise a warning, if the 1 minute load average per
  processor is above this value.
* `load1_critical`: (Default: 4) Raise a critical alert, if the 1 minute load
  average per processor is above this value.
* `load5_warn`: (Default: 1.1) Raise a warning, if the 5 minute load average per
  processor is above this value.
* `load5_critical`: (Default: 1.5) Raise a critical alert, if the 5 minute load
  average per processor is above this value.
* `load15_warn`: (Default: 0.8) Raise a warning, if the 15 minute load average per
  processor is above this value.
* `load15_critical`: (Default: 0.9) Raise a critical alert, if the 15 minute load
  average per processor is above this value.


## Type `port`

The type `port` checks that a given port is open and accepting
connections. The following additional key/values allow to specify what
processes to expect:
* `port`: The port to connect to.
* `protocol`: (Default: `tcp`) The protocol to use for
  connecting. Currently, only `tcp` is supported.
* `service`: (Default: None) A hint about the protocol that's running
  there. Monitoring systems can use this to run more specialized
  checks. But this is optional, and monitoring systems are not
  required to honor this setting and are not required to run more
  specialized checks. Use the following values for services:
  * `ssh`: SSH server


## Type `process`

The type `process` checks that the expected processes are running as immediate
child of the root process. The following additional key/values allow to specify
what processes to expect:
* `argument`: If specified, match only processes that are run with this
  argument.
* `command`: (Default: If the monitoring action is a string (not a dictionary),
  then the default for `command` is that string. Otherwise it is unset) If set,
  match only processes that are run this command (without path)
* `min-procs`: (Default: 1) The minimal number of processes that need to match
  the other conditions. Use the empty string to not check the minimum number of
  processes.
* `max-procs`: (Default: 1) The maximum number of processes that may match the
  other conditions. Use the empty string to not check the maximum number of
  processes.
* `user`: (Default: `root`) Match only processes run by this user. Use the
  string `omit` (not Ansible's variable of name `omit`) to not check the process
  owner.

## Type `website`

The type `website` checks if a website is working from the checking host. The config The
following additional key/values allow to specify what processes to expect:
* `domain`: The domain to check.
* `kind`: The kind of website (E.g. `apache`, or None)
* `dns`: (Default: False) If False, target the request at the host no
  matter what DNS would resolve the domain to. If True, target the
  request at whatever host DNS resolves the domain to.

Checks for domains are taken from `monitoring_website_health_checks`, which is
per default a merge of `monitoring_website_health_checks_defaults`, and
`monitoring_website_health_checks_extra`. The last one is where to best put
configurations for user-defined domains. Each of the three variables is a
dictionary of configurations.

For a domain `foo.bar.baz`, the checks defined by the following keys get added
up (with the later overruling the earlier ones): `foo`, `foo.bar.baz`. The value
for each key is again a dictionary holding the following key/value pairs:
* `alias`: (Default: None) Merges the definition of another web host check
  in. So if the value of `alias` is `foo`, then the definitions of
  `monitoring_website_health_checks['foo']` get added in.
* `protocols`: (Default: ['https', 'http']) The list of protocols offered by
  this server. (See `protocol` of the individual checks to see how to specify
  which protocol gets used for a check). If 'https' is contained, a check for
  certificate expiration is added automatically. If both 'http' and 'https' is
  present, a check that 'http' requests get forwarded to 'https' urls gets
  added.
* `ssl`: (Default: None) If set, enforce a given SSL/TLS version for https
  connections. The following mapping applies:
    * 1: TLS 1
    * 1.1: TLS 1.1
    * 2: SSL 2
    * 3: SSL 3
* Each of the remaining key is considered the name of a check and the
  corresponding value in a dictionary that sepecifies how to check. It's
  key/values are:
    * `data`: (Default: 'None') The encoded data to send along with the request.
    * `encode_data`: (Default: 'None') The unencoded data to send along with the
      request. The data will get encoded automatically.
    * `expected_status_code`: (Default: 200) The response status code needed to
      pass the check.
    * `expected_content`: (Default: '') The content that needs to be in the
      response to pass the check.
    * `max_seconds`: (Default: 2) The maximum number of seconds to allow the
      request to finish. Possible values are `2`, `5`, `10`, `15`, `20`, `30`,
      and `45`.
    * `method`: (Default: 'GET') The HTTP method to use for the check. Only
      `GET` and `POST` are supported at this time.
    * `port`: (Default: None), If `None`, request on the default port for the
      used protocol. Otherwise request on the given port.  `http`) The protocol
      to check on.
    * `protocol`: (Default: 'https' if the web host offers https, otherwise
      `http`) The protocol to check on.
    * `uri`: (Default: '/') The uri to check.
Note that adding a domain configuration to one of the above three configuration
variables only configures the check and does not automatically run checks. It's
the responsibility of the roles (E.g.: `apache-website`) to bring the checks
into place. Additionally, the domains listed in `monitoring_external_websites`,
and `monitoring_internal_websites` have checks set up automatically:

* `monitoring_external_websites`: List of domains that are considered publicly
  accessible and should be monitored. Each of these are checked from the Icinga
  server according to the checks specified in `monitoring_website_health_checks`
* `monitoring_internal_websites`: List of domains that are considered only
  internally visible and should be monitored. Each of these are checked from the
  Icinga server according to the checks specified in
  `monitoring_website_health_checks`

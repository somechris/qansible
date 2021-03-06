# Common role tasks

Typically in Ansible, many roles follow the same structure. First some
preparations, then package installation and finally some fixups. This typically
leads to lots of duplication. To dedupe this, we try to put common tasks
(updating the firewall, guarding against unsupported distributions, ...) into
dedicated roles and re-use them in newly written roles. This helps with
deduplication and increases re-use. The names of these roles starts in
`common-role-tasks`.

At the core of each of these rules is a single configuration dictionary. The
following key/values are supported (Many of these would allow for good
defaults. E.g.: The empty list as default for the list of notifications. We on
purpose do not provide them, as it would then be too easy to miss defining them
in new roles. And that need not be immediately noticable, and maybe needlessly
tricky to debug. Hence, we omit most defaults. That way, we users are forced to
think about them and cannot easily overlook them. We only provide defaults, when
a field has almost always the same value. For example ports are almost always
`tcp`, and the name of a user group is almost always the same as the user
name.):
* `dashboard_host_rows`: A list of rows to add to the host dashboard. Each row
  has to be a row formatted accordingly to `dashboards.md`. (See `dashboards`
  key to add full blown, self-standing dashboards)
* `dashboards`: A list of dashboards. Each dashboard has to be a full,
  self-standing formatted accordingly to `dashboards.md`. (See
  `dashboard_host_rows` to add rows to the host's dashboard)
* `extra_groups`: (Default: []) List of groups to add the user to in addition to
  the main group (given through the `group` key). If an item in the list is
  empty, it automatically gets filtered away.
* `group`: (Default: value at key `user`) The name of the group for the
  service. The group will get created, if it's missing. Use the string 'omit'
  (not `{{omit}}`) to omit all group actions (group creation, setting owner
  groups on files, ...).
* `log_files`: A list of log file definitions following the format
  described in `docs/logging.md`
* `monitoring_checks`: A list of definitions of monitoring checks for
  this server.
#TO-DO: add documentation for monitoring key
* `notifications`: A list of handlers to notify upon changes.
* `packages`: If all supported distributions use the same package
  name, it is a list of packages to install for the including role. If
  packages names differ, it is a dictionary, where the key is the
  distribution and the value is the list of package names to install
  for that distribution.
* `paths`: A list of directory/link definitions set up. Each definition is a
  either a string or a dictionary. A string `foo` is an abbreviation for a
  dictionary `{type: 'directory', 'path': 'foo'}`. Dictionaries can have the
  following key/values:
  * `force`: (Default: False) If True, create symlinks even if the
    source does not exist or if the destination is a file. If False,
    fail in these cases.
  * `group`: (Default: the config's `group`) Sets the path's owner group.
  * `mode`: (Default: '775' for directories, omit for files, and '444'
    for everything else) Sets the file access mode for the path. Due
    to the looping through Jinja, it's best to avoid octal
    notation. So either use the descriptive form, or the octal number
    as string without leading 0.
  * `state`: (Default: 'directory') the state of the path to generate. See the
    `state` parameter of Ansible's file module. As state `touch` is used mostly
    (only?) to make sure files exist, timestamps are preserved in state `touch`
    to avoid unintended updates.
  * `path`: the path of the directory/link to define. See the `path` parameter
    of Ansible's file module.
  * `source`: the source for links. See the `src` parameter of Ansible's file
    module.
  * `user`: (Default: the config's `user`) Sets the path's owner.
* `port_configs`: A list of firewall port configurations. Each item is a
  dictionary and covers a single port. Each such dictionary can have the
  following key/values.
  * `name`: The name of this rule. This will get use as name of the firewall
    chain..
  * `port`: For protocols `tcp` and `udp`, the port to use for this config.
  * `protocol`: (Default: `tcp`) The protocol to use for this config.
  * `icmp_type`: If protocol is icmp, it gives the icmp type to allow.
  * `incoming_net_accesses`: List of net-accesses that can access the port.
  * `skip`: (Default: False) If true, ignore this item. This is useful to easily
    switch parts of the list on/off based on some configuration value.
* `role`: The name of the role that includes the `common-role-tasks-*` role. We
  need to hard-wire this, as `{{role_path|basename}}` would get evaluated in the
  context of the `common-role-task-*` and hence would not give the including,
  but the included role name. As this would be undesired, we explicitly have to
  give the including role name.
* `services`: List of service names provided by the including role. These
  services get enabled and started at the end of the role.
* `supported_distributions`: Either a list of distributions that the including
  role supports, or the string `any` to mark that nothing distribution dependent
  is happening in the role and it may run on all distributions.
* `user`: The name of the user for the service. This will be the owner of the
  files (after the packages got installed). The user get created as system user
  automatically, if it is missing. Use the string 'omit' (not `{{omit}}`) to
  omit all user actions (user creation, setting file owners, ...).
* `user_comment`: (Default: Service user for {{role_name}}) The
  comment (gecos field) for the service user.
* `user_home`: (Default: /var/lib/{{role_name}}) The home directory for the
  service user. Note that this directory does not automatically get created or
  otherwise prepared.

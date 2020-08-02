Role: diamond
=============



1. Description
2. Globals
3. Parameters



1. Description
--------------

Sets up diamond on the host. Diamond is a framework for metric
gathering on the host and reporting them to a metric service
(`graphite` in our case).

We use diamond to gather the baseline host metrics (CPU utilization,
disk usage, ...) and extend it with some plugins that allow analyzing
apache/nginx log files, gather metrics from data in databases, ...



2. Globals
----------

No Globals that are specific only for this role.



3. Parameters
-------------

* `diamond_collector_dir`: Directory to store additional diamond collectors
  (plugins that gather metrics) in.
* `diamond_collector_conf_dir`: Directory to store collector configs in.
* `diamond_collector_conf_extension`: File extension used for files within
  `diamond_collector_conf_dir`.
* `diamond_effective_log_dir`: Directory where logs effectively get stored in.
* `diamond_log_dir`: Directory proccesses will write logs to.
* `diamond_effective_data_disk`: Directory for data disk where data effectively
  gets stored in.
* `diamond_effective_data_dir`: Directory where data effectively gets stored in.
* `diamond_path_config`: Config for paths and links needed by this cole. This is
  a list of directory/link definitions. Each definition is a either a string or
  a dictionary. A string `foo` is an abbreviation for a dictionary `{type:
  'directory', 'path': 'foo'}`. Dictionaries can have the following key/values:
  * `state`: (Default: 'directory') the state of the path to generate. See the
    `state` parameter of Ansible's file module.
  * `path`: the path of the directory/link to define. See the `path` parameter
    of Ansible's file module.
  * `source`: the source for links. See the `src` parameter of Ansible's file
    module.

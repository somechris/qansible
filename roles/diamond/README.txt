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

* `diamond_collector_dir`: Directory to store additional diamond collectors
  (plugins that gather metrics) in.
* `diamond_collector_conf_dir`: Directory to store collector configs in.
* `diamond_collector_conf_extension`: File extension used for files within
  `diamond_collector_conf_dir`.



3. Parameters
-------------

* `diamond_custom_collectors`: List of extra collectors to install and
  configure.
* `diamond_custom_collector_configs`: List of collectors that have extra
  configuration injected. (Elements of `diamond_custom_collectors` will get
  merged in, so you do not need to add them here)
* `diamond_effective_log_dir`: Directory where logs effectively get stored in.
* `diamond_metric_proxy_hosts_ssh`: (Default: []) Hosts to proxy
  metrics for that are reachable through ssh.
* `diamond_metric_proxy_hosts_jetdirect`: (Default: []) Hosts to proxy
  metrics for that expose a JetDirect web interface.
* `diamond_log_dir`: Directory proccesses will write logs to.
* `diamond_effective_data_disk`: Directory for data disk where data effectively
  gets stored in.
* `diamond_effective_data_dir`: Directory where data effectively gets stored in.
* `diamond_common_role_tasks_config`: See `docs/common-role-tasks.txt`.

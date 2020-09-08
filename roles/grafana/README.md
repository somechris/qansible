# Role: grafana



1. Description
2. Globals
3. Parameters



## 1. Description

Sets up Grafana. Grafana is a charting and dashboarding solution,
which we use to plot metrics data from Graphite.

Grafana gets set up and configured along with an Apache site exposing
it.



## 2. Globals

* `grafana_dashboard_dir`: The directory for provisioned dashboards.
* `grafana_web_host`: Domain at which Grafana is available



## 3. Parameters

* `grafana_initial_admin`: (Default: the global `admin_users`) The initial
  Grafana administrator to provision.
* `grafana_admin_password`: Administrator password (Not used when accessing
  through reverse proxy)
* `grafana_common_role_tasks_config`: See `docs/common-role-tasks.md`.
* `grafana_effective_data_disk`: Directory for data disk where grafana data
  effectively gets stored in.
* `grafana_effective_data_dir`: Directory where grafana data effectively gets
  stored in.
* `grafana_effective_log_dir`: Directory where grafana logs effectively get
  stored in.
* `grafana_effective_var_lib_dir`: Directory where grafana data underneath
  `/var/lib` effectively gets stored in.
* `grafana_log_dir`: Directory grafana proccess will write logs to.
* `grafana_log_level`: (Default: logging_default_log_level) Verbosity of logs
  and services. See `docs/logging.md`.
* `grafana_net_accesses`: (Default: []) List of net accesses of which hosts can
  reach the grafana server through the reverse proxy.
* `grafana_server_net_accesses`: (Default: []) List of net accesses of which
  hosts can directly reach the grafana server itself without going through the
  reverse proxy.
* `grafana_port`: Port at which Grafana runs behind the reverse proxy.
* `grafana_provisioning_dir`: Directory from where grafana picks up provisioning
  config files.
* `grafana_secret_key`: Used for signing within Grafana
* `grafana_sqlite_db`: (Default: `grafana.db`) Basename for the backend sqlite
  database.
* `grafana_var_lib_dir`: The directory underneath `/var/lib` associated to
  grafana.
* `grafana_websites_service_user`: (Default: `service-grafana`) The user Grafana
  uses to access other services. This user has to be in the
  `website_common_users` dictionary. (See `roles/website-common/README.md`)

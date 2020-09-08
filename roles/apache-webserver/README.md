# Role: apache-webserver



1. Description
2. Globals
3. Parameters



## 1. Description

Installs an Apache HTTPD webserver, configuring only the default
site. To configure further sites, see the `website-apache` role.



## 2. Globals

* `apache_webserver_log_level`: (Default: webserver_default_log_level) Verbosity
  of logs and services. See `docs/logging.md`.
* `apache_webserver_effective_data_disk`: Directory for data disk where data
  effectively gets stored in.
* `apache_webserver_effective_data_dir`: Directory where all data effectively
  gets stored in.
* `apache_webserver_effective_log_dir`: Directory where logs effectively get
  stored in.
* `apache_webserver_config_changed`: (Default: False) If true by the time this
  role runs, Apache will be told to pick up config changes. Roles that set up
  apache websites can set this to true to achieve a `notify` for Apache
  reloading, although the apache-webserver will get installed only later in the
  play.



## 3. Parameters

* `apache_webserver_common_role_tasks_config`: See `docs/common-role-tasks.md`.
* `apache_webserver_net_accesses`: The allowed incoming net-accesses
  for the server. Websites can restrict further, but cannot relax
  beyond these net-accesses.
* `apache_webserver_ports_plain`: The ports to listen on for
  unencrypted plaintext connections.
* `apache_webserver_ports_encrypted`: The ports to listen on for
  encrypted connections.
* `apache_webserver_error_documents`: Dictionary of overrides for
  Apache's default error pages. The keys are the status codes. The
  values are themselves dictionaries holding the following
  keys/values:
  * `reason`: A short, one-line, plain text description of the reason
    for this status page showing up. (E.g.: `Bad Request`)
  * `explanation`: A more detailed explanation of what happened.
* `apache_webserver_log_dir`: Directory that logs get written to.

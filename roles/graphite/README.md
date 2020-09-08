# Role: graphite



1. Description
2. Globals
3. Parameters



## 1. Description

Sets up Graphite backend and web application.



## 2. Globals

* `graphite_collection_host`: Domain name to which send gathered
  metrics.
* `graphite_line_receiver_port`: Port to which send gathered
  metrics.
* `graphite_host_prefix_wo_host`: The metric prefix left of the
  hostname.
* `graphite_host_prefix`: The full metric prefix including the
  hostname.
* `graphite_service_prefix_wo_service`: The metric prefix left of the
  service name.
* `graphite_web_host`: Domain name which offers the Graphite web
  application for querying and adhoc graphing.



## 3. Parameters

* `graphite_alternate_log_dir`: Secondary directory graphite proccess will write
  logs to.
* `graphite_cache_query_port`: The port to query the cache on.
* `graphite_database_backend`: The database backend to be used for
  Graphite. Currently supported values are:
  * `sqlite3` (default) for SQLite, and
  * `mariadb` for MariaDB databases.
* `graphite_database_host`: (default: '') The host to which connect for
  Graphite's database. Not used if `graphite_database_backend` is `sqlite3`.
* `graphite_database_password`: (default: '') The password to be used when
  connecting to Graphite's database. Not used if `graphite_database_backend` is
  `sqlite3`.
* `graphite_database_name`: (default: '{{graphite_var_lib_dir}}/graphite.db')
  The name of the database that Graphite should connect to. For `sqlite3`
  databases, this is the filename of the database file. For `mariadb` databases,
  this is the database name in the MariaDB server.
* `graphite_database_port`: (default: '') The port on which connect Graphite's
  database. Not used if `graphite_database_backend` is `sqlite3`.
* `graphite_database_user`: (default: '') The user as which to connect to
  Graphite's database. Not used if `graphite_database_backend` is `sqlite3`.
* `graphite_effective_carbon_log_dir`: Directory to store logs from carbon-cache
  application in.
* `graphite_effective_data_disk`: Directory for data disk where graphite data
  effectively gets stored in.
* `graphite_effective_data_dir`: Directory where graphite data effectively gets
  stored in.
* `graphite_effective_log_dir`: Directory where graphite logs effectively get
  stored in.
* `graphite_effective_var_lib_dir`: Directory where graphite data underneath
  `/var/lib` effectively gets stored in.
* `graphite_effective_whisper_dir`: Directory where whisper files effectively
  get stored in.
* `graphite_effective_webapp_log_dir`: Directory to store logs from the web
  application in.
* `graphite_log_dir`: Directory graphite proccess will write logs to.
* `graphite_log_level`: (Default: logging_default_log_level)
  Verbosity of logs and services. See `docs/logging.md`.
* `graphite_max_persisted_updates_per_second`: (Default: 500) The maximum number
  of metric updates to persist to disk per second. Updates that cannot get
  stored to disk, will be kept in memory and persisted later. Lowering this
  value reduced pressure on the disks, but also means that in case graphite or
  the host dies, some cached data might not yet have made it to disk and is
  lost.
* `graphite_common_role_tasks_config`: See `docs/common-role-tasks.md`.
* `graphite_service_users`: List of common web users to grant access. (See
  `website_common_htpasswds` of `roles/website-common/README.md`)
* `graphite_query_net_accesses`: List of net accesses of which hosts can reach
  the cache query service.
* `graphite_receive_net_accesses`: List of net accesses of which hosts can
  ingest metrics.
* `graphite_salt`: The salt graphite uses for auth tokens, CRSF, etc.
* `graphite_var_lib_dir`: The directory underneath `/var/lib` associated to
  graphite.
* `graphite_web_net_accesses`: List of net accesses of which hosts can reach
  the graphite web site.
* `graphite_whisper_dir`: Directory graphite will access whisper
  files through.

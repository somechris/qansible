Role: icinga-client
===================



1. Description
2. Globals
3. Parameters
4. Caveat



1. Description
--------------

Configures the host for monitoring by Icinga. `icinga-client-late` covers the
parts that relies on expanded variables. This role covers the part that does not
rely on expanded variables.



2. Globals
----------

No Globals that are specific only for this role.



3. Parameters
-------------

* `icinga_client_common_role_tasks_config`: See `docs/common-role-tasks.txt`.
* `icinga_client_ip_address`: The IP address to monitor the host at.
* `icinga_client_log_level`: (Default: logging_default_log_level) Verbosity of
  logs and services. See `docs/logging.txt`.
* `icinga_client_server_ip_address`: The IP address Icinga connects from.
* `icinga_client_server_net`: The key of net access that Icinga connects from.
* `icinga_client_net_accesses`: Default list of net accesses for
  `icinga_client_nrpe_net_accesses` and `icinga_client_ping_net_accesses`.
* `icinga_client_nrpe_server_port`: The port the NRPE server listens on.
* `icinga_client_nrpe_net_accesses`: List of net accesses of which hosts can
  reach the NRPE service.
* `icinga_client_ping_net_accesses`: List of net accesses of which hosts can
  ping the host.

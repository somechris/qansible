Role: ssh-server
================



1. Description
2. Globals
3. Parameters



1. Description
--------------

Sets up an ssh server.



2. Globals
----------

* `ssh_server_port`: The SSH Server listening port.



3. Parameters
-------------

* `ssh_server_common_role_tasks_config`: See `docs/common-role-tasks.txt`.
* `ssh_server_net_accesses`: List of net accesses of which hosts can reach
  the service.
* `ssh_server_log_level`: (Default: logging_default_log_level) Verbosity of logs
  and services. See `docs/logging.txt`.

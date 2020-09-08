# Role: vpn



1. Description
2. Globals
3. Parameters



## 1. Description

Sets up VPNs.



## 2. Globals

No Globals that are specific only for this role.



## 3. Parameters

* `vpn_common_role_tasks_config`: See `docs/common-role-tasks.md`.
* `vpn_effective_data_disk`: Directory for data disk where vpn data effectively
  gets stored in.
* `vpn_effective_data_dir`: Directory where vpn data effectively gets stored in.
* `vpn_effective_log_dir`: Directory where vpn logs effectively get stored in.
* `vpn_log_dir`: Directory vpn will write logs to.
* `vpn_log_level`: (Default: logging_default_log_level) Verbosity of logs and
  services. See `docs/logging.md`.
* `vpn_default_heartbeat_rate`: (Default: 10) Default period in seconds between
  sending heartbeats to the remote hosts.

# Role: atop



1. Description
2. Globals
3. Parameters



## 1. Description

Installs atop, which collects general host and process metrics. This
is useful to for example see which process used how much memory 5 days
ago on 11:50. Also, it servers as a backup of metric collection.



## 2. Globals

No Globals that are specific only for this role.



## 3. Parameters

* `atop_common_role_tasks_config`: See `docs/common-role-tasks.md`.
* `atop_effective_data_disk`: Directory for data disk where atop data
  effectively gets stored in.
* `atop_effective_data_dir`: Directory where atop data effectively gets stored
  in.
* `atop_effective_log_dir`: Directory where atop logs effectively get stored in.
* `atop_log_dir`: Directory atop proccess will write logs to.

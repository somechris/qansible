# Role: common-role-tasks-end



1. Description
2. Globals
3. Parameters



## 1. Description

Runs common tasks at role end, like configuring the firewall.



## 2. Globals

No Globals that are specific only for this role.



## 3. Parameters

* `common_role_tasks_end_config`: (Default: {}) See `docs/common-role-tasks.md`
* `common_role_tasks_end_parent_role`: (Default: Pick up from config) The name
  of the including role. This should not be set directly, but set it in
  `common_role_tasks_end_config` to ease re-use.

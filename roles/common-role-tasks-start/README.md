# Role: common-role-tasks-start



1. Description
2. Globals
3. Parameters



## 1. Description

Runs common tasks at role start, like guarding against unsuppported
distributions, and preparing directories.



## 2. Globals

No Globals that are specific only for this role.



## 3. Parameters

* `common_role_tasks_start_config`: (Default: {}) See `docs/common-role-tasks.md`
* `common_role_tasks_start_parent_role`: (Default: Pick up from config) The name
  of the including role. This should not be set directly, but set it in
  `common_role_tasks_start_config` to ease re-use.

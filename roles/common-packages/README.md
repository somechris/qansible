# Role: common-packages



1. Description
2. Globals
3. Parameters



## 1. Description

Installs common packages that should be installed on all systems and
do not need further configuration.

If a service needs to be started, that's ok.

But if configuration needs to be touched, please move the package into
a separate role.



## 2. Globals

No Globals that are specific only for this role.



## 3. Parameters

* `common_packages_common_role_tasks_config`: See `docs/common-role-tasks.md`.

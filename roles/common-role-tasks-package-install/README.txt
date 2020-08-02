Role: common-role-tasks-package-install
=======================================



1. Description
2. Globals
3. Parameters



1. Description
--------------

Runs common tasks to install packages, like installing the packages, and
assigning proper owners/groups for directories.



2. Globals
----------

No Globals that are specific only for this role.



3. Parameters
-------------

* `common_role_tasks_package_install_config`: (Default: {}) See `docs/common-role-tasks.txt`
* `common_role_tasks_package_install_parent_role`: (Default: Pick up from
  config) The name of the including role. This should not be set directly, but
  set it in `common_role_tasks_package_install_config` to ease re-use.

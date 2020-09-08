# Role: install-packages



1. Description
2. Globals
3. Parameters



## 1. Description

Brings installing packages to the role level. This helps when needing
to install packages before dependent roles are run.



## 2. Globals

No Globals that are specific only for this role.



## 3. Parameters

* `install_packages_name`: A name or list of names of the packages to
  install/uninstall.
* `install_packages_state`: The required state of the packages in
  `install_packages_name`.

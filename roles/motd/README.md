# Role: motd



1. Description
2. Globals
3. Parameters



## 1. Description

Add message-of-the-day line for an Ansible managed aspect/service.

This role helps making people aware which aspect/service of the host
that they log in is managed by Ansible.

Be liberal in using this service, and if in doubt, add a motd for a
role.



## 2. Globals

No Globals that are specific only for this role.



## 3. Parameters

* `motd_dir`: The directory to store the motd snippets in.

* `service_name`: The name of the service that should get marked as
  being managed by Ansible. `service_name` is free form and does not
  have to relate to a daemon or program. `service_name` dictates the
  name of the `motd` script that prints the description.

* `service_description`: (optional) (default: `service_name`) The
  textual representation of the service that should be marked as
  managed by Ansible. This is the text that users see when logging in.

* `state`: (optional) (default: `present`) Either `present`, or
  `absent`. If `present` the `motd` gets set up. If `absent`, the
  `motd` config for this role gets removed.

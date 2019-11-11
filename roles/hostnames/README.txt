Role: hostnames
===============



1. Description
2. Globals
3. Parameters



1. Description
--------------

Configures the system's hostnames.
Sets a host's hostname to the name from the Ansible inventory, and
makes sure it can be resolved.



2. Globals
----------

No Globals that are specific only for this role.



3. Parameters
-------------

* `hostnames_static`: A dictionary holding the additional static
  hostnames for the current host. The keys in this dictionary are the
  hostnames, the values are again dictionaries with the following
  key/values:
  * `ip`: The IP to resolve the name to.
  * `reason`: The explanation why this static hostname is needed

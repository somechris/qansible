Role: emergency-user
====================



1. Description
2. Globals
3. Parameters



1. Description
--------------

Sets up a dedicated local user that allows ssh to a given set of
users.



2. Globals
----------

No Globals that are specific only for this role.



3. Parameters
-------------

* `emergency_user_name`: The user name of the emergency user
* `emergency_user_authorized_keys`: Dictionary of SSH public keys that
  can log into the emergency user. The key of each entry is used as
  user name. The value is the list of public keys in ssh format.

Role: firewall-early
====================



1. Description
2. Globals
3. Parameters



1. Description
--------------

Sets up a basic restricted firewall to be used while setting up the
host. This restricted firewall allows to log in and install packages
from the internet, but it does not yet have ports open for
applications.



2. Globals
-------------

No Globals that are specific only for this role.



3. Parameters
-------------

* `firewall_early_rules_file`: Name of file to hold the restricted rule set.

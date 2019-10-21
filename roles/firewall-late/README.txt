Role: firewall-late
===================



1. Description
2. Globals
3. Parameters



1. Description
--------------

Sets up the system's firewall.



2. Globals
-------------

* `firewall_late_rules_file`: Name of file to hold the rule set.



3. Parameters
-------------

* `firewall_late_port_config`: Dictionary holding the configuration
  for the individual ports. The dictionary's keys are port numbers,
  and the values are the configuration for incoming packets on that
  port, which are again dictionaries. Each of these configuration
  dictionaries can have the following key/values:
  * `name`: The basename of the chain that holds this port's rules.
    `protocol`: The protocol (`tcp` or `udp`) to configure for.
    `incoming_net_accesses`: The white-listed incoming net-accesses.
  Each configured port per default logs and drops packets that are not
  explicitly white-listed.

  Each incoming packet that is not caught by a configured port gets
  silently dropped.

Role: ldap-client-late
======================



1. Description
2. Globals
3. Parameters



1. Description
--------------

The early part of ldap client configuration. See also the
`ldap-client-late` for the second part of the ldap client
configuration.



2. Globals
----------

* `ldap_client_late_default_login_groups`: Default list of ldap group
  names that can login on hosts. Those groups get full sudo on the
  host.



3. Parameters
-------------

* `ldap_client_late_host_specific_login_groups`: Host specific list of
  ldap group names that can login on a host. Those groups get full
  sudo on the host.

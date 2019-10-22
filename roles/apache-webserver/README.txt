Role: apache-webserver
======================



1. Description
2. Globals
3. Parameters



1. Description
--------------

Installs an Apache HTTPD webserver, configuring only the default
site. To configure further sites, see the `website-apache` role.



2. Globals
----------

No Globals that are specific only for this role.



3. Parameters
-------------

* `apache_webserver_net_accesses`: The allowed incoming net-accesses
  for the server. Websites can restrict further, but cannot relax
  beyond these net-accesses.
* `apache_webserver_ports_plain`: The ports to listen on for
  unencrypted plaintext connections.
* `apache_webserver_ports_encrypted`: The ports to listen on for
  encrypted connections.

Role: ldap-server
=================



1. Description
2. Globals
3. Parameters



1. Description
--------------

Sets up an LDAP server.



2. Globals
----------

* `ldap_server_base_dn`: The base `distinguised name` for the LDAP server. All
  LDAP entries stem from this one.
* `ldap_server_host`: The domain under which the LDAP server can be reached.
* `ldap_server_uri`: Full URI to the LDAP server
* `ldap_server_ou_groups`: Name of the organizational unit for groups
* `ldap_server_ou_people`: Name of the organizational unit for people
* `ldap_server_ou_machines`: Name of the organizational unit for machines
* `ldap_server_ou_services`: Name of the organizational unit for services
* `ldap_server_port`: The port the server listens on.
* `ldap_server_ssl_type`: The type of ssl setup to require



3. Parameters
-------------

* `ldap_server_admin_password`: Password for the LDAP admin account.
* `ldap_server_admin_salt`: Salt for the LDAP admin password.
* `ldap_server_common_role_tasks_config`: See `docs/common-role-tasks.txt`.
* `ldap_server_log_level`: (Default: logging_default_log_level) Verbosity
  of logs and services. See `docs/logging.txt`.
* `ldap_server_ldapscripts_log_file`: Log file for ldapscripts.
* `ldap_server_extra_schemas`: A list of schemas definitions to inject to the
  database. Each schema is defined as dictionary with the following key/values:
  * `cn`: The common name of the schema.
  * `attributes: A dictionary holding the attributes of the schema. The keys are
    the attribute names, the values are the attribute values.
* `ldap_server_mdb_access`: List of specifications of who can access resources.
* `ldap_server_net_accesses`: List of net accesses of which hosts can reach
  the service.
* `ldap_server_organization`: Name of the organization that the server is for.
* `ldap_server_password_scheme`: Passwordscheme used on the LDAP server.
* `ldap_server_uid_start`: First person uid.

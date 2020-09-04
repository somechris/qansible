Role: pop3-server
=================



1. Description
2. Globals
3. Parameters



1. Description
--------------

Installs an POP3 server for people to fetch their mail. The POP3
server serves mail from /var/mail to users. But the POP3 server does
not care how mail gets to /var/mail (see smtp-server role for getting
mail to /var/mail).



2. Globals
----------

No Globals that are specific only for this role.



3. Parameters
-------------

* `pop3_server_db_directory`: Directory holding the services databases.
* `pop3_server_common_role_tasks_config`: See `docs/common-role-tasks.txt`.
* `pop3_server_control_directory`: Directory to store mail UIDL
  information and similar things in.
* `pop3_server_index_directory`: Directory to store mail index
  information in.
* `pop3_server_effective_data_dir`: Directory where data effectively gets stored
  in.
* `pop3_server_effective_data_disk`: Directory for data disk where data
  effectively gets stored in.
* `pop3_server_effective_log_dir`: Directory where logs effectively get stored
  in.
* `pop3_server_log_dir`: Directory proccesses will write logs to.
* `pop3_server_log_level`: (Default: logging_default_log_level) Verbosity of
  logs and services. See `docs/logging.txt`.
* `pop3_server_net_accesses`: List of net accesses of which hosts can reach
  the service.
* `pop3_server_port`: The port to listen for initially unencrypted but
  STARTTLS enabled POP3 connections. If 0, this listener is disabled.
* `pop3_server_ssl_port`: The port to listen for encrypted
  connections. If 0, this listener is disabled.
* `pop3_server_users`: A dictionary holding user credentials for
  logins. The dictionary's keys are the allowed usernames. The
  corresponding values are again dictionaries having the following
  key/values:
  * `password`: The plain-text, unencrypted password for the user.
  * `salt`: The salt to encrypt the password with for storage on
    target host.
  * `net_accesses`: (Optional) If set, holds a list of net_accesses
    from which a user may connect (this can only restrict users
    further, but not add hosts that are not listed in
    `pop3_server_net_accesses`). If unset, the user may connect from
    any host in `pop3_server_net_accesses`.

# Role: ssh-connections



1. Description
2. Globals
3. Parameters



## 1. Description

Configures user's ssh settings on server and client to allow
connections over ssh keys. This role is limited to the user's
settings. It does not install ssh servers and it does not open
firewalls.



## 2. Globals

* `ssh_connections_available`: Is a dictionary holding the available ssh
  connections. The keys in this dictionary are id's for the connection. The
  private and public keys get picked up from `id_rsa-{{id}}` and
  `id_rsa-{{id}}.pub` in the `files` subdirectory of this role. The values of
  the dictionary are again dictionaries with the following key/values:
  * `client`: A dictionary defining the client side. This is a dictionary with
    the following key/values:
    * `host`: The client's host name.
    * `user`: The client's connecting user name.
  * `server`:
    * `host`: The server's host name.
    * `port`: (Default: ssh_server_port) The port to connect the server at.
    * `key`: The public part of the server's host key.
    * `key_type`: The type of the value at `key`.
    * `user`: The server's user name to connect to.
  * `options`: (Default: {}) A dictionary holding the ssh options to use for
    connecting. The keys are the options and the values the corresponding
    values. (E.g.: `{Ciphers: aes128-cbc}` would force using the aes128-cbc
    cipher to allow to talk to older routers)
  * `known_hosts_hex_salt`: (Default: undefined) If undefined, the
    server get added unencrypted to the client's known hosts file. If
    defined, has to be a 40 character hex string, and will gets used
    as salt when hashing the server host name.


## 3. Parameters

This role does not have parameters.

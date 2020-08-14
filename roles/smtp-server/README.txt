Role: smtp-server
==================



1. Description
2. Globals
3. Parameters



1. Description
--------------

Installs an SMTP server.



2. Globals
----------

No Globals that are specific only for this role.



3. Parameters
-------------

* `smtp_server_alias_files`: Dictionary holding data for alias files
  to render. Each key denotes a separate alias file. The name for the
  alias file is `/etc/mail/alias-{{key}}` (for the empty key, the
  trailing `-` gets dropped). The dictionary's value at the key holds
  the alias data, again in form of a dictionary. This dictionary's
  values hold lists of local parts that should get aliased to the
  corresponding key.
* `smtp_server_alias_files_defaults`: Defaults for
  `smtp_server_alias_files`.
* `smtp_server_alias_files_extra`: Additional custom alias file config.
* `smtp_server_dkim_domains`: List of domain names to render DKIM keys
  for.
* `smtp_server_domain_lists`: Dictionary of domain lists to set
  up. Each key holds the name of the domain list to set up, and the
  corresponding value holds a list of domain names to use for the
  domain list.
* `smtp_server_local_domains`: List of local domains to accept mail for.
* `smtp_server_localpart_lists`: Dictionary of localpartlists to set
  up. Each key holds the name of the localpartlist to set up, and the
  corresponding value holds a list of localparts to use for the
  localpartlist.
* `smtp_server_net_accesses`: List of net accesses of which hosts can reach
  the service.
* `smtp_server_net_accesses_defaults`: Defaults for
  `smtp_server_net_accesses`.
* `smtp_server_net_accesses_extra`: Additional custom net_accesses.
* `smtp_server_relay_net_accesses`: List of net accesses of which hosts can
  relay messages to this server.
* `smtp_server_relay_net_accesses_defaults`: Defaults for
  `smtp_server_relay_net_accesses`.
* `smtp_server_relay_net_accesses_extra`: Additional custom net_accesses.
* `smtp_server_relay_domains_from_host`: Dictionary allowing to fine
  tune which host can relay for which domain. Keys are IPs, and values
  are a list of domains this IP can relay for on this server.
* `smtp_server_routers`: A list (not a dictionary since the order is
  crucial here) holding router config. Each entry is a dictionary
  configuring a single router. Each config dictionaries can hold the
  following key/values:
  * `name`: Identifier for the router.
  * `driver`: The driver to use for the router (E.g.: `accept`, or
    `redirect`)
  * `local_parts`: (Optional) Either a single local part, or a list of
    local parts.
  * `domains`: (Optional) The router's domains.
  * `local_part_prefix`: (Optional) The prefix to strip from local parts.
  * `local_part_suffix`: (Optional) The suffix to strip from local parts.
  * `aliases`: (Optional) The key in `smtp_server_alias_files` of the
    alias file to resolve local_parts by.
  * `redirect_to`: (Optional) (Only if driver is 'redirect') The email
    address to redirect to.
  * `unseen`: (Default: False) The message gets duplicated. One copy
    is processed by this router, and the other copy continues with the
    remaining routers as if it had not been matched by this router.
* `smtp_server_port`: The port to listen for initially unencrypted but
  STARTTLS enabled SMTP connections.
* `smtp_server_port_ssl_config`: The name for the ssl_config to set up
  on the main port.
* `smtp_server_extra_port_ssl_config`: The name for the ssl_config to
  set up on the extra ports.

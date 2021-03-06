# Role: apache-website



1. Description
2. Globals
3. Parameters



## 1. Description

One-stop role for setting up an Apache web site.

Along with the web site itself, an Apache HTTPD server will get set up and
configured (see `apache-webserver` for details).

The web site defaults to get served from `{{web_site_root_dir}}/{{apache_website_domain}}/htdocs/`.

The site listens on port 80 (http) and 443 (https) per default and the
http site does is forwarding to the https site.

Logs go to the apache log dir into the files `{{apache_website_domain}}/$PORT_{error,access}.log`.

Https uses the x509 certs for `{{apache_website_domain}}` (see role `x509-server-cert`.



## 2. Globals

No Globals that are specific only for this role.



## 3. Parameters
* `apache_website_common_role_tasks_config`: See `docs/common-role-tasks.md`.
* `apache_website_htpasswds`: (optional) (default: {}) See `website_common_htpasswds`
  of the `website-common` role.
* `apache_website_locations`: (optional) (default: empty) List of location
  definitions. Each item is a dictionary holding:
   * `alias`: (Default: '') (Optional) If set, configures the location as alias
     for this file/directory on the file system.
   * `auth`: If defined, specifies the authentication/authorization for this
     location as dictionary. The available key/values are:
     * `ldap-groups`: A list of LDAP group names. The user is authorized, if it
       is any of them.
     * `htpasswds`: A list of htpasswd files. The user is authorized, if it is
       in any of them. See the `apache_website_htpasswds` to define them.
     The user is considered authorized, if they are authorized according to any
     of the configured authorizations. So for example if a location defines both
     `ldap-groups` and `htpasswds`, a user in an ldap-group is considered
     authorized, even if they are not in a htpasswd file and vice versa.

     Authorization requirements are merged with parents. So if for example
     membership in the group `staff` is required for `/foo`, and group
     `analytics` for `/foo/bar`, then one needs to be both in `staff` and
     `analytics` to access `/foo/bar`. (This helps to avoid accidentally nixing
     net_access requirements on parents)

     Note though, that mixing auth backends across different locations where one
     contains the other does not work well. So if '/foo' requires an ldap-group
     and `/foo/bar` requires a htpasswd, even users that are in both the
     ldap-group and the htpasswd will fail to authorize. But if `/foo` would
     also rely on a htpasswd or if `/foo/bar` would rely on an ldap-group (so
     both `/foo` and `/foo/bar` are on the same backend, users can log in.
   * `auth_merging`: (Default: And) How auth requirements trickle down to
     defined sublocations. So if for example location `/foo` and `/foo/bar` both
     define Requires (ldap-groups, net-accesses, ...), this setting defines how
     these Requires affect urls under `/foo/bar`. If `And`, the requirements of
     both `/foo` and `/foo/bar` have to hold to get access underneath
     `/foo/bar`.  If `Or`, the requirements of both `/foo` or `/foo/bar` have to
     hold to get access underneath `/foo/bar`. If `Off`, the requirements on
     `/foo` are ignored and only the requirements of `/foo/bar` are relevant.
   * `cors`: (Default: ``) (Optional) If `allow-all-simple`, white-list simple
     requests through CORS.
   * `cacheable`: (Default: ``) (Optional) If set and false, send response
     headers that prohibit caching. If unset or true, no dedicated cache headers
     get sent.
   * `deny`: (Default: False) (Optional) If True, unconditionally deny
     all requests to this location.
   * `expose_server_status`: (Default: False) (Optional) If True, return the
     server status for requests to this location.
   * `is_cgi`: (Default: Undefined) If undefined, do not interfer with cgi
     config. If True, treat this location as cgi and allow to execute them. If
     False, do not allow executing cgi scripts.
   * `name`: The location's URL.
   * `net_accesses`: The net-accesses that may use the location
   * `proxy`: Proxies requests to this location to a backend
     server. The value at this key has to be a dictionary with the
     following key/values:
     * `host`: (Default: `localhost`) The IP address or host name of the backend
       server.
     * `path`: (Default: `/`) The path to proxy to on the backend server.
     * `port`: The port number to connect the backend server on.
     * `protocol`: (Default: `http`) Protocol to use to connect to the backend
       server. Typically `http` or `https`.
   * `security_rules`: List of security adaptions for this
     location. Each security adaption is a dictionary with the
     following key/values:
     * `actions`: For type `add-rule`, the list of actions to carry out on a
       match. If `actions` is the string `standard-deny`, it will get expanded
       to denying the request at severity `CRITICAL`.
     * `id`: The id of the adaption. For type `remove-target`, the id gives
       the rule to remove a target from.
     * `operator`: For `add-type`, the operator to match with against the
       `targets` (E.g.: `@rx ^(?i:file)://(.*)$`).
     * `phase`: (Default: 2 for type `add-rule`, 1 otherwise) The phase in which
       the rule should be applied. Either 1 or 2.
     * `rationale`: The plain text rationale why the adaption is necessary.
     * `targets`: For type `remove-target`, `targets` is the list of targets
       to remove from the security rule `id` for this location. For type
       `add-rule`, it is the list of targets to match against. (E.g.:
       ['ARGS:url', 'REQUEST_URI'])
     * `type`: The type of adaption. Possible adaptions are:
       * `add-rule`: adds a new rule
       * `append-to-variable`: appends a value to a variable
       * `remove-target`: removes targets from an existing rule
       * `set-variable`: sets a variable to a value
     * `value`: The value set or append, in types `append-to-variable` and
       `set_variable`.
     * `variable`: The name of the variable to set or append to, in types
       `append-to-variable` and `set_variable`.
   * `type`: (Default: `static`) If `static`, `name` is the literal
     name of the location to match. If `regexp` take `name` as
     regular expression to match with. This regular expression will
     automatically be anchored to the path start.
* `apache_website_add_www_redirects`: If True, sets up a
  `www.{{apache_website_domain}}` site that redirects to
  `{{apache_website_domain}}`.
* `apache_website_domain`: The domain name of the web site that should be served.
* `apache_website_is_https`: If True, the main site is served through
  https (with certs brought into place automatically) and http
  requests will get redirected to https automatically. If not True,
  the main site is http and no certs or https sites get set up.
* `apache_website_log_anonymously`: If True, avoid logging URLs, IPs,
  or headers. Client serials and usernames will get logged, as these
  indicate special users.
* `apache_website_net_accesses`: The net-accesses that can access this
  site. This can be more restrictive that
  apache_webserver_net_accesses (note the name `server`, not `site`),
  but not more permissive.
* `apache_website_redirects`: A list of redirects to set up for this
  site. Each redirect is a dictionary, holding the following
  key/values:
  * `from`: The match that triggers the redirect
  * `to`: The URL to redirect to
* `apache_website_rewrites`: A list of rewrites to set up for this
  site. Each rewrite is a dictionary, holding the following
  key/values:
  * `description`: (Optional) Description of this rewrite's purpose.
  * `conditions`: (Optional) A list of conditions that all need to be
    matched for the rewrite to become effective. Each condition is a
    dictionary holding the following key/values:
    * `string`: The string to match in.
    * `condition`: The condition that has to hold for the `string`.
  * `rule`: a dictionary holding the following key/values:
    * `from`: A match for the part of the current URI to rewrite.
    * `to`: The target to rewrite to.
    * `flags`: A list of flags for this rewrite rule (E.g.: `['END']`)
* `apache_website_log_level`: (Default: apache_webserver_log_level) Verbosity of
  logs and services. See `docs/logging.md`.
* `apache_website_mod_configs`: (optional) (default: {}) A dictionary for
  configs for additional server mods. The keys of this dictionary are the names
  of the mod, (E.g.: `wsgi`) and the corresponding values hold the config for
  that module. Possible key/values are:
  * `wsgi`: Configures a WSGI site. The value is a list of configuration lines
    to add to the VirtualHost. Each line has to start in `WSGI`. Configuring
    wsgi automatically switches cgi scripts to wsgi for this VirtualHost.

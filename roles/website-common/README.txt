Role: website-common
====================



1. Description
2. Globals
3. Parameters
4. Caveat



1. Description
--------------

Handles common aspects of websites that are not specific to the used
web server (E.g.: www directories, htpasswd files).



2. Globals
----------

No Globals that are specific only for this role.



3. Parameters
-------------
* `website_common_domain`: The domain to host
* `website_common_kind`: The kind of webserver (E.g.: `nginx`, `apache`)
* `website_common_htpasswds`: (optional) (default: []) List of
  htpasswds to set up. Each htpasswd is modelled as dictionary having
  the following key/value pairs:
  * `name`: Name of the htpasswd file to render.
  * `users`: List of usernames to add to the htpasswds. Pick them from
    `website_users` key from the roles' credentials file.
* `website_common_is_https`: If True, the main site is prepared to get
  served through https (E.g.: will have certs brought into place
  automatically).
* `website_common_add_www_redirects`: If True, the requirements for
  `www.{{website_common_domain}}` site are set up (E.g.: certs if it
  is a https site)

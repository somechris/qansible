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
* `website_common_htpasswds`: (optional) (Default: {}) Dictionary of htpasswds
  to set up. The key is the name of the htpasswd file, and the value is a list
  of usernames to add to the htpasswds. Pick them from the key set of the
  `website_common_users` dictionary in this roles' credentials file.
* `website_common_is_https`: If True, the main site is prepared to get
  served through https (E.g.: will have certs brought into place
  automatically).
* `website_common_add_www_redirects`: If True, the requirements for
  `www.{{website_common_domain}}` site are set up (E.g.: certs if it
  is a https site)
* `website_common_users`: a dictionary of common static users for our
  websites. The key is the username. The values are again dictionaries with the
  following key/values:
  * `comment`: A comment for the user.
  * `password`: The plaintext password for this user.
  * `salt`: A salt to hash the password with.

Role: static-website
=================



1. Description
2. Globals
3. Parameters



1. Description
--------------

Deploys a static html page from S3.



2. Globals
-------------

* `static_website_list`: List of dictionaries, each describing a deployed
  static website on this host. Each dictionary has the following keys:
  * `domain`: The domain that got deployed.
  * `build`: The build number of the deployed domain.



3. Parameters
-------------

* `static_website_artifact_domain`: (Default: '{{static_website_domain}}')
  The artifact domain to host the site with. Typically, the default
  should be good enough as it picks the artifact that matches the
  hosted domain. But is some cases (E.g.: PCE) a single artifact will
  be used to host a variety of different domains. This setting allows
  to achieve that.
* `static_website_build`: The build/commit to deploy (E.g.: 18.467dcd6)
* `static_website_default_locations`: The default locations to set
  up. This parameter is not meant to be overridden, and only helps to
  deduplicate when switching web servers as long as Ansible does not
  allow parametric role names. If you need to provide custom
  locations, use `static_website_locations` instead.
* `static_website_locations`: (Default: []) Additional locations to set
  up for the web site. This parameter has to be in the format used by
  by the role selected through `static_website_server_flavor`.
* `static_website_server_flavor`: (default: apache) Specifies which
  web server to use to serve the site. Currently, only `apache` is
  supported here.
* `static_website_htpasswds`: htpasswds configuration for the web
  servers. This parameter has to be in the format used by by the role
  selected through `static_website_server_flavor`.
* `static_website_domain`: Domain name which to deploy and serve at.
* `static_website_net_accesses`: The net-accesses that can access this
  site. This can be more restrictive than the webserver's net_accesses,
  but not more permissive.

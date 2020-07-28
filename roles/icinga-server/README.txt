Role: icinga-server
===================



1. Description
2. Globals
3. Parameters
4. Caveat



1. Description
--------------

Sets up an Icinga server along with an Icinga 1 web application.



2. Globals
----------

* `icinga_server_web_host`: The domain name to serve the web application at,
  and the domain name from whose IP address NRPE calls are made.
* `icinga_server_object_path`: The directory holding the object configuration
  files.
* `icinga_server_preconfigured_web_host_health_checks`: Dictionary that defines
  how to perform web domain checks. For a domain `foo.bar.baz`, the checks defined
  by the following keys get added up (with the later overruling the earlier
  ones): `foo`, `foo.bar.baz`. The value for each key is again a
  dictionary holding the following key/value pairs:
    * `alias`: (Default: None) Merges the definition of another web host check
      in. So if the value of `alias` is `foo`, then the definitions of
      `icinga_server_preconfigured_web_host_health_checks['foo']` get added in.
    * `protocols`: (Default: ['https', 'http']) The list of protocols offered by
      this server. (See `protocol` of the individual checks to see how to
      specify which protocol gets used for a check). If 'https' is contained, a
      check for certificate expiration is added automatically. If both 'http'
      and 'https' is present, a check that 'http' requests get forwarded to
      'https' urls gets added.
    * Each of the remaining key is considered the name of a check and the
      corresponding value in a dictionary that sepecifies how to check. It's
      key/values are:
      * `data`: (Default: 'None') The encoded data to send along with the
        request.
      * `encode_data`: (Default: 'None') The unencoded data to send along with
        the request. The data will get encoded automatically.
      * `expected_status_code`: (Default: 200) The response status code needed
        to pass the check.
      * `expected_content`: (Default: '') The content that needs to be in the
        response to pass the check.
      * `method`: (Default: 'GET') The HTTP method to use for the check. Only
        `GET` and `POST` are supported at this time.
      * `port`: (Default: None), If `None`, request on the default port for the
        used protocol. Otherwise request on the given port.
        `http`) The protocol to check on.
      * `protocol`: (Default: 'https' if the web host offers https, otherwise
        `http`) The protocol to check on.
      * `uri`: (Default: '/') The uri to check.
      * `variant`: (Default: '') If empty, warn above 1 second response. If
        `slow`, warn above 3 seconds response time.
  This dictionary only defines the checks, but does not run or enfocrce them. To
  run the checks, add the relevant, fully qualified domains to for example
  `icinga_server_virtual_external_domains`, and
  `icinga_server_virtual_internal_domains`



3. Parameters
-------------

* `icinga_server_command_dir`: The directory holding the command file.
* `icinga_server_command_file`: The command file. This file can be used to
  inject commands into Icinga.
* `icinga_server_contact_groups`: A dictionary whose keys hold the contactgroups
  that should get generated, and whose corresponding values are lists of members
  to those groups.
* `icinga_server_htdocs_dir`: The directory holding Icinga's htdocs
* `icinga_server_net_accesses`: List of net accesses of which hosts can reach
  the service.
* `icinga_server_virtual_external_domains`: List of domains that are considered
  publicly accessible and should be monitored. Each of these are checked from
  the Icinga server according to the checks specified in
  `icinga_server_preconfigured_web_host_health_checks`
* `icinga_server_virtual_internal_domains`: List of domains that are considered
  only internally visible and should be monitored. Each of these are checked
  from the Icinga server according to the checks specified in
  `icinga_server_preconfigured_web_host_health_checks`



4. Caveat
---------

Note: This role relies on the add-host-to-group role, which means that group
setting is done in a run_once like manner. See the add-host-to-group's
README.txt for more details.

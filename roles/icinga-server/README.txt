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



3. Parameters
-------------

* `icinga_server_command_dir`: The directory holding the command file.
* `icinga_server_command_file`: The command file. This file can be used to
  inject commands into Icinga.
* `icinga_server_contact_groups`: A dictionary whose keys hold the contactgroups
  that should get generated, and whose corresponding values are lists of members
  to those groups.
* `icinga_server_htdocs_dir`: The directory holding Icinga's htdocs
* `icinga_server_log_level`: (Default: logging_default_log_level) Verbosity of
  logs and services. See `docs/logging.txt`.
* `icinga_server_net_accesses`: List of net accesses of which hosts can reach
  the service.



4. Caveat
---------

Note: This role relies on the add-host-to-group role, which means that group
setting is done in a run_once like manner. See the add-host-to-group's
README.txt for more details.

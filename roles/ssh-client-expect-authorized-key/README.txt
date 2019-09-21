Role: ssh-client-expect-authorized-key
======================================



1. Description
2. Globals
3. Parameters



1. Description
--------------

Sets up expectations for users on the presence of private authorized keys,
and allows public authorized keys.



2. Globals
----------

* `ssh_client_expect_authorized_key_collector`: Dictionary holding all
  authorized key expectations for the host. For each entry in this
  dictionary, the key is the username, and the value is a list
  of authorized keys in ssh format.



3. Parameters
-------------

* `ssh_client_expect_authorized_key_expectation`: Dictionary of
  expectations to add to the already collected expectations. The
  format of this dictionary are the same as for
  `ssh_client_expect_authorized_key_collector`.

Role: gnupg-public-key
======================



1. Description
2. Globals
3. Parameters



1. Description
--------------

Installs a gnupg public key to the `root`'s GnuPG keyring

The key material has to be available in the
`{{gnupg_public_key_name}}-{{gnupg_public_key_id}}-public.asc` file as
ASCII armored public key.

2. Globals
----------

No Globals that are specific only for this role.



3. Parameters
-------------
* `gnupg_public_key_name`: The name of the public key. If the key has a
  UID with an associated email address, use that email address as
  name. (E.g.: `do-not-reply.host-auditor@development.environment`)
* `gnupg_public_key_id`: The key's short key id in hex. (E.g.: `0xF3AB5A00`)
* `gnupg_public_key_add_to_keyring`: (Default: True) If True, adds key
  to keyring.

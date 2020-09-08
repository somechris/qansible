# Role: remote-apt-repository



1. Description
2. Globals
3. Parameters



## 1. Description

Adds a remote APT repository for Debian-based systems as package source.



## 2. Globals

No Globals that are specific only for this role.



## 3. Parameters

* `remote_apt_repository_components`: (Default: ['main']) The list of components
  to import.
* `remote_apt_repository_distribution`: The codename of the distribution for
  this apt repository
* `remote_apt_repository_has_sources`: (Default: False). If True, configure
  package sources as well.
* `remote_apt_repository_signing_key_id`: The short id GnuPG key packages are
  signed with. (See role `gnupg-public-key`)
* `remote_apt_repository_signing_key_name`: The name of GnuPG key packages are
  signed with. (See role `gnupg-public-key`)
* `remote_apt_repository_url`: The url to pick up packages from
* `remote_apt_repository_name`: (Default: The URLs domain, stripped of
  first and last component) The basename of file name to use in the
  sources directory.

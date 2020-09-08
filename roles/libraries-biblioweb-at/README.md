# Role: libraries-biblioweb-at



1. Description
2. Globals
3. Parameters



## 1. Description

Integrates data from Biblioweb.at libraries.



## 2. Globals

No Globals that are specific only for this role.



## 3. Parameters


* `libraries_biblioweb_at_accounts`: Is a dictonary of library configs. In this
  dictionary, the keys are the ids for the library accounts, (which will get
  used for metric names), and the values are the corresponding configs. These
  are again dictionaries with the following key/values:
  * `library`: (Default: the account id) The biblioweb id for the library to
    fetch data for. (This is typically the lowercase name of the place the
    library is in)
  * `user`: The username of the account to fetch data for
* `libraries_biblioweb_at_passwords`: Is a dictonary of passwords for
  libraries. The keys correspond to the keys of
  `libraries_biblioweb_at_accounts` and the values are the corresponding
  passwords to authenticate with.

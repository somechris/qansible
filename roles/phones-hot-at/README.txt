Role: phones-hot-at
===================



1. Description
2. Globals
3. Parameters



1. Description
--------------

Integrates data from hot.at phones.



2. Globals
----------

No Globals that are specific only for this role.



3. Parameters
-------------


* `phones_hot_at_accounts`: Configurations for hot.at accounts. This a
  dictionary where the keys are the ids of the accounts and the values are the
  corresponding configurations. The following key/values are supported:
  * `pop`: Configuration of a pop account to fetch login url emails from. This is
    dictionary with the following key/values.
    * `host`: The host of the POP3 server to connect to.
    * `port`: The port to connect the POP3 server at.
    * `user`: The username to connect the POP3 server as.
    (For password, see `phones_hot_at_pop_passwords`)
  * `email`: The email to request an login token for.
  * `aliases`: A mapping from phone numbers to descriptive names. These names
    will get used as metric names. This mapping is a dictionary. The keys are
    the phone numbers and the values the corresponding names.
* `phones_hot_at_pop_passwords`: A dictionary providing passwords for pop
  accounts. The keys are the ids of `phones_hot_at_accounts`, and the values are
  the corresponding passwords.

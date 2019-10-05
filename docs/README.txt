1. Quickstart
2. Big picture
3. Role overview



1. Quickstart
-------------

* DO NOT ADD PASSWORDS, PRIVATE PRODUCTION KEYS OR OTHER STRONGLY
  SENSITIVE DATA TO THIS REPOSITORY!
  (see `passwords.txt`)
* DEPLOYING CONFIG CHANGES CAUSES AUTOMATED SERVICE RESTARTS!
  (see `hacking.txt`)
* If you commit something, deploy it
  (see `hacking.txt`)
* Install Ansible on your local machine (E.g.: `apt-get install ansible`)
* If your LDAP user name differs from your current user name on your
  current host, of if you do not have your LDAP ssh key in the default
  place:
    - Copy common.inc.local.example to common.inc.local
    - Edit common.inc.local to reflect your LDAP user name and ssh
      key.
* Either
   - Run `mkdir private-production`, or
   - Get a clone of the private password repository.
* ./ansible-playbook.sh --become -i production site.yml --tags TAG_YOU_WANT_TO_DEPLOY

If TAG_YOU_WANT_TO_DEPLOY is a tag that only affects client
configuration, the above should be sufficient. If you want to deploy
server configuration, you also need the private password repository
(See `passwords.txt`)

If you want to limit the deploy to certain hosts add `--limit
host.domain.org` to the above command.

So for example if you only want to deploy only the tasks tagged as
`red` to `redp02.domain.org`, you can run:

```
./ansible-playbook.sh --become -i production site.yml --limit redp02.domain.org --tags red
```


2. Big picture
--------------

In our Ansible setup, tasks (E.g.: Installing a package, or copying a
file) are collected in roles (E.g.: Setting up a web server). Roles
are collected in rolebooks (E.g.: Cascade, or Conifer). All rolebooks
are collected in the main entry point `site.yml`.

We always run Ansible against the main `site.yml` file.
So fore example:

```
./ansible-playbook.sh --become -i production site.yml
```

would redeploy everything.

To run only a given role, we still use the main `site.yml` and
restrict needed tasks by using tags. For example

```
./ansible-playbook.sh --become -i production site.yml --tags icinga
```

would only run the tasks that are specific to icinga.

To only run against some hosts, one can use groups (defined in the
`production` file in the root of your checkout) like

```
./ansible-playbook.sh --become -i production --limit appFoos --tags icinga
```

to only run the icinga tasks for the hosts running a AppFoo. One can
also limit to a single host, like

```
./ansible-playbook.sh --become -i production --limit app-foo-01.domain.org --tags icinga
```

to only run the icinga tasks for `app-foo-01.domain.org`.

The main entry point `site.yml` is in your checkout's root directory.
Rolebooks are in the `rolebooks` directory.
Role definitions are in the `roles` directory.
For each role, the corresponding tasks are in the `tasks` subdirectory
of a given role.

To get you set up with a development environment, see
`development.txt`.

Before hacking away, see `hacking.txt` for common conventions and
agreements.



3. Role overview
----------------

* Roles:
  - `common-packages`: Sets up common packages needed on all hosts.
  - `dhparams`: Handles files holding Diffie Hellman parameters for secure
    handshakes. This is needed for applications doing encryption (Websites,
    LDAP, ...)
  - `emergency-user`: Sets up a local user that allows login even if
  - `firewall-early`: Sets up a basic firewall to be used while setting up the
    host
  - `firewall-late`: Sets up the system's firewall
  - `hostname`: Sets up host identifications.
  - `motd`: Sets up motd (message of the day) files shown after login. This is
  - `network-tuner`: Adjusts settings of network interfaces.
  - `ssh-client-expect-authorized-key`: Configures expected authorized
    keys for ssh clients.
  - `ssh-server`: Sets up an SSH server
  - `x509-cert`: Installs an X.509 certificate

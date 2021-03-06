Coding conventions:

* DO NOT ADD PASSWORDS, PRIVATE PRODUCTION KEYS OR OTHER STRONGLY
  SENSITIVE DATA TO THIS REPOSITORY!

  Sensitive data should go into the private repository and only get
  symlinked here. See `passwords.md`.

  (Note that this is for production data. Adding /development/ keys is
  fine, it's even expected to pit them underneath
  `private-development`)

* DEPLOYING CONFIG CHANGES CAUSES AUTOMATED SERVICE RESTARTS

  All Ansible code restarts applications upon need. For example if you
  deploy configuration changes for a service, the service will get
  restarted right away.

  For some services (like Pines), restarting takes some time and needs
  coordination. If you change some settings, deploy them. But
  /carefully/ deploy them.

  For example only during scheduled maintenance, or (if there is
  fail-over) only one host at a time.

  (Do not commit changes without deploying them. See item `If you
  commit something, deploy it`)

* If you commit something, deploy it.

  Ansible should describe what we have deployed. And deployments
  should work.

  When committing changes without deploying them, we break both of the
  above selling points.

  So if you commit something: Deploy it.

  (Deploying on a test host is not enough. You have to deploy it to
  the whole cluster)

* Use roles.

  Do not put tasks into files in the top level directory. This helps a
  lot to structure things, and fosters re-use.

* Make roles idempotent.

  The outcome of deploying a role once, or deploying the role twice
  should be the same. This is especially important if you have to run
  commands to setup services.

  The reason for this convention is that it should always be safe to
  redeploy a role.

* Deploying a service's role must not delete live user data.

  So if a role `foo` got used to set up a service, and the service has
  seen usage and added new data, then deploying the role `foo` again
  must not overwrite the added data.

  The reason for this convention is that it should always be safe to
  redeploy a role.

* Do not add large files to the repository.

  Think hard if Ansible is the right place before adding files >10K.
  Think extra hard if Ansible is the right place before adding files >100K.
  Positively, do not add files >1MB.

  It will only slow down initial cloning and working with the repo.
  Ansible should not be used to bring huge files to the hosts.
  If you need to deploy huge files, use this repo's reprepro. So
  debianize the needed huge files, and deploy them through apt-get.

* No configure, and no compiling through Ansible

  Tools like make, gcc, ... only increase our attack surface, hence we
  do not want to have them on production machines. If you need to
  compile something, please debianize the software and use reprepro
  and apt-get to install it.

* Where applicable, split roles into -client and -server

  For services that have a server and client aspect, use a
  `...-server` and `...-client` role instead of doing a single role
  with complicated `when` settings.

  Thereby, it becomes clearer which aspects are expected on which host.

* Do not add system prefixes in new role names per default. Those
  prefixes are likely to run stale, so we prefer to not have them for
  future roles. So do not use `conifer-red`, but use `red` instead.

  The only place where we use prefixes, is where names would be
  ambiguous/misleading without the prefix. For example we prefer
  'cascade-monitors' over 'monitors' as name, as 'monitors' on its own
  would likely make Ops-minded people think of Nagios/Icinga, which
  would be misleading.

* Restrict variables names to lowercase letters, numbers and underscores.

  Other characters (like dashes '-') get interpreted
  counter-intuitively in certain circumstances (e.g.: `foo-bar` as
  subtracting the variable `bar` from the variable `foo`). Hence, we
  want to avoid such characters in variable names.

  (This It's ok to have '-' in group names, as they are used as strings)

* Start variable names in the role name followed by '_'

  (And replace '-' in the role name by '_')
  That way, if one role uses a variable from another role, it becomes
  clear, where the value is coming from, where changes should go, and
  where to find documentation.

* Start registered names in the role name followed by '_reg_'

  (And replace '-' in the role name by '_')
  That way, if one role uses the registered name, it becomes clear,
  where the value is coming from, where changes should go, and where
  to find documentation.

* Start role facts in the role name followed by '_fact_'

  (And replace '-' in the role name by '_')
  That way, if one role uses the fact from another role, it becomes
  clear, where the value is coming from, where changes should go, and
  where to find documentation.

* Do not use IP addresses, use hostnames

  It's hard for people to recall/remember which IP address corresponds
  to which host. E.g.: If you see `10.198.2.150` in some config file,
  which host does this refer to?

  So where possible, use the hostname instead of IPs.
  (E.g.: `host-foo.domain.org` instead of `10.198.2.150`)

  If some config does not allow to used hostnames, use the IP address,
  and add a comment that says which host it refers to.

  When using IP addresses, do not type them in as strings, but use
  host_vars that hold the needed value. E.g.: Use
  host-foo.domain.org's host_var ec2_private_ip_address
  instead of entering 10.198.2.150 directly)

  The only exception being 127.0.0.1, which is a well-known and
  constant entity, and can be used as is.

* If, when writing a role, say `foo`, you rely on the tasks of another
  role, say `bar`, that is later in `site.yml`, do not add a
  dependency of `foo` on `bar`, as that would lead to running `bar`
  more than once or unpredictable when running the whole
  `site.yml`. Instead either move `bar` to an earlier place in
  `site.yml`, or split off the part of `bar` that you need in a
  dedicated role that you can add to `common-early.yml` (or something
  similar). That way, the needed parts of `bar` get run before `foo`,
  and the flow of `site.yml` is straightened out.

* Follow common best-practices in coding. Especially:

  * YAGNI - You ain't gonna need it
    https://en.wikipedia.org/wiki/You_aren't_gonna_need_it

  * DRY - Don't repeat yourself
    https://en.wikipedia.org/wiki/Don't_repeat_yourself

* Mark todos only with ` TODO: ` (without quotes)

* When adding a role, add a short description of the role to
  `doc/README.md`.

* Before pushing code, make sure the `lint.sh` passes fine on each of
  the new commits.

* If you notice that someone manually changed Ansiblized files in
  production, or did something that would get paved over by Ansible,
  remove the corresponding part from Ansible immediately.

  (We've tried warning one another "Do not roll out $X due to manual
  changes", but this process is too brittle. So we rather remove it
  from Ansible than paving over things unintendedly)

* When using templates, make sure the template file name ends in `.j2`
  (for Jinja2). Also indicate the type of file with an appropriate
  ending before the `.j2`. For example `foo.sh.j2` would be a shell
  script template.

  This naming convention helps to clarify which files are templates,
  helps with grepping in task files and also allows type specific
  linting (E.g.: shell linting for a shell template).

* When rendering templates on the target system, drop the `.j2`
  ending. If it's an executable file, also drop the type marker.
  So if you render `foo.sh.j2` into `/usr/bin` on a target host, use
  `/usr/bin/foo` as target name.

  This convention helps to reap type benefits in our Ansible repo
  itself while avoiding to leak cruft to target hosts.

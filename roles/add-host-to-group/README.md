# Role: add-host-to-group



1. Description
2. Globals
3. Parameters
4. Caveat



## 1. Description

Dynamically adds hosts to groups in Ansible.

Ansible's add_host is tricky to use right, and the `with_items` does
not work exactly as one would want it to work (see Caveat section
below). Hence, we use a dedicated group for adding hosts to groups, so
we have the necessary code in one place instead of having it scattered
across the code base. That way, it suffices to add fixes or further
workarounds of this brittle piece of code in one place instead of
having to duplicate them wherever we need to dynamically add hosts.



## 2. Globals

No Globals that are specific only for this role.



## 3. Parameters

* `add_host_to_group_new_group`: (Default: '') The group(s) to add the play
  hosts (see Caveat below) to. Has to be empty, or a single group name. Use this
  parameter, if you only want to add the hosts to a single group.
* `add_host_to_group_new_groups`: (Default: []) A list of group(s) to add the
  play hosts (see Caveat below) to. Has to be a string. Groups have to be comma
  separated. Use this parameter, if you want to add a host to multiple groups in
  one go.


## 4. Caveat

Since core's `add_host` is by-passing the host loop, this role
adds all hosts in the play set to the group (not only those that match
an intermediate conditional), and the first node in the play_hosts list
must not be excluded by a conditional.

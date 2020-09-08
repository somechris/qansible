* Install through a minimal install. E.g.: through the netinst images
* Allow root login (That will get fixed through Ansible)
* Choose a simple password (That will get fixed through Ansible)
* Choose any hostname (That will get fixed through Ansible)
* Choose any domain name (That will get fixed through Ansible)

* Pick a simple disk layout. For example a GPT disk with
  256MB boot
  10GB swap
  Remaining space btrfs

* No need for backported software (That will get fixed through Ansible)
* No need for a desktop environment (That will install one if needed)
* `apt-get update && apt-get install sudo`
* Make sure you can `ssh` into the host
* deploy dhparams

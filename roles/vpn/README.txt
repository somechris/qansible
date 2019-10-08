Role: vpn
=========



1. Description
2. Globals
3. Parameters



1. Description
--------------

Sets up VPNs.



2. Globals
----------

* `vpn_configs`: A list of VPNs to set up. Each VPN config is a
  dictionary with the following key/value pairs:
  * `client`: The name of the host that acts as client.
  * `server`: The name of the host that acts as server.
  * `port`: The UDP port to use to set up the VPN.
  * `ipv4_net`: The IPv4 net to use for the VPN. Typically a `/30`
    net.


3. Parameters
-------------

This role does not have parameters.

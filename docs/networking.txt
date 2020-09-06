todo: Write content


* `vpn`:
  * `heartbeat_rate`: (Default: `vpn_default_heartbeat_rate`) The period (in
    seconds) between sending heartbeats to the remote host.
  * `heartbeat_timeout`: (Default: 3 * `heartbeat_rate` + the lesser of 10 and
    `heartbeat_rate`/2) Treat the connection as broken and restart after that
    many seconds without receiving a heartbeat from the remote host.

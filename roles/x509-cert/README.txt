Role: x509-cert
===============



1. Description
2. Globals
3. Parameters



1. Description
--------------

Installs a x509 server certificate and key to the OS.

The server certificate, chain, and key for have to be available in the
x509_cert_name's subdirectory of this role's `files` directory as
`cert.pem`, `chain.pem`, and `key.pem` in PEM format.

The certificate gets installed into `{{ssl_cert_dir}}` in two
variants:
* `DOMAIN__cert.crt` The plain certificate
* `DOMAIN__chained.crt` The chained certificate

The certificate key gets installed into `{{ssl_private_dir}}` in two
variants:
* `DOMAIN__key.pem` The plain key
* `DOMAIN__w_dhparam.pem` The key with dhparams.



2. Globals
----------

No Globals that are specific only for this role.



3. Parameters
-------------

* `x509_cert_name`: The name of the certificate to set up.

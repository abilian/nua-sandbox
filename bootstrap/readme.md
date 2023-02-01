How to use?
===========

Remotely
--------

Assuming you have root access to the server vias SSH:

1) Install `pyinfra` (e.g. `pipx install pyinfra`).

2) Run `pyinfra --user root <name-of-your-server> nua-bootstrap.py` from this directory.

Note: currently this has to be run twice (the first time it fails). This is under invstigation.

On the server
-------------

1) Run `curl https://raw.githubusercontent.com/abilian/nua-sandbox/main/bootstrap/nua-bootstrap.sh | bash -` (as root).

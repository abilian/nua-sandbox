# Bootstrap scripts for NUA instances

## What is this?

Boostrap scripts to create a NUA environment on a server.

## How to use?

### Remotely

Assuming you have root access to the server via SSH from your laptop / development machine:

1) Install `pyinfra` (e.g. `pipx install pyinfra`) on your development environment.

2) Run `pyinfra --user root <name-of-your-server> nua-bootstrap.py` from this directory.

Note: currently this has to be run twice (the first time it fails). This is under invstigation.

### On the server

1) Run `curl https://raw.githubusercontent.com/abilian/nua-sandbox/main/bootstrap/nua-bootstrap.sh | bash -` (as root).

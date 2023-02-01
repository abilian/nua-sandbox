#!/bin/bash

set -ex

# This script is used to bootstrap the NUA environment.
# It is intended to be run on a fresh Ubuntu 22.04 LTS installation.

apt-get update
apt-get install -y pipx
pipx install pyinfra

git clone https://github.com/abilian/nua-sandbox.git
cd nua-sandbox/bootstrap
pyinfra @localhost nua-bootstrap.py

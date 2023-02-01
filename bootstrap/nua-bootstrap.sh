#!/bin/bash

set -ex

# This script is used to bootstrap the NUA environment.
# It is intended to be run on a fresh Ubuntu 22.04 LTS installation.

apt-get update
apt-get install -y pipx
pipx install pyinfra

rm -rf /tmp/nua-sandbox-git
git clone https://github.com/abilian/nua-sandbox.git /tmp/nua-sandbox-git
cd /tmp/nua-sandbox-git/bootstrap
pyinfra @local nua-bootstrap.py

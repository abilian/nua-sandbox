#!/usr/bin/sh

set -e

useradd nua -m -d /nua -U -s /bin/bash

cat > /etc/apt/apt.conf.d/00-nua << EOF
Acquire::http {No-Cache=True;};
APT::Install-Recommends "0";
APT::Install-Suggests "0";
Acquire::GzipIndexes "true";
Acquire::CompressionTypes::Order:: "gz";
Dir::Cache { srcpkgcache ""; pkgcache ""; }
EOF

echo "Installing Python packages"
apt-get -y update
apt-get -qq --no-install-recommends install \
        python3.10 python3.10-venv python-pip python-setuptools \
        unzip curl

# unzip and curl may be removed someday

python3 -m venv /nua/build/agent
chown -R nua:nua /nua/build

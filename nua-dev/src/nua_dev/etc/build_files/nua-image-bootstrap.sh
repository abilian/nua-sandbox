#/usr/bin/sh

useradd nua -m -d /nua -U -s /bin/bash

cat > /etc/apt/apt.conf.d/00-nua << EOF
Acquire::http {No-Cache=True;};
APT::Install-Recommends "0";
APT::Install-Suggests "0";
Acquire::GzipIndexes "true";
Acquire::CompressionTypes::Order:: "gz";
Dir::Cache { srcpkgcache ""; pkgcache ""; }
EOF

apt-get -y update && \
    apt-get -qq --no-install-recommends install \
      python3 python3-pip python3.10-venv curl python3-setuptools

python3 -m venv /nua/build/env
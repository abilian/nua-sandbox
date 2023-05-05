#!/bin/bash

set -e
set -o pipefail

# Build
CGO_ENABLED=0 go build -ldflags='-s -w'

# Install
mkdir -p /nua/app
cp galene /nua/app
cp LICENCE /nua/app
cp -a static /nua/app
mkdir /nua/app/groups
mkdir /nua/app/dat

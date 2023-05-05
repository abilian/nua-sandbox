#!/bin/bash

set -eux -o pipefail

# See: https://github.com/calcom/docker/blob/main/Dockerfile

yarn install
yarn global add turbo
yarn config set network-timeout 1000000000 -g
turbo prune --scope=@calcom/web --docker
yarn install
yarn turbo run build --filter=@calcom/web

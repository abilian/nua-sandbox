#
# This dockerfile is used by all Nua packages
# (except those that supply their own Dockerfile).
#
FROM ubuntu:jammy-20230308

ENV DEBIAN_FRONTEND noninteractive

WORKDIR /nua/build

# Initial bootstrap (install Python, etc.)
COPY nua-bootstrap-image.sh nua-install-build-agent.py ./bin/
RUN /bin/sh bin/nua-bootstrap-image.sh

# Install nua-build-agent
COPY ./dist/ ./dist/
RUN /nua/build-env/bin/python3 bin/nua-install-build-agent.py

# Install system dependencies
COPY ./_nua-build-config.json ./
RUN /nua/build-env/bin/nua-build-agent install-deps

# Build app
COPY ./_nua-config.json ./
ADD ./src/* /nua/src/
RUN /nua/build-env/bin/nua-build-agent build-app

# Cleanup
RUN /nua/build-env/bin/nua-build-agent cleanup
RUN rm -rf /nua/build-env

#
# This dockerfile is used by all Nua packages
# (except those that supply their own Dockerfile).
#
FROM ubuntu:jammy-20230308

ENV DEBIAN_FRONTEND noninteractive

WORKDIR /nua/build

# Initial bootstrap (install Python, etc.)
COPY nua-image-bootstrap.sh ./bin/
RUN /bin/sh bin/nua-image-bootstrap.sh

# Install nua-agent
COPY ./dist/ ./dist/
RUN /nua/build/env/bin/pip install \
    /nua/build/dist/*.whl setuptools typer jinja2 snoop

# Install system dependencies
COPY ./_nua-build-config.json ./
RUN ./env/bin/nua-agent install-deps

# Build app
COPY ./_nua-config.json ./
RUN ./env/bin/nua-agent build-app

# Cleanup
RUN ./env/bin/nua-agent cleanup
RUN rm -rf /nua/build-env

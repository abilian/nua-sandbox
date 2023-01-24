FROM ubuntu:jammy-20221130

ENV DEBIAN_FRONTEND noninteractive

RUN useradd nua -m -d /nua -U -s /bin/bash
COPY apt.conf.d/ /etc/apt/apt.conf.d/
RUN apt-get -y update && \
    apt-get -y --no-install-recommends install python3 python3-pip curl python3-setuptools

# RUN apt-get -y install python3-typer python3-jinja2 python3-setuptools python3-pip

# Install the Nua Agent and dependencies (manually)
COPY dist/ /nua/dist/

# Note:
# Typer used for CLI arg parsing
# Jinja2 not used (yet?)
# Shelmet used for running shell commands
RUN pip install /nua/dist/*.whl setuptools typer jinja2 snoop
RUN nua-agent version

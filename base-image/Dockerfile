FROM ubuntu:jammy-20221130

ENV DEBIAN_FRONTEND noninteractive

RUN useradd nua
RUN apt-get -y update && \
    apt-get -y install curl python3

RUN apt-get -y install python3-typer python3-jinja2 python3-setuptools python3-pip

# Install Nua agent
COPY dist/ /nua/dist/
RUN pip install /nua/dist/*.whl
RUN nua-agent version

#RUN curl -sL https://deb.nodesource.com/setup_18.x | bash - && \
#    apt-get -y install nodejs && \
#    npm install -g yarn
# RUN apt-get -y install nodejs
# RUN npm install -g yarn

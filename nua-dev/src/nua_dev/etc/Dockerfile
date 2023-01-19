#
# This dockerfile is used in all Nua packges (for now...)
# Additional info will be added lated using Jinja templating.
#
FROM nua-base

WORKDIR /nua/build
ADD _nua-config.json .

# fetch-source is run first so that builder detection can work
RUN nua-agent fetch-source
RUN nua-agent pre-build
RUN nua-agent build

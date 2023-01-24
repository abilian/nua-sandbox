#
# This dockerfile is used in all Nua packges (for now...)
# Additional info will be added lated using Jinja templating.
#
FROM nua-base

WORKDIR /nua/build
ADD _nua-config.json .

RUN nua-agent build-image

#
# This dockerfile is used in all Nua packges (for now...)
# Additional info will be added lated using Jinja templating.
#
FROM nua-base

WORKDIR /nua/build
COPY ./ ./

RUN nua-agent build-image

# Image specification

How a Nua image is organized.

A Nua image is just a Docker (OCI) image with a few conventions.

Everything related to Nua is under `/nua` in the image.

(This doc is a draft to be discussed.)

## At build time

`/nua/build` is the root directory of the build tree. It contains:

- `/nua/build/src`: the source code of the application
- `/nua/build/metadata`: the metadata of the application

The build itself is done in `/nua/build/src` (e.g. `cd /nua/build/src && ./configure && make` or its modern equivalent).

Implementation details:

- `/nua/build/dist`: temp directory where the agent wheels are put
- `/nua/build/agent`: the virtual environment directory of the build agent

At the end of the build, `/nua/build` should be removed.


## At runtime

- `/nua/app`: the runtime directory of the application (may be empty in the whole app is in a virtualenv, for instance)
- `/nua/metadata`: the Nua metadata directory
- `/nua/etc`: for application-sepcific configuration files
- `/nua/venv`: the virtual environment directory (for Python apps)
- `/nua/scripts`: the scripts that manage the lifecycle of the application
- `/nua/bin`: the binaries of the application (if needed, for instance `deno` can go there)

### TBD

The `/nua/metadata` directory contains:

- `/nua/metadata/nua-config.json`: the config of the application
- `/nua/metadata/sbom.json`: a SBOM (in a format to be determined)
- What else ?

The `/nua/scripts` directory may contain:

- `/nua/scripts/start`: the script that starts the application
- `/nua/scripts/stop`: the script that stops the application
- `/nua/scripts/restart`: the script that restarts the application
- `/nua/scripts/healthcheck`: the script that checks the health of the application
- `/nua/scripts/upgrade`: the script that upgrades the application
- `/nua/scripts/rollback`: the script that rolls back the application
- `/nua/scripts/backup`: the script that backs up the application
- `/nua/scripts/restore`: the script that restores the application

Or a single script that does all of the above (either a Python script with well-defined entry points, or a shell script with well-defined functions).

The scripts may use templates (e.g. Jinja2) to generate application-specific scripts or config files. Where do we put them ? (e.g. `/nua/scripts/templates` ?)

### Notes

`/nua/venv` contains the virtualenv of the application (if it's a Python app). What about other languages ?

The logs should be sent to the orchestrator (e.g 12-factor app), not kept locally.

Do we need to specify other directories (for instance for app-specific data) ?

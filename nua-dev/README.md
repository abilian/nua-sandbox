# About

CLI to directly interact with the build system.

Only used for developping / debugging Nua itself.

End-users will use the `nua` CLI.

## What it does

- Validate the `nua-config.toml` file using a JSONSchema.
- Does some basic variable expansion.
- Generate a `Dockerfile.nua`. (Actually, it's the same Dockerfile for alls projects, at least for now.)
- Calls the `docker build` command with the generated `Dockerfile.nua`.

## Usage

`nua-dev build`: build a Nua image. (You must be in a Nua project directory, with a `nua-config.toml` file at its root.)

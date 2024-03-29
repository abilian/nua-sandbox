# TODO

## Done

- [x] ZIP support
- [x] Implement and test all the build profiles (moslty done for now)
- [x] Make sure all the applications build (mostly done for now)
- [x] Extract metadata from GitHub projects
- [x] Support Ruby apps
- [x] Make all the demo build

## Short term

Source code:

- [ ] Git support.
- [ ] Version update (automated)
- [ ] Check and update checksums

Build / Run:

- [ ] Build as `nua`, not as `root`
- [ ] Support "multi-language" apps (ex: Ruby + Node)
- [ ] Support "old-school PHP" apps (i.e. w/o Composer)
- [ ] Support multiple Python / Node / PHP / Ruby / etc. versions
- [ ] Make sure (test) that the images built with nua-dev are compatible with nua-orchestrator

DX:

- [ ] Work on the log messages so that it's easier to understand what's going on.
  - [ ] Logging: divert build logs to 1 file per build.
  - [ ] Add hooks to deal with special cases at build time (e.g. `build.py`).

Optimisations:

- [ ] Look at ways to reduce image size
  - [ ] Split build image / run image
  - [ ] Remove dependency on `curl`.
  - [ ] Remove cruft after build
- [ ] Optimise for layer caching (when using Docker)

Refactor:

- [ ] Run builds in a dedicated directory (e.g. `_build/`) ?

Metadata / lifecycle:

- [ ] Procfile support.
- [ ] Import useful metadata from other systems (heroku, render, etc.).
- [ ] Formalize specification
  - [ ] Of the build profiles (config + support files).
  - [ ] Of the runtime images.

Buildpacks:

- [ ] Make it possible to use buildpacks
  - [ ] We need to choose the right one
- [ ] make `nua-dev` into a buildpack

## Longer term / advanced R&D

- [ ] Runtime support via `nua-agent` (not sure if this is needed)
- [ ] Alternatives build systems (hand-crafted Dockerfiles, Nix/Guix, https://buildpacks.io/, https://modus-continens.com/, https://nixpacks.com/, etc.)
- [ ] Alternative backends (e.g. SlapOS)
- [ ] Support for `docker-compose` (or similar)
- [ ] Reproducible builds.
- [ ] SBOM and software supply chain issues.
- [ ] Plugins: the system should be extensible. For the build subsystem, this should probably (at least in the current architecture) done by adding support for plugins at the `nua-build-agent` level. This means that the plugins to use should be specified (in a specific section) in the `nua-config.toml` file and be injected early in the build process (this seems a bit tricky so more thoughts are needed).

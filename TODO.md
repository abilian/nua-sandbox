# TODO

## Short term

- [x] ZIP support
- [ ] Support multiple Python / Node / PHP / Ruby / etc. versions
- [ ] Implement and test all the build profiles.
- [ ] Make sure all the applications build (and add more).
- [ ] Work on the log messages so that it's easier to understand what's going on.
  - [ ] Logging: divert build logs to 1 file per build.
  - [ ] Add hooks to deal with special cases at build time (e.g. `build.py`).
- [ ] Look at ways to reduce image size (e.g. split build image / run image).
    - [ ] Remove dependency on `curl`.
- [ ] Run builds in a dedicated directory (e.g. `_build/`) ?
- [ ] Git support.
- [ ] Procfile support.
- [ ] Import useful metadata from other systems (heroku, render, etc.).
- [ ] Formalize specification
  - [ ] Of the build profiles (config + support files).
  - [ ] Of the runtime images.

## Longer term

- [ ] Runtime support via `nua-agent`
  - [ ] Should we split `nua-agent` into a build-time and a run-time part?
- [ ] Alternatives build systems (hand-crafted Dockerfiles, Nix/Guix, https://buildpacks.io/, https://modus-continens.com/, https://nixpacks.com/, etc.)
- [ ] Alternative backends (e.g. SlapOS)
- [ ] Support for `docker-compose` (or similar)
- [ ] Optimise for layer caching (when using Docker)
- [ ] Reproducible builds.
- [ ] SBOM and software supply chain.
- [ ] Plugins: the system should be extensible. For the build subsystem, this should probably (at least in the current architecture) done by adding support for plugins at the `nua-agent` level. This means that the plugins to use should be specified (in a specific section) in the `nua-config.toml` file and be injected early in the build process (this seems a bit tricky so more thoughts are needed).

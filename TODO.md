# TODO

## Short term
 
- [ ] Implement and test all the build profiles.
- [ ] Make sure all the applications build.
- [ ] Remove dependency on `curl`.
- [ ] Look at ways to reduce image size (e.g. split build image / run image).
- [ ] Add hooks to deal with special cases at build time (e.g. `build.py`).
- [ ] Run builds in a dedicated directory (e.g. `_build/`).
- [ ] Procfile support.
- [ ] Import useful metadata from other systems (heroku, render, etc.).
- [ ] Git support.

 
## Longer term

- [ ] Runtime support via `nua-agent` ?
- [ ] Alternatives build systems (hand-crafted Dockerfiles, Nix/Guix, etc.)
- [ ] Alternative backends (e.g. SlapOS)
- [ ] Support for `docker-compose` (or similar)

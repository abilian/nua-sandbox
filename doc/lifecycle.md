## Build Lifecycle

Each of these lifecycle stages is a target for the `nua-build-agent` script.

The general idea is to split the build lifecycle into as many parts as reasonably possible, in order to leverage Docker's layer caching mechanism to speed up builds.

At the end of the build, another extra step could be added (outside the container) to reduce the image size.

### Current

- `install-deps`: install system dependencies (e.g. `apt-get install`)
- `build-app`: build the app
- `cleanup`: cleanup after build

### Target

After refactoring, the build lifecycle should become:

- `install-sys-deps`: install system dependencies (e.g. `apt-get install`)
- `fetch-source`: fetch the app source code
- `prep`: prepare the build tree (not sure if this is needed)
- `fetch-deps`: fetch dependencies (e.g. `pip download`)
- `build-deps`: build dependencies
- `build`: build the application itself
- `install`: install the app to `/nua/app`
- `cleanup`: cleanup after build
- `check`: check that everything is ok (applying some heuristics)
- `smoke-test`: run a smoke test

Notes:

- `cleanup` is probably not needef (or maybe exceptionnally) as `/nua/build` is removed at the end of the build.

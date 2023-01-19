# About

Alternative implementation of `Nua` to explore the design space.

DON'T USE. Useful concepts will be merged into the main `Nua` project.

## Key ideas

- Purely declarative build system. (Actually: as declarative as possible.)
- Build profiles for ~10 major web technologies.

## Specific points

- What's called `nua-rutime` in Nua is called `nua-agent` here.
- Python sup-packages are called `nua_something` instead of `nua.something`.
- Main entry point for the project in the `tasks.py` file.
  - Run `poetry shell && poetry install` first
  - Then `invoke install`
  - Then `invoke build-all`.
- Every time you edit something in `nua-agent`, you need to rebuild the base image
  - (so either run `invoke build-all` or `invoke build-base` before building specific apps).
- Many apps are not building (yet). Sometimes it's not our fault.
- Debian (actually, Ubuntu) is used as the base image. This causes some issues (TBD).

## What's missing

No work on runtime/orchestrator (yet?).

## TODO

see [TODO.md](./TODO.md)

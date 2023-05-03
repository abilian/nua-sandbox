# About

This is code that runs in the containers.

- At buildtime (currently)
- At runtime (in the future?)

It is injected in the base image (see [../base-image/](../base-image/)).


## Notes for developers

For debugging / troubleshooting, you can use [Snoop](https://pypi.org/project/snoop).

Snoop is "installed", so you can use `@snoop` et `pp` everywhere without importing anything.

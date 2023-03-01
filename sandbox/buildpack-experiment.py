#!/usr/bin/env python3
import re
import tempfile
from pathlib import Path

from click import secho

from nua_agent.builder import Builder
from nua_agent.sh import shell
from nua_dev.backports import chdir
from nua_dev.config import Config

BUILDER_NAMES = [
    "cnbs/sample-builder:bionic",
    "heroku/buildpacks:20",
    "cloudfoundry/cnb:bionic",
    "gcr.io/buildpacks/builder:v1",
    "paketobuildpacks/builder:full",
]


successful_builds = []
failed_builds = []


def main():
    this_dir = Path(__file__).parent
    for app_dir in (this_dir / ".." / "apps").iterdir():
        try:
            build_app(app_dir)
        except Exception as e:  # noqa
            print(f"Error while building {app_dir}: {e}")

        print("\n" + 78 * "=" + "\n")

    print("Successful builds:")
    for build in successful_builds:
        print(f" - {build[0]} with {build[1]}")

    print()

    print("Failed builds:")
    for build in failed_builds:
        print(f" - {build[0]} with {build[1]}")


def build_app(app_dir: Path):
    config = Config().parse_config(app_dir)
    app_name = config["metadata"]["id"]

    builder = Builder(config)

    with tempfile.TemporaryDirectory() as tmp_build_dir:
        with chdir(tmp_build_dir):
            builder.fetch_app_source()
            build_with_all_builders(app_name)


def build_with_all_builders(app_name: str):
    for builder_name in BUILDER_NAMES:
        build_with_builder(app_name, builder_name)


def build_with_builder(app_name: str, builder_name: str):
    builder_tag = re.sub('\W+', '-', builder_name)
    tag = rf"{app_name}-buildpack-{builder_tag}"
    try:
        shell(f"pack build {tag} --path . --builder {builder_name}")
        successful_builds.append((app_name, builder_name))
    except:
        secho(f"Failed to build {app_name} with {builder_name}", fg="red")
        failed_builds.append((app_name, builder_name))


if __name__ == "__main__":
    main()

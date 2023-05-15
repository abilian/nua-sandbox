from io import BytesIO

from nua_dev.config import AttrGetter, Config

CONFIG = b"""
[metadata]
id = "aip-mini"
title = "AIP Mini"
author = "Abilian"
description = ""
version = "0.1"
release = 1
license = "MIT"

[build]
project = "."
# builder = ""
packages = [
    "build-essential",
    "git",
    "python3-dev",
    # For magic
    "libmagic-dev",
]
"""


def test_get():
    config = Config.from_file(BytesIO(CONFIG))
    assert config.get(["metadata", "id"]) == "aip-mini"
    assert config.get("metadata.id") == "aip-mini"
    assert config.get(["metadata", "foobar"]) is None
    assert config.get(["barbek", "foobar"]) is None


def test_get_str():
    config = Config.from_file(BytesIO(CONFIG))
    assert config.get_str(["metadata", "id"]) == "aip-mini"
    assert config.get_str("metadata.id") == "aip-mini"
    assert config.get_str(["metadata", "foobar"]) == ""
    assert config.get_str(["barbek", "foobar"]) == ""


def test_attr_getter():
    d = {"foo": "bar"}
    ag = AttrGetter(d)
    assert ag.foo == "bar"

    dd = {"foo": {"bar": "baz"}}
    ag = AttrGetter(dd)
    assert ag.foo.bar == "baz"

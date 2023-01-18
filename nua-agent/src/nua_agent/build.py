from .builders import BUILDER_CLASSES
from .builders.base import Builder


def build():
    builder = find_builder()
    builder.build()


def find_builder() -> Builder:
    for builder_cls in BUILDER_CLASSES:
        builder = builder_cls()
        if builder.accept():
            print(f"Will build with builder: {builder_cls.__name__}")
            return builder

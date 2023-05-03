import sys
import traceback

from cleez.colors import red


class Fail(Exception):
    def __init__(self, msg: str, exception: Exception | None = None):
        print(red(msg))
        if exception:
            traceback.print_exception(exception)
            raise SystemExit(1)

        exc_info = sys.exc_info()
        if exc_info:
            traceback.print_exc()

        raise SystemExit(1)

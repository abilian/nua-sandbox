from cleez.colors import red


class Abort(SystemExit):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)
        self.msg = msg
        print(red(msg))
        raise SystemExit(1)

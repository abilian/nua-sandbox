import nua_dev.sh as sh


def test_builder():
    sh.shell("inv build-all")

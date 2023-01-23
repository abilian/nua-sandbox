import nua_dev.sh as sh


def test_all():
    sh.shell("inv build-base")
    sh.shell("inv build-apps")

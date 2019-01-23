import pytest

from pymba import Vimba, VimbaException


def test_version():
    version = Vimba().version.split('.')
    assert int(version[0]) >= 1
    assert int(version[1]) >= 7
    assert int(version[2]) >= 0


def test_startup_shutdown():
    with pytest.raises(VimbaException) as e:
        Vimba().system().feature_names()
    assert e.value.error_code == VimbaException.ERR_STARTUP_NOT_CALLED

    # manual
    Vimba().startup()
    Vimba().system().feature_names()
    Vimba().shutdown()

    # context manager
    with Vimba() as vmb:
        vmb.system().feature_names()


@pytest.fixture
def vmb() -> Vimba:
    with Vimba() as v:
        yield v


# works best with camera(s) attached
def test_interface_camera_ids(vmb: Vimba):
    # for ethernet camera discovery
    if vmb.system().GeVTLIsPresent:
        vmb.system().run_feature_command("GeVDiscoveryAllOnce")

    # test id funcs return a list of strings (not bytes)
    for func in (vmb.interface_ids, vmb.camera_ids):
        ids = func()
        assert isinstance(ids, list)
        for x in ids:
            assert isinstance(x, str)

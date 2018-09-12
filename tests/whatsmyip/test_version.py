import pkg_resources

from whatsmyip.__version__ import __version__ as app_version


def test_version():
    v = pkg_resources.parse_version(app_version)
    assert isinstance(v, pkg_resources.extern.packaging.version.Version)

from distutils.version import StrictVersion
from whatsmyip.__version__ import __version__ as app_version


def test_version():
    StrictVersion(app_version)

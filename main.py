from libprobe.probe import Probe
from lib.check.sites import CheckSites
from lib.check.system import CheckSystem
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = (
        CheckSites,
        CheckSystem,
    )

    probe = Probe('unificontroller', version, checks)
    probe.start()

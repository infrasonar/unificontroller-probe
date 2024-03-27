from libprobe.probe import Probe
from lib.check.sites import check_sites
from lib.check.system import check_system
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = {
        'sites': check_sites,
        'system': check_system,
    }

    probe = Probe('unificontroller', version, checks)
    probe.start()

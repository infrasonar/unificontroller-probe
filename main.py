from libprobe.probe import Probe
from lib.check.alarms import check_alarms
from lib.check.device import check_device
from lib.check.health import check_health
from lib.check.system import check_system
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = {
        'alarms': check_alarms,
        'device': check_device,
        'health': check_health,
        'system': check_system,
    }

    probe = Probe('unificontroller', version, checks)
    probe.start()

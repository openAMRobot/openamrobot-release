"""One validated inventory shared by preflight and the installed-type verifier."""
import re

BASE_NAMES = ('ActiveConstraint', 'DockingStatus', 'LocalizationStatus',
              'MotionSourceCoverage', 'NavigationStatus', 'NavStackStatus',
              'NavTaskStatus', 'ParkingStatus', 'ProtectionStatus', 'RecoveryStatus',
              'SensorStatus')


def inventory_names(contract, additional):
    if type(contract) is not int or contract not in (1, 2):
        raise ValueError('unsupported contract_version; expected 1 or 2')
    built_in = BASE_NAMES + (('SiteConfigStatus',) if contract == 2 else ())
    if (not isinstance(additional, list)
            or any(not isinstance(name, str) or not re.fullmatch(r'[A-Z][A-Za-z0-9]*', name)
                   for name in additional)
            or len(additional) != len(set(additional))):
        raise ValueError('additional_messages must be a list of unique message names')
    repeated = set(built_in).intersection(additional)
    if repeated:
        raise ValueError('additional_messages repeats built-in messages: ' + ', '.join(sorted(repeated)))
    return built_in + tuple(additional)

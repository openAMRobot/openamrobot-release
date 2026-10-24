"""Check a fixed inventory, native type support, and serialization after install."""
import os
import subprocess
from rclpy.serialization import deserialize_message, serialize_message
from rosidl_runtime_py.utilities import get_message
from openamr_nav_msgs.msg import NavigationStatus

NAMES = ('ActiveConstraint', 'DockingStatus', 'LocalizationStatus',
         'MotionSourceCoverage', 'NavigationStatus', 'NavStackStatus',
         'NavTaskStatus', 'ParkingStatus', 'ProtectionStatus', 'RecoveryStatus',
         'SensorStatus')
assert NavigationStatus.CONTRACT_VERSION == int(os.environ['EXPECTED_CONTRACT'])
with open('/evidence/interfaces.txt', 'w') as output:
    for name in NAMES:
        interface = f'openamr_nav_msgs/msg/{name}'
        output.write(interface + '\n')
        output.write(subprocess.check_output(['ros2', 'interface', 'show', interface], text=True))
        cls = get_message(interface)
        message = cls()
        assert deserialize_message(serialize_message(message), cls) == message
        print(f'PASS: {interface} native serialization round trip', flush=True)

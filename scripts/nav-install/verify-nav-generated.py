"""Check a fixed inventory, native type support, and serialization after install."""
import os
import json
import subprocess
from rclpy.serialization import deserialize_message, serialize_message
from rosidl_runtime_py.utilities import get_message
from openamr_nav_msgs.msg import NavigationStatus
from message_inventory import inventory_names

NAMES = inventory_names(int(os.environ['EXPECTED_CONTRACT']),
                        [name for name in os.environ.get('EXTRA_MESSAGES', '').split(',') if name])
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
with open('/evidence/verified-messages.json', 'w') as output:
    json.dump(list(NAMES), output)

#!/usr/bin/env bash
set -eo pipefail
exec > >(tee /evidence/steps.log) 2>&1
trap 'code=$?; echo "FAIL: consumer line $LINENO (exit $code)"; exit "$code"' ERR
export EXPECTED_CONTRACT=$1
source /opt/ros/jazzy/setup.bash
apt-get update
apt-get install -y --no-install-recommends build-essential python3-colcon-common-extensions ros-jazzy-rclcpp ros-jazzy-rclpy ros-jazzy-std-msgs ros-jazzy-rosidl-default-runtime
test ! -e /producer
test ! -e /producer-unavailable
tar -C /opt -xzf /artifact/navigation-install.tar.gz
mkdir -p /consumer/src
cp -a /checks/nav_consumer /consumer/src/nav_consumer
cd /consumer
# Negative control: ROS alone cannot configure this consumer.
if colcon build --event-handlers console_direct+ > /evidence/absent-install.log 2>&1; then
  echo 'FAIL: consumer unexpectedly built without the installed package'
  exit 1
fi
python3 - <<'PY'
from pathlib import Path
log = Path('/evidence/absent-install.log').read_text()
if 'openamr_nav_msgs' not in log or 'Could not find' not in log:
    raise SystemExit('Negative control failed for an unexpected reason')
print('PASS: absent-install negative control', flush=True)
PY
# Clear only the throwaway consumer outputs, all under this container workspace.
python3 - <<'PY'
import shutil
from pathlib import Path
for name in ('build', 'install', 'log'):
    path = Path('/consumer') / name
    if path.exists(): shutil.rmtree(path)
PY
source /opt/nav-install/local_setup.bash
test "$(ros2 pkg prefix openamr_nav_msgs)" = /opt/nav-install/openamr_nav_msgs
printf 'AMENT_PREFIX_PATH=%s\nCMAKE_PREFIX_PATH=%s\nPYTHONPATH=%s\n' "${AMENT_PREFIX_PATH:-}" "${CMAKE_PREFIX_PATH:-}" "${PYTHONPATH:-}"
python3 /checks/verify-nav-generated.py
cd /opt/nav-install/openamr_nav_msgs
find include share/openamr_nav_msgs/msg -type f \( -name '*.h' -o -name '*.hpp' -o -name '*.idl' \) -print0 | sort -z | xargs -0 sha256sum > /evidence/generated.sha256
test -s /evidence/generated.sha256
dpkg-query -W -f='${Package}=${Version}\n' | sort > /evidence/dependencies.txt
cd /consumer
colcon build --event-handlers console_direct+
cp -a log /evidence/consumer-log
source install/local_setup.bash
ros2 run nav_install_consumer smoke
echo 'PASS: installed generated messages and downstream consumer in a source-free container'

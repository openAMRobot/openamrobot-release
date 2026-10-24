#!/usr/bin/env bash
set -eo pipefail
exec > >(tee /evidence/steps.log) 2>&1
trap 'code=$?; echo "FAIL: producer line $LINENO (exit $code)"; exit "$code"' ERR
repository=$1
revision=$2
package_version=$3
source /opt/ros/jazzy/setup.bash
apt-get update
apt-get install -y --no-install-recommends git build-essential python3-colcon-common-extensions python3-rosdep
if [ ! -f /etc/ros/rosdep/sources.list.d/20-default.list ]; then rosdep init; fi
rosdep update --rosdistro jazzy
mkdir -p /producer/src
git clone "$repository" /producer/src/interfaces
git -C /producer/src/interfaces checkout --detach "$revision"
test "$(git -C /producer/src/interfaces rev-parse HEAD)" = "$revision"
git -C /producer/src/interfaces archive --format=zip --prefix="openamrobot-interfaces-$revision/" --output=/evidence/interfaces-source.zip "$revision"
export EXPECTED_VERSION=$package_version
python3 - <<'PY'
import os
import xml.etree.ElementTree as ET
version = ET.parse('/producer/src/interfaces/ros2/openamr_nav_msgs/package.xml').findtext('version')
if version != os.environ['EXPECTED_VERSION']:
    raise SystemExit(f'Package version mismatch: {version}')
print(f'PIN VERIFIED: openamr_nav_msgs {version}', flush=True)
PY
rosdep install --from-paths /producer/src/interfaces/ros2/openamr_nav_msgs --ignore-src --rosdistro jazzy -y
cd /producer
colcon build --base-paths src/interfaces/ros2/openamr_nav_msgs --install-base /opt/nav-install --event-handlers console_direct+
cp -a log /evidence/producer-log
dpkg-query -W -f='${Package}=${Version}\n' | sort > /evidence/dependencies.txt
# Ordinary install, never --symlink-install. Consumer runs in another container.
tar -C /opt -czf /evidence/navigation-install.tar.gz nav-install
sha256sum /evidence/navigation-install.tar.gz /evidence/interfaces-source.zip
echo 'PASS: pinned producer install packaged'

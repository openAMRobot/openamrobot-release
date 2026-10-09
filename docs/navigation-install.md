# Pinned navigation installation

Release issue [#5](https://github.com/openAMRobot/openamrobot-release/issues/5)
is validated against the release-owned [installation manifest](../navigation-install-manifest.json),
not a moving interfaces branch. The selected source commit is
`fa7c438e33bd807c174fa0747119d7d627faa3bf`; `openamr_nav_msgs` package version
is **0.0.0** and `NavigationStatus.CONTRACT_VERSION` is **1**. These identifiers
are distinct. This is a source-install candidate, not a published binary package.

## Reproduce the release gate

Install Python 3.11+ and Docker with its Linux engine running. The host needs
no ROS installation or developer workspace. From this release repository:

```sh
python3 scripts/validate_navigation_install.py --manifest navigation-install-manifest.json --evidence evidence/navigation-install-20261006-final
```

On Windows use `python` if that is the installed command. Choose a **new**
evidence directory for every attempt; the runner refuses to overwrite one.
The target is Ubuntu 24.04 / ROS 2 Jazzy / linux amd64, with the base image
pinned by digest in the manifest. Two independent producer/consumer pairs run:

1. The producer checks out the exact commit, verifies the package version,
   resolves dependencies, builds an ordinary install (no symlink install),
   and creates a source ZIP and installed-package tarball.
2. A fresh consumer container receives the install tarball and test fixtures
   only. The producer source/build tree is absent. Before installing the
   artifact, CMake configuration must fail because `openamr_nav_msgs` is missing.
3. After extracting the artifact, only ROS Jazzy and the navigation install
   are sourced. The package prefix must be `/opt/nav-install/openamr_nav_msgs`.
   All 11 generated messages are located, imported, and serialized/deserialized
   with native Python type support; the contract constant must equal `1`.
4. The minimal C++ consumer builds against the installed CMake exports and
   headers, links native type support, and runs serialization round trips for
   navigation, docking, and parking messages, including aggregate fields.
5. The two runs must agree on generated header/IDL hashes, expanded definitions,
   and resolved producer and consumer dependency inventories.

The runner snapshots its scripts before starting. No developer overlay,
host ROS paths, user Python packages, or source checkout is mounted into the
consumer. Generated file reproducibility is checked; byte-identical binaries
and a frozen apt/rosdep dependency snapshot are not claimed. Resolved package
versions are recorded because apt and rosdep indexes remain live.

## Consume the validated install

The validation tarball is a test artifact for the recorded Linux/Jazzy environment.
It is not an apt package or a published product release. In a matching environment
with the dependencies recorded in `consumer/dependencies.txt` installed:

```sh
tar -C /opt -xzf navigation-install.tar.gz
source /opt/ros/jazzy/setup.bash
source /opt/nav-install/local_setup.bash
ros2 pkg prefix openamr_nav_msgs
ros2 interface show openamr_nav_msgs/msg/NavigationStatus
mkdir -p consumer_ws/src
cp -r scripts/nav-install/nav_consumer consumer_ws/src/
cd consumer_ws
colcon build --event-handlers console_direct+
source install/local_setup.bash
ros2 run nav_install_consumer smoke
```

Extracting into `/opt` may require administrative rights. Package dependencies
and the exact setup/build commands are in `scripts/nav-install/consumer.sh`.
The consumer fixture uses `find_package(openamr_nav_msgs 0.0.0 EXACT REQUIRED)`;
its package manifest declares the dependency. Runtime contract version is
checked separately. Owning-repository field semantics remain canonical in the
[pinned navigation contract](https://github.com/openAMRobot/openamrobot-interfaces/blob/fa7c438e33bd807c174fa0747119d7d627faa3bf/ros2/openamr_nav_msgs/CONTRACT.md).

## Release-manifest integration

[release-config.nav-install.json](../release-config.nav-install.json) is a
**candidate** configuration for `2.0.0-rc.1`, not publication evidence. It replaces
the floating interfaces archive with the exact commit ZIP and references the
installation manifest. Other components and legacy product metadata still
need their own release preparation; this task does not validate the whole product.
The historical `release-config.json` is unchanged.

Copy the validated source ZIP, retaining its bytes:

```sh
mkdir -p input
cp evidence/navigation-install-20261006-final/first/producer/interfaces-source.zip input/openamrobot-interfaces-fa7c438e33bd807c174fa0747119d7d627faa3bf.zip
# Prepare the other component archives and candidate product metadata separately.
python3 scripts/build_release.py --config release-config.nav-install.json --input-dir input --output-dir dist --metadata-dir release-metadata
```

The builder rejects missing/failing evidence, mismatched manifest/evidence pins
or versions, unvalidated archive bytes, or archive/package/contract mismatches.
Generated `MANIFEST.json` carries the full source SHA, package version, contract
version, evidence result/digest, workflow URL when hosted, and install-artifact
digests. Do not overwrite or republish an existing release with this configuration.

## Evidence and review

See [the local evidence record](navigation-install-evidence.md). `commands.json`
records the exact Docker arguments. Each stage retains full command output,
dependency versions and colcon logs; consumer logs include all message checks
and the negative control. `checksums.sha256` covers the evidence files.
Install tarballs, source ZIPs and detailed colcon logs remain in the local/Actions
artifact; compact logs and results are retained in this repository.
The [CI workflow](../.github/workflows/navigation-install.yml) uploads evidence
even on failure. A skipped job or partial artifact is not a pass. Local evidence
does not constitute a hosted CI result. Reviewer acceptance and publication
remain separate from a successful source install.

## Troubleshooting

- Docker engine pipe missing or engine HTTP 500: start Docker Desktop's Linux
  engine and check `docker info`. No checks ran if the engine was unavailable.
- Image, apt, Git or rosdep failure: retain the failed log and repair access to
  the dependency source; do not skip dependency installation.
- Missing package: source Jazzy, then the intended install's `local_setup.bash`;
  verify the package prefix. Do not source a developer workspace to make it pass.
- Python/type-support failure: check the recorded Jazzy system Python and ROS
  runtime dependencies. Do not copy generated files from a source workspace.
- CMake/version mismatch: verify the manifest SHA, package `0.0.0`, and contract
  `1`. A package version does not replace the contract-version check.
- Reproducibility mismatch: compare both dependency inventories and generated
  hashes. Record a failure and rerun only after addressing the cause.
- Build-release pin rejection: use the source ZIP emitted by the validated run;
  redownloading or modifying a ZIP can change its digest despite the same commit.

## Provenance

Prepared with OpenAI Codex assistance at the release owner's request. The
consumer and generated-message check reuse the earlier local interfaces install
validation work; the producer/consumer separation, release builder integration,
workflow, and documentation were prepared for issue #5. No external source code
was copied. Repository code/documentation licensing applies.

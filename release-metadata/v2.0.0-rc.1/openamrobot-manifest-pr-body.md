## Work package

OA-39 follow-up for v2.0.0-rc.1: `releases/v2.0.0-rc.1.repos` moves from the 2026-10-19 candidate to the reviewed main of each repository read on 2026-11-20, the pins of openAMRobot/openamrobot-release `manifests/v2.0.0-rc.1.repos` (PR openAMRobot/openamrobot-release#18). The release builder's `pinned-release` check compares the two files and stays red until this merges. openamrobot-embodied-ai is added to both manifests; the two counting tests follow (13 -> 14, 11 -> 12). Source pins only, not release acceptance.

## Integration Gate

- Applied from `release-metadata/v2.0.0-rc.1/openamrobot-manifest-rc1-pins.patch` of openamrobot-release at 18bb3c8 (patch sha256 5ff714130a8b5d27540b3413273d29bd1462d1a4577ae125fb45e9af57c57ab9).
- Overlapping: #22 (release/rc1-pins-2026-11-10, 10 Nov pins and a cross-pin checker) changes the same file with older pins. Its pins are superseded by this PR; its checker is not taken here because it fails rc.1 while upperbody-sw main pins platform-sw 8e7a454 (openamr-upperbody-sw #74 carries the repin). Do not merge both pin sets.
- Reused: the existing validators (`tools/check_manifest.py`, `tools/check_release_manifest.py`) unchanged.

## Dependencies

- `openamrobot.repos`: adds openAMRobot/openamrobot-embodied-ai (branch main, MIT, https://github.com/openAMRobot/openamrobot-embodied-ai).
- `releases/v2.0.0-rc.1.repos`: every entry moves to the 2026-11-20 main SHA of its repository (licences unchanged per the licence map: MIT software and firmware, CERN-OHL-P-2.0 hardware, CC-BY-4.0 documentation); adds openamrobot-embodied-ai at 56bbd36ea313f3765df51524df07ccc6b2623f47 (MIT). Third-party entries unchanged: Slamtec/sllidar_ros2 34300099 (BSD), micro-ROS/micro-ROS-Agent 7c932329 (Apache-2.0, jazzy branch).

## Tests

Run on 2026-11-20 on a scratch clone of main 5b782ac with the patch applied:

```
python -m pip install yamllint==1.38.0 vcstool==0.3.0 PyYAML==6.0.2 setuptools==79.0.1
python -m unittest discover -s tests            # Ran 42 tests, OK
python tools/check_manifest.py openamrobot.repos   # 14 repositories
python tools/check_manifest.py --offline releases/v2.0.0-rc.1.repos
python tools/check_release_manifest.py releases/v2.0.0-rc.1.repos --development openamrobot.repos
# PASS development coverage and sources; PASS immutable refs: 14 repositories
```

Parity with the release builder (openamrobot-release at 18bb3c8): `python scripts/check_manifest_sync.py manifests/v2.0.0-rc.1.repos <this file>` prints "Matched 14 repositories (governance/.github excepted)". Against main 5b782ac it reports drift in 11 entries and the missing embodied-ai entry, which is the current red check on openamrobot-release#18.

## Evidence

- Base SHA: 5b782ac25f471d2006cae07bc06da4a88e7dca8e (main)
- Head SHA: PUSHED_HEAD_SHA (patch commit 3a50890 as prepared; `git am` gives it a new SHA with the same tree)
- Commands (the CI of this PR, manifest validation and Jazzy driver sources, is the record for the import of every SHA):

```
git am openamrobot-manifest-rc1-pins.patch
python -m unittest discover -s tests
python tools/check_release_manifest.py releases/v2.0.0-rc.1.repos --development openamrobot.repos
```

## Not verified

- The vcs import of every pinned SHA into a fresh workspace and the Jazzy driver build were not run locally; this PR's CI runs them.
- Pins are source pins only: no build of the ROS 2 workspace, no simulation, no physical, electrical or safety acceptance.

## AI disclosure

Claude Code (Claude Opus 5.5) prepared the patch, ran the commands above and wrote this description; the owner applied and pushed it.

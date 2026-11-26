# OpenAMRobot v2.0.0-rc.1 release notes

Status: release candidate, prepared 2026-11-26. Not tagged and not published until the owner gives the release decision.
This repository holds the release archive and is the ground truth; version tags in component repositories are navigation aids only.

**rc.1 is the Digital Twin release candidate: software and simulation only. No 2.0 hardware has been powered. Nothing in this release is physical, electrical or safety acceptance.**

| Version | Date | Meaning |
|---|---|---|
| v2.0.0-rc.1 | 2026-11-26 (planned 2026-11-20, missed) <!-- decision-allow: RELEASE-MILESTONES register keeps 20 Nov; owner chose RUNBOOK option B on 22 Nov 2026 --> | Pre-release: Digital Twin on Gazebo with simulation evidence |
| (bench window) | to 2026-12-18 | Physical integration, testing and acceptance |
| v2.0.0 | 2026-12-18 | Final release, only after the bench gates are recorded |

## Supported in rc.1

One profile is supported and tested: ROS 2 Jazzy on Ubuntu 24.04, Gazebo Harmonic, CycloneDDS.

- Combined robot model: mobile base, lift and two OpenArm arms.
- Navigation with Nav2; arm planning with MoveIt 2; lift and arm control through ros2_control.
- Software in the loop on virtual CAN for the base, the lift and the arm drivers (emulated devices).
- RViz configuration `build1.rviz` for the full profile.
- Baseline 1 whole-robot mission in simulation: drive to the station, authorize and raise the lift, reach, grasp, and retreat from the station (turn and 0.30 m forward). 8 phases. It is supported with the failures listed under Qualification evidence.
- A reproducible source archive and a clean install procedure for the profile above.

Install the supported profile from `openamrobot-manifest`: `releases/v2.0.0-rc.1-digital-twin.repos` with `tools/bootstrap_digital_twin.sh`. It imports six repositories at the commits below, installs the pinned Gazebo packages, builds, and prints the launch commands.

## Get started

1. Read the documentation section "OpenAMRobot 2.0 rc.1 Digital Twin" on https://docs.openamrobot.ai/ (system requirements, installation, quick start, RViz guide, demonstrations, troubleshooting). The section is in review in `openamrobot-docs` at the time of writing.
2. On Ubuntu 24.04 (x86_64): clone `openamrobot-manifest`, run `bash tools/bootstrap_digital_twin.sh ~/oamr_dt_ws`, then start the twin with `ros2 launch openamrobot_build1_scene build1.launch.py profile:=fast rviz:=true`.
3. In a second terminal run the first demonstration: `ros2 run openamrobot_build1_scene run_scenario.py scn01_drive`.

No physical hardware is needed. No GPU was used in the automated tests (headless software rendering); requirements for a desktop session have not been measured.

## Not supported in rc.1

Operator UI and manual driving from the UI; camera-driven manipulation (object poses come from simulator ground truth); cancel and resume of a navigation goal (see below); docking; Isaac Sim and MuJoCo; LeRobot and other AI pipelines; Jetson deployment; firmware on 2.0 hardware; any physical commissioning. These repositories are in the archive as source snapshots at reviewed commits, without a support claim.

The full workspace manifest `manifests/v2.0.0-rc.1.repos` does not build as one workspace: the interfaces and the UI repository both provide the package `openamr_ui_msgs`. Use the supported profile.

## Candidate commits

| Component | Commit | Note |
|---|---|---|
| openamr-platform-sw | ddd20ab3a85d98bb78c4c5f014952c4a0717ef92 | branch `release/2.0.0-rc.1`: `334e0ad` plus a documentation-only publication cleanup. The `main` branch is not the candidate |
| openamr-upperbody-sw | 1ab45a62957d238fc293eee08a8fd9158acebb01 | branch `release/2.0.0-rc.1` |
| openamrobot-interfaces | 50ed777be7990edbd3465f33fd97a158e7e3b88b | |
| openarm_description (upstream) | 14ff67b638ff1c738a1b9a6be8aaa5ce5ed2c831 | Apache-2.0 |
| openarm_ros2 (upstream) | 4e837e1d0dae692ff67b560b69d8d281d7a8d4ed | Apache-2.0 |
| openarm_can (upstream) | bfd4e52194aefe38389fa6e670be3738136facb9 | Apache-2.0 |

## Qualification evidence (simulation, hosted CI)

All runs are in `openamr-upperbody-sw` unless stated. Every attempt is listed, including those that did not pass. No limit, threshold or timeout was changed for this candidate.

Candidate: upper body `1ab45a62957d238fc293eee08a8fd9158acebb01` with platform `ddd20ab3a85d98bb78c4c5f014952c4a0717ef92`. The same gates were first run on the pull request head `729be2a`, which has the identical source tree (`1cf9ed4b`); both sets are listed.

| Gate | On the candidate `1ab45a6` | On the identical tree `729be2a` |
|---|---|---|
| Strict mission: 3 dispatches of 2 consecutive legs, 8 phases each | **2 of 3 verdicts PASS, 5 of 6 legs, 47 of 48 phases.** [45746655009](https://github.com/openAMRobot/openamr-upperbody-sw/actions/runs/45746655009) PASS, [45746645594](https://github.com/openAMRobot/openamr-upperbody-sw/actions/runs/45746645594) PASS, [45746635231](https://github.com/openAMRobot/openamr-upperbody-sw/actions/runs/45746635231) FAIL | 3 of 3 verdicts, 6 of 6 legs, 48 of 48 phases: [45735465924](https://github.com/openAMRobot/openamr-upperbody-sw/actions/runs/45735465924), [45735474913](https://github.com/openAMRobot/openamr-upperbody-sw/actions/runs/45735474913), [45735483682](https://github.com/openAMRobot/openamr-upperbody-sw/actions/runs/45735483682) |
| Scene matrix, 6 jobs | [45746664091](https://github.com/openAMRobot/openamr-upperbody-sw/actions/runs/45746664091): 374 passed, 0 failed, 0 blocked, 0 skipped, 1 expected failure (limitation 4). [45745728376](https://github.com/openAMRobot/openamr-upperbody-sw/actions/runs/45745728376): 5 of 6 jobs, `scn07_cancel_resume` FAIL (not supported) | [45735467645](https://github.com/openAMRobot/openamr-upperbody-sw/actions/runs/45735467645): 6 of 6 jobs |
| Arm diagnostics, 5 runs | 5 of 5: [45746668006](https://github.com/openAMRobot/openamr-upperbody-sw/actions/runs/45746668006) | 5 of 5: [45735492749](https://github.com/openAMRobot/openamr-upperbody-sw/actions/runs/45735492749) |
| OpenArm emulator on virtual CAN | passed: [45746675219](https://github.com/openAMRobot/openamr-upperbody-sw/actions/runs/45746675219) | passed: [45735467578](https://github.com/openAMRobot/openamr-upperbody-sw/actions/runs/45735467578) |
| Model tests, static and mock (a6) | passed: [45745728393](https://github.com/openAMRobot/openamr-upperbody-sw/actions/runs/45745728393) | passed on attempt 2: [45735467586](https://github.com/openAMRobot/openamr-upperbody-sw/actions/runs/45735467586) |
| Model tests, simulation (a7) | passed: [45746672017](https://github.com/openAMRobot/openamr-upperbody-sw/actions/runs/45746672017) | passed: [45742401706](https://github.com/openAMRobot/openamr-upperbody-sw/actions/runs/45742401706) |
| Clean install, 2 fresh environments | 2 of 2: [45747748555](https://github.com/openAMRobot/openamrobot-manifest/actions/runs/45747748555) (bootstrap twice, 17 packages built, advancing `/clock`, robot description, TF with `base_link`, drive scenario exit 0) | 2 of 2: [45738318716](https://github.com/openAMRobot/openamrobot-manifest/actions/runs/45738318716) |
| Platform tests on the platform candidate | description, drivers bring-up, navigation status and SIL tests passed: [45754126719](https://github.com/openAMRobot/openamr-platform-sw/actions/runs/45754126719), [45754129965](https://github.com/openAMRobot/openamr-platform-sw/actions/runs/45754129965), [45754133285](https://github.com/openAMRobot/openamr-platform-sw/actions/runs/45754133285), [45754136239](https://github.com/openAMRobot/openamr-platform-sw/actions/runs/45754136239) | |

The strict acceptance target for this candidate was 3 of 3 verdicts on the candidate commit. It was not met: one leg failed.

Attempts that did not pass:

- Strict dispatch [45746635231](https://github.com/openAMRobot/openamr-upperbody-sw/actions/runs/45746635231), leg 2: 7 of 8 phases. `nav_to_station` failed the odometry check, 0.10016 m against a limit of 0.100 m (limitation 1). The leg was not rerun to replace the result.
- Strict dispatch [45735465924](https://github.com/openAMRobot/openamr-upperbody-sw/actions/runs/45735465924), leg 2: tries 1 and 2 ended BLOCKED because the simulation froze right after start (limitation 2); try 3 passed 8 of 8. Across the 12 strict legs on this tree, 11 started on the first try and 2 of 14 start-up tries froze.
- Scene run [45745728376](https://github.com/openAMRobot/openamr-upperbody-sw/actions/runs/45745728376): `scn07_cancel_resume` failed, the resumed drive ended ABORTED. The same scenario passed in [45746664091](https://github.com/openAMRobot/openamr-upperbody-sw/actions/runs/45746664091) and [45735467645](https://github.com/openAMRobot/openamr-upperbody-sw/actions/runs/45735467645). Not supported.
- Model tests [45735467586](https://github.com/openAMRobot/openamr-upperbody-sw/actions/runs/45735467586), attempt 1: a download in the ROS setup step returned 404 before any test ran. Infrastructure.
- Pull request acceptance [45735467471](https://github.com/openAMRobot/openamr-upperbody-sw/actions/runs/45735467471): the single leg passed 8 of 8; the verdict job is red because one leg is never a strict result.
- Clean install [45736285492](https://github.com/openAMRobot/openamrobot-manifest/actions/runs/45736285492): build and launch worked, the check itself looked for the wrong TF frame and was corrected.

Not covered by any automated evidence: RViz on a real screen, a desktop or GPU session, the documented `rviz:=true` launch, and an installation followed by a person from the public instructions.

## Not supported: cancel and resume

Cancel stops the base under control (0.12 s and 0.012 m in the traced run, goal status CANCELED). The resumed goal can end ABORTED when the progress checker fires near the station (platform-sw #207, root cause #201). The scenario `scn07_cancel_resume` stays in the test matrix and its actual result is reported: on the candidate it passed in one run and failed in another. A pass does not make it supported. An older report that the cancelled goal itself returns ABORTED (platform-sw #189) is still open; it did not occur in the runs listed here.

## Known limitations of supported behaviour

1. **Odometry gate has little margin.** The mission compares odometry with simulator ground truth at the station (limit 0.100 m). Typical values are 0.048 to 0.070 m; one leg on the candidate measured 0.10016 m and failed (upperbody-sw #136). Odometry drifts in turns because of simulated wheel slip. Odometry numbers are not a reference.
2. **The simulation can freeze right after start.** In 2 of 14 start-ups of the mission the simulator published a few milliseconds of `/clock` and then stopped stepping. The cause is not known (upperbody-sw #135). CI detects it after 60 s, ends the processes of that try and starts again; every such try is listed in the verdict. If it happens to you: stop the launch with Ctrl+C and start it again.
3. **Station approach** can stop a few centimetres short and abort, about 1 time in 12 to 15 in earlier measurements. The mission fails closed and never reports a false success (platform-sw #207).
4. **Arm park in the `fast` profile.** `scn17_base_yaw_fast` is an expected failure: joint 4 of the arms on its lower limit does not move toward park with the DART physics engine while the controller reports success (upperbody-sw #126).
5. **Model tests use an older platform commit.** The static, mock and simulation model tests and the emulator tests build platform-sw `8e7a454` (the model pin in `upstream_pins.yaml`), not the candidate commit. The mission, scene and diagnostics gates build the candidate commit. In a diagnostic run with the model pin moved to the candidate commit, the emulator tests passed and two simulation model tests failed: the standalone upper body Gazebo launch spawns the model 2 mm from its resting height, and one bring-up shutdown check failed (upperbody-sw #145). The supported launch is the Build 1 scene; the standalone launches of the upper body repository are tested against the older platform commit only.
6. **Software in the loop.** Start-up standstill of the emulated drive in 2 of 65 earlier launches, and link-loss events from mixed wall and simulation clocks (upperbody-sw #137, #142). Simulation artefacts, not hardware evidence.
7. **RViz.** `build1.rviz` needs Nav2 and MoveIt both on (the defaults). The ground truth display is off by default because its frame is not in TF. RViz exits with an error at shutdown (upperbody-sw #143). Automated evidence is a configuration test only. A person has not yet checked RViz on a real screen for this candidate.
8. **Perception is not exercised.** The planning scene and object poses come from simulator ground truth.
9. **Middleware.** CycloneDDS only. Fast DDS loses samples under the mission load and one platform simulation job is red on it (platform-sw #197).
10. **Fidelity placeholders.** Wheel contact and friction, track width 0.400 m, drive dynamics and speed limits, camera poses and fields of view, battery constants; no power or brake model.
11. **Gate definitions are proposed values.** Known weaknesses for rc.2: the end-of-run liveness check passes when it is absent, the cancellation gate needs only one check, finger-to-item contact has no force cap, and the Stop check measures a base already at rest. The reverse-speed gate judges the forward drive at 0.010 m/s and reports the in-place turn separately (guarded by the 0.05 m turn-drift check).
12. **Clean install coverage.** The clean install check runs the `fast` profile headless with one drive scenario. It does not cover RViz on a screen, the `firmware_sil` profile or manipulation; those are covered by the gates on CI workspaces.
13. **Firmware.** No firmware image has been flashed on 2.0 hardware. The simulated mission uses host and emulator stand-ins; the safety state machine, drive enable, lift-permit producer and micro-ROS link are not implemented in the STM32H723 code.
14. **Timing-sensitive platform test.** `sil-tests` in platform-sw can fail on a slow runner (platform-sw #198).

## Safety statement

Simulation, software in the loop, emulators, fixtures and CI results are development evidence. They are not physical, electrical or safety acceptance, and functional telemetry, watchdogs and status displays are never safety evidence. There is no physical motion of 2.0 hardware until the bench gates are recorded, with wheels off the ground first and the hardwired stop chain tested on its own record. This is a research-grade pre-release, not certified for industrial, medical, safety-critical or unsupervised use.

## Source archive

Machine-readable files: `manifests/v2.0.0-rc.1.repos` (all pins) and the lock `release-config.rc1.json` (SHA-256 of the manifest and of every source archive, plus the exclusion list).

Two independent fetch builds from the lock are byte identical:

```
38faaaec8474364cf58f92e014fe623d0cbc34c4a43495012d20155fa888a9c2  OpenAMRobot-v2.0.0-rc.1-source.zip  (311720694 bytes, 3038 files verified)
```

This is a local rehearsal on the head of the release pull request. The published asset is the artifact of the hosted `Pinned rc.1 release` workflow, which must show the same procedure passing; its checksum is the one that counts. Only the source archive is reproducible; no compiled binaries are claimed. Inside the archive: `MANIFEST.json` (repositories, commits, source hashes, excluded files), `release.repos` and `checksums.sha256` covering every other file.

Which file to use: to run the Digital Twin, do not download the archive; use the supported profile in `openamrobot-manifest` as described above. The archive is the complete source record of the release.

Left out of the archive: 32 manufacturer files (25 datasheets and 7 other vendor files) under `hardware/openamr-platform-hw`, for which no redistribution right is documented. They are listed under `excluded` in `MANIFEST.json`. This is a packaging decision only; it says nothing about files hosted elsewhere.

| Path | Repository | Commit |
|---|---|---|
| src/openamrobot-interfaces | openAMRobot/openamrobot-interfaces | 50ed777be7990edbd3465f33fd97a158e7e3b88b |
| src/openamrobot-comm | openAMRobot/openamrobot-comm | 73fa694aa60594f1f99e813741d8f744ee302f8a |
| src/openamrobot-manipulation | openAMRobot/openamrobot-manipulation | be76d30632f01aab2badddf4e33de829c113b1b7 |
| src/openamr-platform-sw | openAMRobot/openamr-platform-sw | ddd20ab3a85d98bb78c4c5f014952c4a0717ef92 |
| src/openamr-upperbody-sw | openAMRobot/openamr-upperbody-sw | 1ab45a62957d238fc293eee08a8fd9158acebb01 |
| src/openamrobot-embodied-ai | openAMRobot/openamrobot-embodied-ai | 56bbd36ea313f3765df51524df07ccc6b2623f47 |
| firmware/openamr-platform-fw | openAMRobot/openamr-platform-fw | bad0567a58b1b5bb7b1df69b1b8b9950e600f504 |
| firmware/openamr-upperbody-fw | openAMRobot/openamr-upperbody-fw | ba1a53f2a031cdbfbe4fa0f5f4d32ed7cdf4dbbb |
| hardware/openamr-platform-hw | openAMRobot/openamr-platform-hw | 33941236db5fc2e651bf44dce97203f750a8f15e |
| hardware/openamr-upperbody-hw | openAMRobot/openamr-upperbody-hw | e760126b2b79611e0a915ab2bc11e15afb22cd8b |
| ui/openamrobot-ui | openAMRobot/openamrobot-ui | 2cf917950adef411bbdc54381865ea137c7b2e26 |
| docs/openamrobot-docs | openAMRobot/openamrobot-docs | 852c32c2b77fadbd119b1cc8c8fa5f629df5fbd2 |
| src/sllidar_ros2 | Slamtec/sllidar_ros2 | 34300099fadfc772965962dec837bf436706188f |
| src/micro_ros_agent | micro-ROS/micro-ROS-Agent | 7c932329ad5591ef23942ef1962534258c16b000 |

## Licences

Software and firmware MIT, hardware CERN-OHL-P-2.0, documentation CC-BY-4.0. Files derived from Apache-2.0 upstream work keep their notices: see `NOTICE.md` and `LICENSES/` in `openamr-platform-sw` and `openamr-upperbody-sw`.

## Contributing and attribution

Issues and pull requests are welcome in the component repositories; the contribution rules are in https://github.com/openAMRobot/.github/blob/main/CONTRIBUTING.md. The arms are OpenArm by Enactic (https://github.com/enactic), used unmodified under Apache-2.0 at the commits above. Navigation uses Nav2 and manipulation uses MoveIt 2; both are installed from the ROS 2 Jazzy packages. Thanks to everyone who wrote, reviewed and tested the work in this candidate.

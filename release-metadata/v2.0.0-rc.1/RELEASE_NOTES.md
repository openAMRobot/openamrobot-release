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
2. For a **pre-publication Candidate 2 verification installation** (not the final released installation), use the pinned verification checkout below. It must be checked out **before** running bootstrap:

   ```bash
   git clone https://github.com/openAMRobot/openamrobot-manifest.git
   git -C openamrobot-manifest checkout 24e903d951ea404d3fd8d7ce04353673382de2e4
   bash openamrobot-manifest/tools/bootstrap_digital_twin.sh "$HOME/oamr_dt_ws"
   source /opt/ros/jazzy/setup.bash
   source "$HOME/oamr_dt_ws/install/setup.bash"
   export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
   export CYCLONEDDS_URI='<CycloneDDS><Domain Id="any"><Discovery><MaxAutoParticipantIndex>120</MaxAutoParticipantIndex></Discovery></Domain></CycloneDDS>'
   ros2 launch openamrobot_build1_scene build1.launch.py profile:=fast rviz:=true
   ```

   This checkout is manifest `main` after PR #26 (hardware pin; #23 was merged as `68ccce3` with the earlier hardware pin). The clean install passed in 2 of 2 fresh environments on this exact commit ([run 46030163636](https://github.com/openAMRobot/openamrobot-manifest/actions/runs/46030163636)). Replace this preview instruction with the immutable published manifest revision before the release is tagged.
3. In a second terminal run the first demonstration: `ros2 run openamrobot_build1_scene run_scenario.py scn01_drive`.

No physical hardware is needed. No GPU was used in the automated tests (headless software rendering); requirements for a desktop session have not been measured.

## Not supported in rc.1

Operator UI and manual driving from the UI; camera-driven manipulation (object poses come from simulator ground truth); cancel and resume of a navigation goal (see below); docking; Isaac Sim and MuJoCo; LeRobot and other AI pipelines; Jetson deployment; firmware on 2.0 hardware; any physical commissioning. These repositories are in the archive as source snapshots at reviewed commits, without a support claim.

If the operator UI is started, rc.1 exposes rosbridge on port 9090 without a topic allowlist (ui#64 is not part of this candidate); a client on that port can publish `/cmd_vel` directly and bypass the command gate. Run the UI only on a trusted network and not while the base is powered for motion.

The full workspace manifest `manifests/v2.0.0-rc.1.repos` does not build as one workspace: the interfaces and the UI repository both provide the package `openamr_ui_msgs`. Use the supported profile.

## Candidate commits

| Component | Commit | Note |
|---|---|---|
| openamr-platform-sw | 2ac40702deaf3533f9612a1e05d1ea9bb41b996c | branch `release/2.0.0-rc.1`: `334e0ad`, a publication cleanup of documents (`ddd20ab`), and the SIL effective-track calibration with its regression tests (platform-sw #211: `sil.yaml`, `test_sil_config.py`). The `main` branch is not the candidate |
| openamr-upperbody-sw | 6687f65b8bd03f83ef6c38a7ddaf47eb3bfd18ac | branch `release/2.0.0-rc.1` since 27 Nov (upperbody-sw #146: code-owner approval, fast-forward) |
| openamrobot-interfaces | 50ed777be7990edbd3465f33fd97a158e7e3b88b | |
| openarm_description (upstream) | 14ff67b638ff1c738a1b9a6be8aaa5ce5ed2c831 | Apache-2.0 |
| openarm_ros2 (upstream) | 4e837e1d0dae692ff67b560b69d8d281d7a8d4ed | Apache-2.0 |
| openarm_can (upstream) | bfd4e52194aefe38389fa6e670be3738136facb9 | Apache-2.0 |

## Qualification evidence (simulation, hosted CI)

Release pair: upper body `6687f65b8bd03f83ef6c38a7ddaf47eb3bfd18ac` with platform `2ac40702deaf3533f9612a1e05d1ea9bb41b996c`. Every gate below ran on exactly this pair, each as a first attempt; an independent re-read of the original logs confirmed the table. No limit, threshold or timeout was changed.

| Gate | Result | Runs |
|---|---|---|
| Strict mission: 3 dispatches of 2 consecutive legs, 8 phases each | **3 of 3 verdicts, 6 of 6 legs, 48 of 48 phases.** One start-up try blocked (limitation 2) and repeated inside its job | [45826325912](https://github.com/openAMRobot/openamr-upperbody-sw/actions/runs/45826325912), [45826340366](https://github.com/openAMRobot/openamr-upperbody-sw/actions/runs/45826340366), [45826354243](https://github.com/openAMRobot/openamr-upperbody-sw/actions/runs/45826354243) |
| Odometry against ground truth in the mission, limit 0.100 m | 0.023 to 0.041 m in the six legs | same runs |
| Scene tests: 17 tests produce 19 results | **17 PASS, 1 FAIL, 1 XFAIL.** FAIL: `scn07_cancel_resume` (not supported). XFAIL: `scn17_base_yaw_fast` (limitation 4) | [45826367333](https://github.com/openAMRobot/openamr-upperbody-sw/actions/runs/45826367333) |
| Arm diagnostics | 10 of 10 jobs | [45826372314](https://github.com/openAMRobot/openamr-upperbody-sw/actions/runs/45826372314), [45826335990](https://github.com/openAMRobot/openamr-upperbody-sw/actions/runs/45826335990) |
| OpenArm emulator on virtual CAN | 66 tests, 0 failed, 0 skipped | [45826383251](https://github.com/openAMRobot/openamr-upperbody-sw/actions/runs/45826383251), [45826335981](https://github.com/openAMRobot/openamr-upperbody-sw/actions/runs/45826335981) |
| Model tests, static and mock (a6) | 927 executed, 0 failed, 21 skipped | [45826336167](https://github.com/openAMRobot/openamr-upperbody-sw/actions/runs/45826336167) |
| Model tests, simulation (a7) | 297 executed, 0 failed, 3 skipped | [45826377770](https://github.com/openAMRobot/openamr-upperbody-sw/actions/runs/45826377770) |
| Platform SIL protocol tests | 209 passed, 3 expected failures (platform-sw #159) | [45826145729](https://github.com/openAMRobot/openamr-platform-sw/actions/runs/45826145729) |
| Platform description, navigation status, drivers bring-up | passed | [45826150907](https://github.com/openAMRobot/openamr-platform-sw/actions/runs/45826150907), [45826156811](https://github.com/openAMRobot/openamr-platform-sw/actions/runs/45826156811), [45826162821](https://github.com/openAMRobot/openamr-platform-sw/actions/runs/45826162821) |
| Platform station alignment | required jobs passed; the Fast DDS job failed (limitation 9) | [45826167431](https://github.com/openAMRobot/openamr-platform-sw/actions/runs/45826167431) |
| Clean install on the release pins, 2 fresh environments | 2 of 2: bootstrap twice, 17 packages built, clock, robot description, TF, `scn01_drive` PASS, `scn16_lift_stops` PASS, one interrupt, relaunch, `scn04_grasp` PASS. On manifest `main` `24e903d` (after #26, hardware pin). Earlier on `442241a` and a commit with identical profile content | [46030163636](https://github.com/openAMRobot/openamrobot-manifest/actions/runs/46030163636); earlier [45871626093](https://github.com/openAMRobot/openamrobot-manifest/actions/runs/45871626093), [45855870217](https://github.com/openAMRobot/openamrobot-manifest/actions/runs/45855870217) |

What the mission evidence is and is not: the mission runs in the declared simulation-oracle setting. The pose used for planning and the pose of the item come from simulator ground truth. A pass shows the sequence, the control paths and odometry agreement. It is not a localization or perception result.

Earlier attempts, kept on record:

- **Previous candidate** (upper body `1ab45a6` with platform `ddd20ab`, effective track 0.400 m): strict mission 2 of 3 verdicts, 5 of 6 legs, 47 of 48 phases. Leg 2 of [45746635231](https://github.com/openAMRobot/openamr-upperbody-sw/actions/runs/45746635231) failed the odometry check with 0.10016 m against 0.100 m. It was not rerun to replace the result. The cause was found (limitation 1) and that candidate was not released.
- **Previous head of this candidate** (`7b60f62` with platform `4948644`, whose `ros2/` tree is identical to `2ac4070`): strict mission 3 of 3. On that head the emulator run [45817609565](https://github.com/openAMRobot/openamr-upperbody-sw/actions/runs/45817609565) stopped in the ROS set-up step with a 404 before any test; it is not counted as a pass, and the set-up step was pinned.
- **Platform SIL tests on `4948644`**, run [45817417389](https://github.com/openAMRobot/openamr-platform-sw/actions/runs/45817417389): attempt 1 had one failing timing test (platform-sw #198); attempt 2 passed every test and failed the workflow's own test count, because the change added one test. The count was corrected in `2ac4070`.
- **Pre-registered predictions for the calibration:** two were missed. The heading after the first turn was outside its band in one of four legs by 0.001 rad, and 2 of 16 legs exceeded the predicted 0.050 m. The value was kept as tested.

Human checks: one contributor ran the previous candidate on a real screen under WSL2 (installation, Gazebo, RViz and the drive scenario worked; upperbody-sw #143). A screen check of the release pair and a quick start walk-through by a second person are open.

## Not supported: cancel and resume

Cancel stops the base under control (0.12 s and 0.012 m in the traced run, goal status CANCELED). The resumed goal can end ABORTED when the progress checker fires near the station (platform-sw #207, root cause #201). The overall `scn07_cancel_resume` scenario **FAILED in both exact-head Candidate 2 scene runs** ([45826335970](https://github.com/openAMRobot/openamr-upperbody-sw/actions/runs/45826335970) and [45826367333](https://github.com/openAMRobot/openamr-upperbody-sw/actions/runs/45826367333)); successful cancellation of one goal is not successful cancel/resume. Cancel/resume remains unsupported in rc.1. An older report that the cancelled goal itself returns ABORTED (platform-sw #189) is still open; it did not occur in the runs listed here.

## Known limitations of supported behaviour

1. **Odometry depends on a simulation calibration.** The SIL effective track is 0.411 m; the model keeps 0.400 m. It is a calibration of the twin, not a chassis dimension: the simulated base turns 2.7 percent less than its wheel joints predict at 0.400 m (upperbody-sw #136). At 0.411 m, 16 of 16 mission legs measured 0.010 to 0.060 m against the unchanged 0.100 m limit (0.023 to 0.041 m on the release pair). The value corrects slightly too far. One leg showed 0.144 rad between odometry yaw and ground truth yaw at the station, recorded without a limit. The physical robot needs its own calibration.
2. **The simulation can freeze right after start.** In 2 of 14 start-ups of the mission the simulator published a few milliseconds of `/clock` and then stopped stepping. The cause is not known (upperbody-sw #135). CI detects it after 60 s, ends the processes of that try and starts again; every such try is listed in the verdict. If it happens to you: stop the launch with Ctrl+C and start it again.
3. **Station approach** can stop a few centimetres short and abort, about 1 time in 12 to 15 in earlier measurements. The mission fails closed and never reports a false success (platform-sw #207).
4. **Arm park in the `fast` profile.** `scn17_base_yaw_fast` is an expected failure: joint 4 of the arms on its lower limit does not move toward park with the DART physics engine while the controller reports success (upperbody-sw #126).
5. **Shutdown and repeatability.** `move_group` and `parameter_bridge` can exit with code -11 at shutdown, after results are complete. The mission seeds Python random and the ROS domain of the test (`BASELINE1_SEED`, checked by the mission gate), but Gazebo is started without a seed, and the model hash printed per launch differs at identical pins, so two runs are not guaranteed identical. Mean real-time factor of the mission runs was 0.13 to 0.18.
6. **Software in the loop.** Start-up standstill of the emulated drive in 2 of 65 earlier launches, and link-loss events from mixed wall and simulation clocks (upperbody-sw #137, #142). Simulation artefacts, not hardware evidence.
7. **RViz.** `build1.rviz` needs Nav2 and MoveIt both on (the defaults). The ground truth display is off by default because its frame is not in TF. RViz exits with an error at shutdown (upperbody-sw #143). Automated evidence is a configuration test only. A person has not yet checked RViz on a real screen for this candidate.
8. **Perception is not exercised.** The planning scene and object poses come from simulator ground truth.
9. **Middleware.** CycloneDDS only. Fast DDS loses samples under the mission load and one platform simulation job is red on it (platform-sw #197).
10. **Fidelity placeholders.** Wheel contact and friction, track width 0.400 m, drive dynamics and speed limits, camera poses and fields of view, battery constants; no power or brake model.
11. **Gate definitions are proposed values.** Known weaknesses for rc.2: the end-of-run liveness check passes when it is absent, the cancellation gate needs only one check, finger-to-item contact has no force cap, and the Stop check measures a base already at rest. The reverse-speed gate judges the forward drive at 0.010 m/s and reports the in-place turn separately (guarded by the 0.05 m turn-drift check).
12. **Clean install coverage.** The clean install check runs the `fast` profile headless: drive, lift, shutdown, relaunch and a left-arm grasp with the Bullet Featherstone engine. It does not cover RViz on a screen or the `firmware_sil` profile. The `firmware_sil` profile is exercised by the mission and scene gates on CI workspaces, without a screen. RViz and Gazebo on a real screen are not established for this pair: one contributor ran the previous candidate on a desktop, and the screen check of this pair by a person has not been done.
13. **Firmware.** No firmware image has been flashed on 2.0 hardware. The simulated mission uses host and emulator stand-ins; the safety state machine, drive enable, lift-permit producer and micro-ROS link are not implemented in the STM32H723 code.
14. **Timing-sensitive platform test.** `sil-tests` in platform-sw can fail on a slow runner (platform-sw #198).

## Safety statement

Simulation, software in the loop, emulators, fixtures and CI results are development evidence. They are not physical, electrical or safety acceptance, and functional telemetry, watchdogs and status displays are never safety evidence. There is no physical motion of 2.0 hardware until the bench gates are recorded, with wheels off the ground first and the hardwired stop chain tested on its own record. This is a research-grade pre-release, not certified for industrial, medical, safety-critical or unsupervised use.

## Source archive

Machine-readable files: `manifests/v2.0.0-rc.1.repos` (all pins) and the lock `release-config.rc1.json` (SHA-256 of the manifest and of every source archive, plus the exclusion list).

Two independent fetch builds from the lock are byte identical:

```
e1b6226c29ecddcf3ecc89833cd8f2fa2ad2fd1708e29c1ac5e24e98a13d85c6  OpenAMRobot-v2.0.0-rc.1-source.zip  (312147032 bytes, 3042 files verified)
```

The hosted `Pinned rc.1 release` workflow reproduced the same bytes ([run 46030504263](https://github.com/openAMRobot/openamrobot-release/actions/runs/46030504263)), and the downloaded artifact was verified independently. The published asset is the hosted artifact; its checksum is the one that counts. Only the source archive is reproducible; no compiled binaries are claimed. Inside the archive: `MANIFEST.json` (repositories, commits, source hashes, excluded files), `release.repos` and `checksums.sha256` covering every other file.

Which file to use: to run the Digital Twin, do not download the archive; use the supported profile in `openamrobot-manifest` as described above. The archive is the complete source record of the release.

Left out of the archive: 32 manufacturer files (25 datasheets and 7 other vendor files) under `hardware/openamr-platform-hw`, for which no redistribution right is documented. They are listed under `excluded` in `MANIFEST.json`. This is a packaging decision only; it says nothing about files hosted elsewhere.

| Path | Repository | Commit |
|---|---|---|
| src/openamrobot-interfaces | openAMRobot/openamrobot-interfaces | 50ed777be7990edbd3465f33fd97a158e7e3b88b |
| src/openamrobot-comm | openAMRobot/openamrobot-comm | 73fa694aa60594f1f99e813741d8f744ee302f8a |
| src/openamrobot-manipulation | openAMRobot/openamrobot-manipulation | be76d30632f01aab2badddf4e33de829c113b1b7 |
| src/openamr-platform-sw | openAMRobot/openamr-platform-sw | 2ac40702deaf3533f9612a1e05d1ea9bb41b996c |
| src/openamr-upperbody-sw | openAMRobot/openamr-upperbody-sw | 6687f65b8bd03f83ef6c38a7ddaf47eb3bfd18ac |
| src/openamrobot-embodied-ai | openAMRobot/openamrobot-embodied-ai | 56bbd36ea313f3765df51524df07ccc6b2623f47 |
| firmware/openamr-platform-fw | openAMRobot/openamr-platform-fw | bad0567a58b1b5bb7b1df69b1b8b9950e600f504 |
| firmware/openamr-upperbody-fw | openAMRobot/openamr-upperbody-fw | ba1a53f2a031cdbfbe4fa0f5f4d32ed7cdf4dbbb |
| hardware/openamr-platform-hw | openAMRobot/openamr-platform-hw | bf9fefa0250e4e59d4de4e634461d30689944357 |
| hardware/openamr-upperbody-hw | openAMRobot/openamr-upperbody-hw | e760126b2b79611e0a915ab2bc11e15afb22cd8b |
| ui/openamrobot-ui | openAMRobot/openamrobot-ui | 2cf917950adef411bbdc54381865ea137c7b2e26 |
| docs/openamrobot-docs | openAMRobot/openamrobot-docs | 852c32c2b77fadbd119b1cc8c8fa5f629df5fbd2 |
| src/sllidar_ros2 | Slamtec/sllidar_ros2 | 34300099fadfc772965962dec837bf436706188f |
| src/micro_ros_agent | micro-ROS/micro-ROS-Agent | 7c932329ad5591ef23942ef1962534258c16b000 |

## Licences

Software and firmware MIT, hardware CERN-OHL-P-2.0, documentation CC-BY-4.0. Files derived from Apache-2.0 upstream work keep their notices: see `NOTICE.md` and `LICENSES/` in `openamr-platform-sw` and `openamr-upperbody-sw`.

## Contributing and attribution

Issues and pull requests are welcome in the component repositories; the contribution rules are in https://github.com/openAMRobot/.github/blob/main/CONTRIBUTING.md. The arms are OpenArm by Enactic (https://github.com/enactic), used unmodified under Apache-2.0 at the commits above. Navigation uses Nav2 and manipulation uses MoveIt 2; both are installed from the ROS 2 Jazzy packages. Thanks to everyone who wrote, reviewed and tested the work in this candidate.

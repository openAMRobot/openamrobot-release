# OpenAMRobot v2.0.0-rc.1 release notes (DRAFT)

Status: draft for owner review, prepared 2026-11-20, refreshed 2026-11-22 01:30 UTC.
Update 2026-11-24 (platform-sw #164 merged; Track A limitations added). The pins table below is not repinned yet: the platform pin changes to c42a972 and the upperbody pin waits on #130.
Not published, not tagged. Trial builds only (local, see "Source pins and lock");
the published archive is built by CI after the merges in RUNBOOK.md. The release model is unchanged: this repository holds the release
archive and is the ground truth; version tags in component repositories are
navigation aids only.

| Version | Date | Meaning |
|---|---|---|
| v2.0.0-rc.1 | 2026-11-23 (planned 2026-11-20, missed; publication only on owner authorization) <!-- decision-allow: RELEASE-MILESTONES register keeps 20 Nov; owner chose RUNBOOK option B on 22 Nov 2026 --> | Pre-release: reviewed source state and simulation evidence, reduced scope (see Scope) |
| (bench window) | 2026-11-23 to 2026-12-18 | Physical integration, testing and acceptance |
| v2.0.0 | 2026-12-18 | Final release, only after the bench gates below are recorded |

## Scope (owner decision, 22 Nov 2026)

rc.1 is built from the reviewed main branch of each repository (manifest openamrobot-manifest #23). Not included and not claimed: strict Baseline 1 acceptance, Isaac Sim GPU evidence, the integration branches (upperbody-sw #77, platform-sw #161), and manual driving from the UI (the command gate platform-sw #90 and the UI command path ui #50 were merged on 22 Nov; the operator path is verified in simulation only, see the row "Manual driving from the operator UI"). If the code owners approve the Baseline 1 fixes and two consecutive strict legs pass on identical pins before publication, these notes are updated with that evidence; otherwise those items stay as listed below.

**rc.1 is a software and simulation candidate. No 2.0 hardware has been powered.
Nothing in this release is physical, electrical or safety acceptance.**

## Status labels

Only these labels are used.

- **merged and CI green**: on the repository's default branch; every check that ran on that commit passed (skipped checks are listed as not run).
- **demonstrated in simulation (run ID)**: a hosted CI run in simulation passed; development evidence only.
- **proposed (draft PR)**: open pull request (draft or ready), not merged; not release content.
- **blocked**: cannot proceed until a named dependency or decision is resolved.
- **not verified**: no evidence was found or recorded for this item.

## Status per subsystem

### Platform software (openamr-platform-sw)

| Item | Status | Evidence |
|---|---|---|
| main 69847ab: description, Nav2 config, base and lift software-in-the-loop on virtual CAN (#139) | merged and CI green | sil-tests and repository-quality pass on 69847ab; description and simulation workflows did not run on this commit (path filters) |
| Stop gate and command arbitration (#90) | proposed (draft PR) | open, changes requested on GitHub; not in main, not in the deployed robot build |
| Station approach for manipulation goals (#164) | merged (23 Nov 2026 23:24 UTC, merge commit c42a9724b33b6cd115543dbb51974c80e4fabffd) | not in the pins table yet (repin pending). On the merge commit: repository-quality, description-tests, description-gazebo-tests and producer-tests pass; **sil-tests failed** (Renode boot banner not seen within the fixed wait; runner-speed sensitivity tracked in #198; passed on the previous head). Simulation job results on the merge commit not read here |
| Recovery trees without reversing (#91, #92), station alignment (#167) | proposed (draft PR) | open; one tree owner and merge order pending |
| SDO reply matching in the drive host client (#169) | proposed (draft PR) | approved by the code owner at 5c8515f (20 Nov); still draft, not merged |
| Teleop topic (cmd_vel_teleop vs cmd_vel_joy) | blocked | contract change request #170 (Proposed) |
| Docking with the stop lock (#117, #124) | blocked | docking stays off in rc.1 |
| Integration branch integration/baseline1 fb25be1 (#161, never merged) | not verified | integration snapshot only; run 44464850846: simulation (rtf02) fails, other jobs pass |

### Upper body software (openamr-upperbody-sw)

| Item | Status | Evidence |
|---|---|---|
| main a3a93c6: combined robot description, MoveIt 2, OpenArm software in the loop on virtual CAN (#67), joint dynamics (#66), actuator ledger (#65) | merged and CI green | a6 (static+mock), sil (vcan, real driver), repository-quality pass; a7 (simulation) skipped, not run |
| Combined model platform pin | not verified | main pins platform-sw 8e7a454, three commits behind the rc.1 platform pin 69847ab; in a workspace imported from the rc.1 manifest C02 fails on that difference. Repin 8e7a454 -> 69847ab proposed in #74 (c0c405c): the expanded model keeps every link, joint, inertial and mesh, only six Gazebo friction blocks change (#135); on c0c405c a6 927 executed / 0 failed with C02 PASS (run 44739809301) and a7 297 executed / 0 failed (run 44739808961); draft, not merged |
| Lift permit wait (#94), lift emulator pin (#95), palm standoff (#98), scn03 targets (#99), measured arm park (#108) | proposed (draft PR) | code-owner reviews 20 Nov: #95 and #99 adopt, approval on a green head; #94 adapt; #98 conditions on the contact gate; none approved as of 22 Nov 01:30 UTC; not in integration/baseline1 |
| Integration branch integration/baseline1 18454ab (#77, never merged) | not verified | single validation leg with the strict gates, run 44848867373: 7 of 8 phases, no unaccounted contact, cancellation at the end 12 of 13 checks; fails on reverse speed 0.01306 m/s (limit 0.010), cancel-hold /cmd_vel peak 0.0755 (limit 0.001) and the end-of-run drive liveness check; scene tests, emulator tests and arm diagnostics fail on this head |

### Baseline 1 whole-robot mission (simulation)

| Item | Status | Evidence |
|---|---|---|
| Single-leg mission, 8/8 checks, three runs, integration d63e9ed with platform 931e631 | demonstrated in simulation (44309791416, 44309804809, 44309817813) | sim-oracle profile; recordings in upperbody-sw pre-release sim-baseline1-2026-11-18 |
| Two-leg strict sequence, 8/8 per leg, scratch branch eb920f0 with unreviewed fixes | demonstrated in simulation (44470870769) | diagnostic only: scratch branch, fixes not reviewed or merged |
| Mission with the read-only control room, demo/control-room 825ebfa | demonstrated in simulation (44593505369) | diagnostic only: draft PR #84 |
| Single validation leg with the strict gates, integration 18454ab | demonstrated in simulation, 7 of 8 (44848867373) | not acceptance: one leg, unreviewed integration head, three failed checks (row above) |
| Strict reviewed acceptance run on reviewed integration heads | not verified | not run; reasons below |

Why the strict reviewed acceptance has not been run:

1. Approvals are incomplete. upperbody-sw #94, #95, #98, #99 and #108 have no adopt from the code owner; platform-sw #178 (no-reverse configuration) has review comments, no approval; #167 has no current-head approval; #175 is approved but not applied to integration/baseline1.
2. Those fixes are not in the integration branches, so the branches do not carry the code the earlier diagnostic runs used.
3. The single validation leg on 18454ab (row above) fails three checks; the causes are under investigation and no threshold is changed.
4. Owner decisions taken 21 Nov: the retreat is turn-and-forward (no backup), the reverse-speed limit stays 0.010 m/s, strict acceptance needs two consecutive legs from one dispatch on identical full SHAs.
   Owner decisions taken 22 Nov (upperbody-sw issue #117, PRs #118, #123, #124; platform-sw #178, #182):
   - upperbody-sw #94, #95, #98, #99 adopted and approved by the code owner; not yet merged into the integration branch.
   - Reverse speed (C7): the gate judges the forward drive at 0.010 m/s (unchanged); the in-place turn is reported and guarded by the 0.05 m turn-drift check. Every report shows the gate value, the turn value and the earlier single-series value side by side, so the change cannot be read as a relaxed limit.
   - Cancellation hold: judged by message publication time; the report states the time basis, and any fallback to delivery time.
   - No-reverse platform configuration (#178) and the StationRetreat controller for the forward retreat (#182, consumer upperbody-sw #122) adopted by the navigation owner; the gate owner requires at least 5 retreat legs, all succeeded, and the clearance measured at the retreat end before relying on it. Without that evidence, rc.1 states that strict acceptance is not met because of the forward-retreat stall.
   - Two-leg preview with all of these on an evidence branch (run 44983640874): both legs 8 of 8 on identical pins; the strict verdict failed on one palm-to-item contact in grasp (0.349 N, leg 1). Not acceptance.
5. All runs use the sim-oracle profile (planning scene and object poses from Gazebo ground truth), so perception is not exercised.

Intended sequence once approvals exist: merge the fixes into the integration branches, move the pins, then one dispatch of baseline1-acceptance.yml (strict sequence, CycloneDDS) on upperbody-sw integration/baseline1.

### Digital twin components

| Component | Status | Evidence |
|---|---|---|
| Gazebo Harmonic whole-robot scene (Nav2, MoveIt 2, ros2_control, emulated lift and arm motors on virtual CAN) | demonstrated in simulation (44309791416) | integration branches only, sim-oracle |
| Base and lift SIL on virtual CAN | merged and CI green | platform-sw main 69847ab (#139) |
| OpenArm SIL on virtual CAN | merged and CI green | upperbody-sw main a3a93c6 (#67) |
| MuJoCo and Isaac Sim models with parity tests (#69, #80) | proposed (draft PR) | Isaac GPU job blocked (no GPU runner) |
| Firmware in Renode on the drive bus (#141, #144, #166) | proposed (draft PR) | telemetry image only, read-only |
| Read-only control room (#84) | proposed (draft PR) | 44593505369 |
| Grocery dark store demonstrator (#86) | proposed (draft PR) | run 44299879412: 10 of 12 phase checks; station offset 0.0497 m vs 0.04 m and odometry guard 0.907 m vs 0.56 m fail |
| SIL fidelity record (#168) | proposed (draft PR) | wheel contact, track, drive dynamics, camera poses, battery are placeholders |
| Public model bundle (#74) and tag model-2.0.0-rc.1 | proposed (draft PR) | #74 now triggers on model-2.0.0-rc.1 and model-2.0.0 (0364b2c, with tests) and carries the platform repin; model-owner additions open; tag does not exist |

### Firmware

| Item | Status | Evidence |
|---|---|---|
| platform-fw main bad0567: Gate A Teensy build, host module tests | merged and CI green | Host module tests, host-tests, teensy40 pass; no STM32 job runs on main |
| STM32H723 CubeMX project (#22) | proposed (draft PR) | STM32H723 Debug and Release build in CI on e7bcbd9; never flashed, no CAN on a bench |
| Renode | not verified | Renode runs the telemetry image only (#51, #55 drafts); no motion or safety logic is exercised |
| SDO client reply matching on the bench scripts (#62, #63) | blocked | the bench scripts on the real drive use the client with the bug; fix in draft #63 |
| upperbody-fw main ba1a53f | merged and CI green | documentation only (lift interface on CAN3); no lift firmware on main |
| Gate A (Teensy/MPU6500) and Gate B (STM32/ICM-42688-P) | not verified | kept distinct; Jetson is the 2.0 compute |

### Hardware

| Item | Status | Evidence |
|---|---|---|
| platform-hw main 8ed2b06: CAD, drawings, BOM, electrical, datasheets | merged and CI green | hardware-checks pass (text and structure checks, not design verification) |
| CAD mass properties of the 2.0 base (#43) | proposed (draft PR) | open, CI green, no review; chassis 18.549 kg from STEP vs 15.766 kg in the ledger |
| 2.0 hardware powered | not verified | no 2.0 hardware has been powered |
| Bench gate: LiDAR /scan publishing | blocked | /scan has no publisher on the bench robot; serial, permissions and S3 baud unchecked |
| Bench gate: stop gate deployed with a recorded Stop and Resume test | blocked | depends on #90 |
| Bench gate: teleop path through the gate | blocked | depends on #170 |
| Bench gate: CAN host client to the drive | blocked | depends on #62 and #63 |

### Interfaces, UI, embodied AI, documentation

| Item | Status | Evidence |
|---|---|---|
| interfaces main 50ed777 (includes StopState.msg, #35) | merged and CI green | quality/build, repository-quality pass |
| interfaces C9 components and radians (#39, #42) | proposed (draft PR) | Proposed contracts |
| ui main 51b4af3 | merged and CI green | ROS build and tests, web build and tests, Playwright route smoke test pass |
| Manual driving from the operator UI | not supported in rc.1 | not exercised on hardware. The code is merged: platform-sw #90 (9865468) and ui #50 (8df8415), both 22 Nov 2026; ui main 713345ac publishes TwistStamped on /ui/cmd_vel and binds /safety/stop_lock. The operator path is verified in simulation only (command path end to end, Stop during motion, Resume, readiness, fault handling; Nikolai Goloborodko, measured on platform 3aa17d2 / ui 21e95b9). The hardware gates (stop gate deployed, LiDAR publishing, teleop contract) are open, so it must not be treated as a supported capability. **The pins table below still names ui 51b4af3, which predates #50; the rc.1 repin must move ui to a commit that includes it, or this row must say the pinned UI still publishes /cmd_vel directly.** |
| ui rc.1 issues #31, #32, #33 | proposed (draft PR) | fixes in drafts #40 to #55, combined in integration candidate #56 |
| embodied-ai main 56bbd36 | merged and CI green | quality/python, quality/ros2 pass; the bag to LeRobot converter is in draft #8 |
| AI dataset: upperbody-sw pre-release dev-evidence-baseline1-c9-2026-11-19 | not verified | development evidence, not validated: 1 episode, 543 frames, simulation; Proposed conversion rules; C10 result NOT_VERIFIED |
| docs main 852c32c | not verified | merged; no CI ran on this commit |
| openamrobot-comm, openamrobot-manipulation, openamr-upperbody-hw, governance | not verified | main HEAD read with git; CI not read for this draft |

## Known limitations

Added 24 Nov 2026 (Track A, simulation only, from platform-sw #164 and the firmware/SIL readiness statement of 23 Nov):

- Station approach aborts about 1 time in 12 to 15; the mission fails closed and never reports a false success (platform-sw #192). The navigation owner decided on 23 Nov that it is a known limitation for rc.1 and the fix is a follow-up. Issue #192 was closed automatically when #164 merged, without a fix; the rc.2 fix is tracked in platform-sw #201.
- `scn07_cancel_resume` failed 5 times in 24 runs. Traced to the same stall as #192 (the base stops about 4 cm short, linear command 0.0, angular alternating, retries start from the same pose); nonblocking on the same basis.
- `simulation (rtf02)` (real-time factor 0.2) is red on Fast DDS (platform-sw #197, nonblocking). CycloneDDS is the supported middleware for rc.1.
- `sil-tests` is sensitive to runner speed (tracked in platform-sw #198); it is not a defect in the robot software. It failed on the #164 merge commit because Renode did not print its boot banner within the fixed wait. Earlier it failed on a different check, a low SDO upload count. These are two different timing/count checks, not one failure repeating.
- Upperbody scene tests: no `/clock` at start-up (#135), a lift-permit gap (#132), one odometry outlier (#136), rare palm contact in grasp (#134; contact cap stays 1.0 N), and one retreat that ended 3 mm short of its window in 12 legs (issue to be opened).
- A cancelled goal reports ABORTED, not CANCELED (#189); motion stops correctly, only the reported code is wrong.
- The 2 s clean-boot Resume bound (D-13) is not evidenced on hardware; multi-step missions and Stop mid-mission are unverified.
- Firmware: STM32H723 board support (platform-fw #22) is an initialization baseline, not operational firmware. Read-only telemetry (#51, draft) has L3 evidence on Renode's H743 model only. Not implemented in STM32H723 code: safety state machine, drive enable and commands, lift-permit producer, CAN3 reader, micro-ROS link; the simulated mission uses host and emulator stand-ins. Watchdog values (ZLAC 250 ms, drive heartbeat 100 ms, base consumer 300 ms) await bench capture. The ArmStatus/STOWED contract is undefined.
- Gazebo is the release twin for rc.1. MuJoCo and Isaac Sim are experimental and outside the critical path.
- Baseline 1 results in this release are simulation evidence only. They are not real-robot, hardware, electrical or safety acceptance.
- C7 measurement change: the reverse-speed gate judges the forward drive at 0.010 m/s (limit unchanged); the in-place turn is reported separately and guarded by the 0.05 m turn-drift check. Each report shows the gate value, the turn value and the earlier single-series value side by side, so the change cannot be read as a relaxed limit (owner decision, 22 Nov; upperbody-sw #117, #118, #123, #124).
- Forward retreat: the retreat is turn-and-forward (no backup). The StationRetreat controller (platform-sw #182) was adopted; the gate owner requires at least 5 retreat legs, all succeeded, with the clearance measured at the retreat end. One retreat ended 3 mm short of its window in 12 legs. Without that evidence, strict acceptance is not met because of the forward-retreat stall.
- Arm park-return flake: named as a known gap by the upperbody code owner on 22 Nov. Issue number and rate TBD; not verified here.

Earlier entries, still valid:

- Shelf approach (StationApproach controller, simulation): the controller can declare the goal reached a few centimetres short and then stall; seen once (run 44974892529), passed on retry. Root cause in upperbody-sw issue #117.

- Simulation runs use the sim-oracle profile; perception, real sensor noise and real contact are not exercised.
- Simulation fidelity placeholders: wheel contact shape and friction, track width 0.400 m, drive dynamics and speed limits (Gazebo 1.0 m/s vs the 0.5 m/s ceiling), camera poses and fields of view, battery constants; no power or brake model.
- Fast DDS loses camera and pose samples under the Baseline 1 load; acceptance is planned on CycloneDDS, which the robot runs.
- Odometry drifts in turns in simulation because of wheel slip; odometry numbers are not a reference yet.
- Docking is off. Reversing is not allowed in ordinary navigation by decision D-19; the integration branch does not yet enforce it.
- The combined upper-body model on main is generated against an older platform-sw commit (8e7a454) unless #74 merges before the build (RUNBOOK.md, step 2).
- The rc.1 builder (PR #12) is merged (a8f60f6). The parity check stays red until openamrobot-manifest #23 carries the same pins (RUNBOOK.md, step 3).
- No firmware image has been flashed on 2.0 hardware. The STM32 project is not on main.

## Safety statement

Simulation, software in the loop, emulators, Renode, fixtures and CI results are
development evidence. They are not physical, electrical or safety acceptance, and
functional telemetry, watchdogs and status displays are never safety evidence.
There is no physical motion of 2.0 hardware until the bench gates above (LiDAR,
deployed stop gate with a recorded Stop and Resume test, teleop through the gate,
CAN host client fix) are recorded, with wheels off the ground first and the
hardwired stop chain tested on its own record. This is a research-grade
pre-release, not certified for industrial, medical, safety-critical or
unsupervised use.

## Source pins and lock

Rule: the reviewed default branch of each repository. Integration branches appear
only in the separate integration snapshot. Machine-readable files:
`manifests/v2.0.0-rc.1.repos` (the pins, at the repository root), the lock
`release-config.rc1.json` (SHA-256 of the manifest and of every source archive)
and `integration-snapshot.repos` in this directory.

Trial builds, 20 Nov 2026, local, two independent `--fetch` builds from the lock
(not the published artifact): 15 sources, 3061 files verified, `cmp` identical.

```
657ed9b3aa59d9c669af53bcf1ff2612d1b068c969af3cd966b9d76ae1f6530c  OpenAMRobot-v2.0.0-rc.1-source.zip  (400568111 bytes)
```

| Path | Repository | Commit | Basis |
|---|---|---|---|
| src/openamrobot-interfaces | openAMRobot/openamrobot-interfaces | 50ed777be7990edbd3465f33fd97a158e7e3b88b | main, CI green; carries StopState.msg used by the stop gate and by the 19 Nov runs |
| src/openamrobot-comm | openAMRobot/openamrobot-comm | 73fa694aa60594f1f99e813741d8f744ee302f8a | main; CI not read |
| src/openamrobot-manipulation | openAMRobot/openamrobot-manipulation | be76d30632f01aab2badddf4e33de829c113b1b7 | main; CI not read |
| src/openamr-platform-sw | openAMRobot/openamr-platform-sw | 69847ab7c9c6cd49b3022dc1a62f86c044ba10ff | main, CI green |
| src/openamr-upperbody-sw | openAMRobot/openamr-upperbody-sw | a3a93c60b0de2865c6ce09499cfad566d7072659 | main, CI green (a7 skipped) |
| src/openamrobot-embodied-ai | openAMRobot/openamrobot-embodied-ai | 56bbd36ea313f3765df51524df07ccc6b2623f47 | main, CI green; new entry for 2.0 |
| firmware/openamr-platform-fw | openAMRobot/openamr-platform-fw | bad0567a58b1b5bb7b1df69b1b8b9950e600f504 | main, CI green |
| firmware/openamr-upperbody-fw | openAMRobot/openamr-upperbody-fw | ba1a53f2a031cdbfbe4fa0f5f4d32ed7cdf4dbbb | main, documentation only |
| hardware/openamr-platform-hw | openAMRobot/openamr-platform-hw | 8ed2b06a46115abe2dffadbf0d902ae731d278d1 | main, CI green |
| hardware/openamr-upperbody-hw | openAMRobot/openamr-upperbody-hw | e760126b2b79611e0a915ab2bc11e15afb22cd8b | main; CI not read |
| ui/openamrobot-ui | openAMRobot/openamrobot-ui | 51b4af38d6b7eeb260610e8ab2ebde0a340beea9 | main, CI green |
| docs/openamrobot-docs | openAMRobot/openamrobot-docs | 852c32c2b77fadbd119b1cc8c8fa5f629df5fbd2 | main; no CI on this commit |
| src/sllidar_ros2 | Slamtec/sllidar_ros2 | 34300099fadfc772965962dec837bf436706188f | unchanged upstream pin |
| src/micro_ros_agent | micro-ROS/micro-ROS-Agent | 7c932329ad5591ef23942ef1962534258c16b000 | unchanged upstream pin |
| governance/.github | openAMRobot/.github | 87c848617bd9a2135a5c75e1aaa54be8f8955556 | main |

Integration snapshot (not release content), heads read 2026-11-20 19:00 UTC:
platform-sw integration/baseline1 fb25be1b56652316f47b7505cef021576822c558 (#161);
upperbody-sw integration/baseline1 196dd3fe64900ba4a12124c9ee20e0cfaafa1651 (#77).
The runs above name the older commits they ran on.

Simulation evidence pre-releases referenced (upperbody-sw, all pre-releases,
simulation only): sim-baseline1-2026-11-18 (5df600b), sim-grocery-demo-2026-11-18
(eb9c34f), sim-videos-2026-11-19 (5905f61), dev-evidence-baseline1-c9-2026-11-19 (a207463).

## Next steps before publication

Follow `RUNBOOK.md` in this directory: merge order, build, checksum check,
draft release, the Baseline 1 decision and the switch to pre-release.

Open before publication (source compliance audit of the pinned archive, comment on this pull request, 22 Nov 2026):
- Prices and payment links in three public READMEs; removal proposed for the owner's decision (platform-sw #181, platform-hw #44, ui #65).
- Apache-2.0 derived files without NOTICE entries and package.xml licence tags missing a second licence; fixes in review (platform-sw #180, upperbody-sw #121).
- 25 vendor datasheets in platform-hw without a documented redistribution right; owner and legal decision (remove, exclude from the archive, or obtain the right).
Each merged fix moves an rc.1 pin: manifest #23 and this pull request are then re-pinned and the archive rebuilt and re-checked.

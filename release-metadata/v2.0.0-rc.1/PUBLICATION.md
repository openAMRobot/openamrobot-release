# v2.0.0-rc.1 publication sheet

Prepared 26 November 2026. Nothing in this file has been executed. No tag and no release exists. Every step after "Preconditions" waits for the owner's explicit GO.

## Preconditions (all must be true)

| # | Condition | State on 26 Nov, 21:50 CET |
|---|---|---|
| 1 | openamr-platform-sw `release/2.0.0-rc.1` is at `2ac40702deaf3533f9612a1e05d1ea9bb41b996c` | done |
| 2 | openamr-upperbody-sw `release/2.0.0-rc.1` is at `6687f65b8bd03f83ef6c38a7ddaf47eb3bfd18ac` | done, 27 Nov 13:27 UTC (code-owner approval, fast-forward) |
| 3 | Contributor agreement of upperbody-sw #141 is signed | open: status pending for the account that has not signed |
| 4 | openamrobot-manifest #23 is merged at the candidate 2 pins with hardware `bf9fefa` (head `c567f178a56c9e7c739617e2350e17ba125a5283`) | open: clean install on the new head, then current-head approvals of the manifest owner and the software lead, then merge |
| 5 | `Pinned rc.1 release` on the head of openamrobot-release #18 is green and its artifact has SHA-256 `e1b6226c29ecddcf3ecc89833cd8f2fa2ad2fd1708e29c1ac5e24e98a13d85c6` | open: needs condition 4 |
| 6 | openamrobot-release #18 is approved and merged | open: needs condition 5 |
| 7 | openamrobot-docs #102 is approved by the documentation owner | open: verdict so far "adapt", five points applied |
| 8 | Owner's GO | open |

## Tags

Four repositories get the tag `v2.0.0-rc.1`. They are the ones a user or auditor addresses by tag.

| Repository | Tag | Target commit | Why |
|---|---|---|---|
| openAMRobot/openamrobot-release | `v2.0.0-rc.1` | merge commit of #18 | carries the GitHub release, the archive and the checksum |
| openAMRobot/openamrobot-manifest | `v2.0.0-rc.1` | merge commit of #23 | installation entry point: users check out this tag and run the bootstrap script |
| openAMRobot/openamr-platform-sw | `v2.0.0-rc.1` | `2ac40702deaf3533f9612a1e05d1ea9bb41b996c` | qualified source |
| openAMRobot/openamr-upperbody-sw | `v2.0.0-rc.1` | `6687f65b8bd03f83ef6c38a7ddaf47eb3bfd18ac` | qualified source |

Not tagged: the twelve other repositories of the source inventory (interfaces, hardware, firmware, UI, embodied AI, comm, manipulation, docs, and the two third-party repositories). Their exact commits are in `MANIFEST.json` inside the archive and in `manifests/v2.0.0-rc.1.repos`. A tag there would suggest that their function is part of the supported Digital Twin, which it is not. The documentation is versioned by its path (`.../digital-twin/rc1/`).

## Sequence after GO

1. Download the artifact `OpenAMRobot-v2.0.0-rc.1-candidate` of the green hosted run into `./candidate/` and verify: `(cd candidate && sha256sum -c OpenAMRobot-v2.0.0-rc.1-source.zip.sha256)`; the hash must be the one in condition 5.
2. Tag the two source repositories (annotated tags, exact commits):
   ```sh
   git -C openamr-platform-sw tag -a v2.0.0-rc.1 2ac40702deaf3533f9612a1e05d1ea9bb41b996c -m "OpenAMRobot 2.0 rc.1 Digital Twin"
   git -C openamr-platform-sw push origin v2.0.0-rc.1
   git -C openamr-upperbody-sw tag -a v2.0.0-rc.1 6687f65b8bd03f83ef6c38a7ddaf47eb3bfd18ac -m "OpenAMRobot 2.0 rc.1 Digital Twin"
   git -C openamr-upperbody-sw push origin v2.0.0-rc.1
   ```
3. Tag the manifest at the merge commit of #23 the same way.
4. Documentation: one commit on openamrobot-docs #102 replaces the pre-publication line `git -C openamrobot-manifest checkout c567f17...` by `git -C openamrobot-manifest checkout v2.0.0-rc.1` in `installation.md` and `quick-start.md`, removes the pre-publication notes, and the same in the install preview of `RELEASE_NOTES.md` here. Strict build, then the documentation owner merges #102; the site deploys from `main`.
5. Create the release as a draft, with the hosted artifact (command in RUNBOOK.md section 7; it attaches the archive, its checksum file, the manifest and the lock). The tag `v2.0.0-rc.1` of this repository is created by that command on the merge commit of #18.
6. Check the draft: download both files from the draft, verify the checksum again, open the notes.
7. Publish: `gh release edit v2.0.0-rc.1 --repo openAMRobot/openamrobot-release --draft=false`. It stays marked as a pre-release.

In the GitHub web interface, steps 5 to 7 are: Releases, "Draft a new release", tag `v2.0.0-rc.1` on the merge commit of #18, title "OpenAMRobot 2.0 rc.1: Digital Twin", paste `RELEASE_NOTES.md`, attach the four files, tick "Set as a pre-release", "Save draft", verify, "Publish release".

## What a user downloads

The release asset `OpenAMRobot-v2.0.0-rc.1-source.zip` is the coordinated source snapshot of all 14 repositories at their pinned commits (3,042 files, 312,147,032 bytes). GitHub also shows "Source code (zip)" and "Source code (tar.gz)" on every release: those two are only this builder repository. The first lines of the release text say which file is which.

## After publication

- From a machine that was not involved: download the asset and the checksum file from the public release page and run `sha256sum -c`.
- Follow the published quick start from a clean Ubuntu 24.04 machine using the tag.
- Check that https://docs.openamrobot.ai/ shows the rc.1 section and that the links to the release resolve.
- Record the release URL, the asset hash and the time in the evidence register.

## Public description (first paragraph of the release text)

OpenAMRobot 2.0 rc.1 is the first release candidate of the Digital Twin of the OpenAMRobot 2.0 mobile manipulator: a mobile base, a lift and two arms in Gazebo Harmonic with ROS 2 Jazzy, Nav2, MoveIt 2 and device emulators on virtual CAN. It is simulation software for developers. It is not hardware, physical acceptance or safety evidence. **Download `OpenAMRobot-v2.0.0-rc.1-source.zip`** for the complete source record; the automatic "Source code" files below contain only the release tooling. To run it, follow the quick start in the documentation.

## Acknowledgements (proposal, the documentation owner decides the list)

Reviews and decisions for this candidate, by GitHub account: skunal3318 (navigation), Evans-Kwashie (SIL and base controller), panthera-momagdii (upper body), KARTHIKEYAN124 (manifest and release), wikki26 (desktop verification), anandgawai123456-glitch (documentation). Arm description, drivers and CAN library: the upstream OpenArm project (Apache-2.0). Further contributors are named in the AUTHORS and commit history of each repository.

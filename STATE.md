# Release builder state

OA-05 adds a candidate v2.0.0-rc.1 source bundle from exact Git SHAs and a
reviewed SHA-256 source lock. The 2026-10-19 snapshot is for reproducibility
validation; it is not the final release selection or acceptance evidence.

The v0.0.1 archive-input path remains available. The rc.1 path uses the same
build and validation entry points and preserves workspace checkout paths.
Source archive checksums use canonical, uncompressed ZIPs produced from verified
Git commits. Output ZIP metadata and ordering are deterministic.

Integrated main at `c39eda7` on 2026-10-24 after PR #9 merged navigation
installation validation and PR #8 merged the release model. The existing
navigation gate, test configuration, source provenance and compact evidence
remain intact. The archive-input builder still rejects navigation evidence,
archive, pin, package-version and contract mismatches.

The original candidate source pins are unchanged by the rebase. Repinning to
the accepted interfaces contract/package version and final rc.1 component
selection remain separate release work. The release-local snapshot still
requires owner alignment with the workspace release manifest.

Fresh Linux CI exposed host-dependent Git archive line endings in the old
Windows-generated source lock. Export now fixes autocrlf/eol settings; the
source lock is regenerated from the same SHAs. A regression test checks that
opposite host autocrlf defaults produce the same source hash. Checksum
enforcement remains strict; the earlier cached-bundle hash is historical.

No safety implementation is changed. Source bundling does not validate package
builds, firmware, robot operation, physical safety or release readiness.
Upstream build-time downloads are not locked by this source bundle.

Prepared 2026-10-28: pinned-release CI now compares the complete repository
mapping with openamrobot-manifest main's releases/v2.0.0-rc.1.repos. Only
governance/.github is exempt; missing files, missing entries and changed URLs
or SHAs fail. The 19 October source pins and checksums are unchanged.
Manifest PR #17 merged at 80161e5 and #18 merged at d9ab9db. The
workspace main now includes all 13 matching entries, including both drivers.
The historical #17-only snapshot correctly failed for both missing drivers.
On 2026-10-30 the old workflow rerun required unavailable repository admin
rights. This state update triggers fresh PR checks with the source pins,
source checksums and builder code unchanged; hosted results remain pending.

2026-11-20: the manifest moves to the reviewed main of each repository read on
2026-11-20 (release-metadata/v2.0.0-rc.1/RELEASE_NOTES.md lists them) and adds
openamrobot-embodied-ai. The lock is regenerated with lock_release_sources.py
from those SHAs; unchanged entries (upperbody-fw, sllidar_ros2,
micro_ros_agent) keep their previous source hashes. Two local fetch builds gave
identical bundles. The parity check passes only after openamrobot-manifest main
carries the same SHAs (patch in release-metadata/v2.0.0-rc.1/).

2026-11-20 evening: pins unchanged (every pinned main and the micro-ROS-Agent
jazzy branch read at 18:55 UTC equal the manifest), lock unchanged; one local
fetch build again gave sha256 657ed9b3...6530c, 400568111 bytes. The manifest
patch still applies to openamrobot-manifest main 5b782ac and its 42 tests pass.
RUNBOOK.md was dry-run and corrected: merge commits are disabled in this
repository (step 1a), #12 and #18 each need a code-owner approval other than
their author's, the patch is fetched at a fixed commit, the manifest PR body is
prepared (openamrobot-manifest-pr-body.md), the checksum and pin checks are
single commands for PowerShell and bash, and step 8 is the publication-day
status refresh. The integration snapshot records the current heads (upperbody-sw
196dd3f), still not release content. README labels the v0.0.1 Raspberry Pi as
legacy (COMPUTE). release-metadata/RELEASE_NOTES.md (v0.0.1 notes, unchanged)
still names the Raspberry Pi 5 without a legacy label; it is historical metadata
of the v0.0.1 builder and is left for the owner.

2026-11-25: documentation-only preparation supersedes the stale Monday runbook.
Builder #12 is merged; final platform/upperbody main pins, publication audit
closure and fresh hosted evidence remain pending. No pins or lock changed.
No tag or release, including draft publication, without Alex authorization.

Prepared 2026-11-25 (Proposed, draft): the pinned builder accepts an optional
`exclude` mapping in the release config (component to exact file paths). The
listed files are left out of the bundle and named under `excluded` in
MANIFEST.json; the source checksum still covers the whole pinned commit. A
listed path that is not in the source fails the build. Without the key the
bundle is unchanged. `lock_release_sources.py --exclude-file` copies the
mapping into a new lock. Reason: owner decision of 25 Nov on #18 to leave the
manufacturer files under openamr-platform-hw `datasheets/` out of the rc.1
archive. No pin, lock or release config is changed by this entry.

## v2.0.0-rc.1 candidate, 26 Nov 2026

`manifests/v2.0.0-rc.1.repos` equals openamrobot-manifest #23: platform software `2ac4070` and upper body software
`6687f65` (candidate 2; provisional until both are on their release branches) on their `release/2.0.0-rc.1` branches, platform hardware `3394123`, UI `2cf9179`. The lock
`release-config.rc1.json` was regenerated with the 32-path exclusion (`release-metadata/v2.0.0-rc.1/exclude.json`).
Local rehearsal: two fetch builds byte identical, SHA-256 `e1b6226c…85c6` (27 Nov, candidate 2 pins with hardware `bf9fefa`), 3,042 files verified, 0 of 32 excluded
files present. The hosted `Pinned rc.1 release` check stays red on manifest parity until #23 is on manifest `main`.
Release notes rewritten for the Digital Twin scope with every attempt listed; the strict mission target (3 of 3
verdicts on the candidate) was not met: 2 of 3, one leg failed the odometry check by 0.16 mm. Not published, not
tagged. Publication commands are in `release-metadata/v2.0.0-rc.1/RUNBOOK.md`, section 7.

Hardware pin, 27 Nov 2026: `manifests/v2.0.0-rc.1.repos` pins openamr-platform-hw `bf9fefa0250e4e59d4de4e634461d30689944357` (squash merge of openamr-platform-hw#49: public extracts of BOM Issue 7.15 and B-02 rev18.11). The regenerated lock differs from the previous one only in `manifest_sha256` and the hardware source hash; 32 exclusions kept. Two fetch builds from empty directories are byte identical: SHA-256 `e1b6226c29ecddcf3ecc89833cd8f2fa2ad2fd1708e29c1ac5e24e98a13d85c6`, 312,147,032 bytes, 3,042 files verified; the three snapshot files are in the archive and contain no personal names. The earlier `b13a77f1…` describes the archive without the hardware extracts and is no longer an acceptance value. The hosted build is still to run.


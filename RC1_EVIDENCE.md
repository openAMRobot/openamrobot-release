# OA-05 verification

Candidate snapshot date: 2026-10-19.
Base: `b9f4a9d2a1845ab50769693240a3050cf0f6d171`.
The PR head is recorded in the PR description after committing.

## Regression and fault injection

`python -m unittest discover -s tests -v`: **16 tests, 0 failures** on
Windows with Python 3.14 and Git 2.55.0.windows.5. Tests cover exact SHA fetch
arguments, fetched commit mismatch, submodule rejection, mutable refs,
duplicate keys, changed manifest bytes, changed cache bytes, fetched archive
checksum mismatch, incorrect archive commit, missing checksum coverage,
tampered output, extra output members, unsafe paths, executable/link modes,
ZIP metadata normalization, reproducible output and CLI dispatch.
The legacy v0.0.1 build and validator pass using eight fixture source archives.
Fixture tests establish packaging behavior, not component build acceptance.

Before-change regression: ran `scripts/build_release.py` from base `b9f4a9d`
against `release-config.rc1.json` in a temporary output directory. It exits 1
with `KeyError: 'components'`. The updated entry point accepts the same config.

## Independent real-source builds

Executed separately, each fetching all 14 repositories into a new temporary
Git repository and using separate source caches:

```sh
python scripts/build_release.py --config release-config.rc1.json --input-dir input/first --output-dir dist/first --fetch
python scripts/build_release.py --config release-config.rc1.json --input-dir input/second --output-dir dist/second --fetch
python scripts/validate_release.py dist/first/OpenAMRobot-v2.0.0-rc.1-source.zip
```

Both builds exit 0, each verifies **1,841 files**, and byte comparison using
Python `filecmp.cmp(..., shallow=False)` passes. The bundle is 231,082,934 bytes.

SHA-256 for both bundles:

```text
2f87bf21a99add7fb3aa37b2965943c4ac6fa390054476b5ea5293f6500fed41
```

The SHA inventory and commit provenance are inside each bundle; the external
`.zip.sha256` accompanies it. Generated ZIPs and source caches are not committed.
The new hosted workflow repeats two independent fetches/builds on Ubuntu 24.04
and uploads the validated candidate, without publishing a GitHub Release.

## Linux packaging check

Ran the following with the repository mounted at `/work` in the local
`ros:jazzy-ros-base` image (image ID
`sha256:c3706ef0a0aa45413c07803cf433602f543b22e45b4855f6fca955c2d8ecc4e8`):

```sh
python3 -m unittest discover -s tests -v
python3 scripts/build_release.py --config release-config.rc1.json --input-dir input/rc1 --output-dir dist/linux
python3 scripts/validate_release.py dist/linux/OpenAMRobot-v2.0.0-rc.1-source.zip
```

**16 tests, 0 failures**; build and validation exit 0. The Linux build uses
the verified source cache and verifies 1,841 files. Its bundle has the same
SHA-256 shown above as both independently fetched Windows builds. This proves
cross-platform packaging for this candidate; it is not a Linux source fetch
or ROS package compilation check.

## Not verified

Full Ubuntu/Jazzy workspace compilation, third-party build-time dependency
pinning, firmware builds, drivers on physical hardware and rc.1 acceptance
are outside this source-packaging verification. No hardware or safety claim
is made. Hosted CI status is reported separately from local test results.

## Integration and provenance

PR #9's navigation-install work and PR #8's release-model documentation were
inspected. This change preserves the legacy builder path and keeps the rc.1
procedure in a separate document. No assertion is made about inaccessible work.
The release-local manifest will be aligned with OA-39 after review; it includes
13 workspace repositories plus the release-only governance source.

Prepared with OpenAI Codex: implementation, candidate lock, tests, workflow
and documentation. No safety logic or third-party source was authored or
modified. Third-party source and licence notices remain in their exports;
tooling dependency and upstream licences are described in RC1_RELEASE.md.

## Rebase validation, 2026-10-24

Rebased onto main `c39eda70d8cf2e4f98ae09a51afc3a0750350a11` after navigation gate PR #9
merged as `0c9442fff722ce56567ebc106dc6ca38afcb9e3d` and release-model PR #8
merged. Pre-rebase head: `58ce4a24e6a1b9619332a59f44217fb1fd55c70b`.
The original source pins and source checksum lock are unchanged.

```sh
python -m unittest discover -s tests -v
python scripts/build_release.py --config release-config.rc1.json --input-dir input/rc1 --output-dir dist/rebase-20261024
python scripts/validate_release.py dist/rebase-20261024/OpenAMRobot-v2.0.0-rc.1-source.zip
```

**27 tests, zero failures**, including all 11 merged navigation gate/config/
provenance tests and 16 pinned-release tests. The real-source build from the
existing verified cache exits 0 and verifies 1,841 files. Its SHA-256 remains
`2f87bf21a99add7fb3aa37b2965943c4ac6fa390054476b5ea5293f6500fed41`.
No fresh network source fetch or physical/ROS package build is claimed by
this cached packaging run.

Conflict resolution retains main's evidence byte-preservation attributes,
archive ignores and release-model documentation. The merged navigation
manifest, navigation-only config, verifier scripts, workflow and compact
evidence are unchanged relative to main. Only rc.1 dispatch is added to the
archive-input builder; its navigation validation remains intact.

Fresh hosted check results on the new head are reported in PR #12. This rebase
is not a new rc.1 interfaces/package-version repin or final release selection.

## Fresh-fetch portability correction, 2026-10-24

The first rebased hosted run (40104847352) failed strictly on the interfaces
source checksum. The navigation gate on the same head passed (40104847340).
The cached build above did not exercise a fresh Linux export.

Investigation reproduced the cause: Windows `core.autocrlf=true` changed text
bytes during `git archive`. With the interfaces SHA unchanged, 59 exported
files differed only by CRLF versus LF. Git export now explicitly uses
`core.autocrlf=false` and `core.eol=lf`. The source lock was regenerated by
freshly fetching the same 14 exact SHAs; no version, component or repository
selection changed. Expected checksum checks remain strict.

Regression command:

```sh
python -m unittest discover -s tests -p test_pinned_release.py -k git_line_ending -v
```

Before the fix: 1 test fails because opposite host autocrlf defaults produce
different source hashes. After the fix: that test passes. The complete suite
then passes **28 tests, zero failures**, including all merged navigation tests.

Regenerated the reviewed candidate lock using a new output file:

```sh
python scripts/lock_release_sources.py --manifest manifests/v2.0.0-rc.1.repos --output release-config.rc1.lf.json --cache-dir input/rc1 --version 2.0.0-rc.1
```

Confirmed all config fields except the 14 source checksums are unchanged, then
replaced the old candidate lock. The rebuilt real-source bundle verifies
1,841 files and has SHA-256:

`2c494b1d090a3c525379d32585f483d9c685d606943657c1b64991190c11d227`.

This supersedes the earlier Windows-derived **candidate** bundle checksum;
no published release is changed. Fresh Linux two-fetch reproducibility and
navigation checks are rerun on the final head, with results linked in PR #12.

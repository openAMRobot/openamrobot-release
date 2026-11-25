# v2.0.0-rc.1 preparation and publication runbook

Updated 25 November 2026. Parent release #18 head: bcaef5109260411764aee91ed5eca01d609e4810.
This supersedes the historical Monday runbook. Work only in existing manifest #23
and release #18. No new PR, tag or GitHub Release, including a draft release,
until Alex explicitly authorizes publication. An elapsed calendar target is not authorization.

## 1. Preconditions and final selection

Release builder #12 is already merged at a8f60f6961555244991a9e13437504ed79bdc808.
Do not change repository merge settings or repeat its approval/merge procedure.
Record clean checkout, branch and full parent SHA before each write.

Final platform pin: owner-approved platform main commit including merged licence
PR #180. Final upperbody pin: owner-approved main commit after Mohamed merges
his integration chain and licence PR #121. Both licence PRs were open on 25 Nov.
The requested 18:00 CET upperbody target is a dependency target, not an available SHA.
Verify actual merge commits and branch ancestry; proposal heads or integration
branch tips are not substitutes. Obtain owner approval for every other changed
pin, including firmware code changes. Keep interfaces repinning separately reviewed.
Do not automatically refresh all entries to moving default branch tips.

## 2. Publication audit: mandatory gate

Before authorization, resolve and inspect the selected source bytes for:
- Public prices/content: platform-sw #181, platform-hw #44, UI #65, or explicit
  per-file owner disposition; the compute component price needs its own disposition.
- Apache attribution, NOTICE/licence texts and package licence tags:
  platform-sw #180 and upperbody-sw #121 must be merged and included in selected pins.
- Platform-hw NOTICE consistency with LICENSING.md (documentation CC BY 4.0,
  hardware designs CERN-OHL-P-2.0, scripts MIT): platform lead disposition required.
- Vendor files: Alex selected option B on 25 Nov in release #18 comment 7149787926.
  Implement the exact 32-path exclusion (25 PDFs plus seven other manufacturer
  files), preserve project-written material, record excluded paths in MANIFEST.json,
  and prove all 32 are absent from the final ZIP. The owner decision is recorded;
  implementation and final-byte verification remain pending. Check the existing
  draft #20 implementation for reuse; do not create another PR. Do not describe
  archive exclusions as proof of general redistribution rights.

Use the detailed audit in release #18 comment 7150025052 as the path inventory.
Track non-blocking SPDX coverage, embodied-ai licence/NOTICE, UI library notices
and firmware documentation notices explicitly; do not silently claim they are fixed.

## 3. Single UI message provider and install scope

The selected canonical provider is openamrobot-interfaces/ros2/openamr_ui_msgs.
Remove the UI repository copy only through the reviewed contract/UI change,
including standalone build, CI and documentation dependency updates. Until that
change is merged and pinned, full workspace install remains BLOCKED by duplicate
package names. Do not silently add COLCON_IGNORE or describe interfaces-only
checks as a complete workspace install. Any source-only release limitation needs
explicit owner acceptance and a matching Known limitations entry.

## 4. Coordinated repin and lock

On the existing #23 and #18 branches, record both approved final SHAs and their
merge evidence. Change the same repository URL/type/SHA mapping in
releases/v2.0.0-rc.1.repos (manifest) and manifests/v2.0.0-rc.1.repos (release).
Only governance/.github is excepted from parity. Check upperbody's internal
platform pin against the selected platform SHA and record any owner disposition.

From the release checkout, use a new output and fresh cache:

```sh
python scripts/check_manifest_sync.py manifests/v2.0.0-rc.1.repos <manifest-checkout>/releases/v2.0.0-rc.1.repos
python scripts/lock_release_sources.py --manifest manifests/v2.0.0-rc.1.repos --output release-config.rc1.next.json --cache-dir <fresh-lock-cache> --version 2.0.0-rc.1
```

Review source hashes, manifest hash and packaging exclusions before replacing the
old lock. Preserve/reapply reviewed exact-path exclusion policy if the lock tool
does not retain it. Never edit checksum values just to make verification pass.
Update notes, evidence references and PR bodies for the resulting commits, then
request fresh owner/code-owner reviews; older approvals cover older selections.

## 5. Rehearsal and exact-head checks

The 23 Nov current-pin rehearsal is historical: two fresh builds validated 3,061
files, 400,568,111 bytes, SHA-256
657ed9b3aa59d9c669af53bcf1ff2612d1b068c969af3cd966b9d76ae1f6530c.
It is not the expected hash after repin or exclusions. Selected interfaces install
passed two isolated producer/consumer pairs at 50ed777, actual version 0.0.0 and
contract 2, with 12 unique types, absent-install controls and downstream C++.
Installed tarballs differed; no reproducible compiled binaries are claimed.

Run both repositories' unit/manifest checks on the updated heads. Run two source
builds with separate empty caches and outputs:

```sh
python -m unittest discover -s tests
python scripts/build_release.py --config release-config.rc1.json --input-dir <fresh-first> --output-dir <first-output> --fetch
python scripts/build_release.py --config release-config.rc1.json --input-dir <fresh-second> --output-dir <second-output> --fetch
python scripts/validate_release.py <first-output>/OpenAMRobot-v2.0.0-rc.1-source.zip
python scripts/validate_release.py <second-output>/OpenAMRobot-v2.0.0-rc.1-source.zip
```

Compare complete ZIP bytes and SHA-256, verify both external sidecars, inspect
MANIFEST.json and prove exclusion absence/preserved project files. Repeat clean
install/absent-install/downstream checks using the actual selected archive pins.
Record full-workspace result separately. Retain commands, logs, hashes, JUnit,
image digests, source provenance and limitations as workflow evidence.

After manifest #23 lands on main through its maintainer, rerun #18 CI on the exact
new head. Hosted parity reads manifest main, not the unmerged #23 branch. Require
fresh successful hosted source builds/checksums and current-head reviews. Skipped
jobs are not passing test evidence. Do not bypass parity or other branch protections.

## 6. Authorization and publication handover

Refresh the notes from selected commits and evidence, including simulation-only
scope, hardware limitations and unresolved full-workspace status. Obtain explicit
acceptance/GO and Alex's publication authorization. Until then stop here: no tag,
model tag, draft GitHub Release or publication. Once authorized, the owner records
release date/target SHA, attaches the exact reviewed CI artifact without rebuilding,
verifies downloaded asset checksums, and confirms the tag resolves to the approved
commit. Never move/overwrite a published tag or replace an asset to hide a failure.

# v2.0.0-rc.1 publication runbook (Monday 23 Nov 2026)

Who: the release owner. Nothing here is done by CI or by an agent: merges, the
tag and the publication are owner actions. Commands are for PowerShell with the
GitHub CLI (`gh`) signed in; they also run in bash where noted.

The release is a source pre-release. Its statuses come from
`RELEASE_NOTES.md` in this directory and must stay as they are unless a step
below says otherwise. No status is upgraded because a step passed that does
not measure it.

## 0. Check that nothing moved since the lock

The lock (`release-config.rc1.json`) holds one SHA-256 per source. If a main
branch moved, the lock is still valid (it pins SHAs, not branches), but the
"reviewed main" label in the notes then needs a fresh read. Compare:

```powershell
gh api repos/openAMRobot/openamr-upperbody-sw/commits/main --jq .sha
gh api repos/openAMRobot/openamr-platform-sw/commits/main --jq .sha
```

Expected: upperbody-sw `a3a93c60b0de2865c6ce09499cfad566d7072659`
(or the #74 merge commit, see step 2), platform-sw
`69847ab7c9c6cd49b3022dc1a62f86c044ba10ff`. Any other value: stop and decide
whether rc.1 takes the new commit (then redo the lock as in step 2b).

## 1. Merge the rc.1 builder: openamrobot-release #12

https://github.com/openAMRobot/openamrobot-release/pull/12

Adopted 27 Oct, approved by the software lead on e7a41dd. Use **Create a merge
commit** (not squash): #18 already contains #12's commits, so a merge commit
keeps #18's diff to its own files.

## 2. Model bundle and platform pin: openamr-upperbody-sw #74 (optional for rc.1)

https://github.com/openAMRobot/openamr-upperbody-sw/pull/74

#74 carries the model bundle workflow (now listening for `model-2.0.0-rc.1`
and `model-2.0.0`) and the combined-model platform pin 8e7a454 -> 69847ab.
It can merge only when: the model owner's three additions are done or
deferred in the thread, the software lead writes adopt, A6 and A7 are green on
its head (PLATFORM-PIN needs both), and it is marked ready.

### 2a. #74 not merged by Monday

Publish without it. Keep these rows in the notes exactly as they are:
"Combined model platform pin" (not verified) and "Public model bundle"
(proposed). Skip step 7. The rc.1 lock stays as committed.

### 2b. #74 merged

The upperbody-sw entry must move to the merge commit, in two files:

1. In this repository (on the #18 branch), `manifests/v2.0.0-rc.1.repos`:
   replace `a3a93c60b0de2865c6ce09499cfad566d7072659` under
   `src/openamr-upperbody-sw` with the #74 merge commit SHA. Then regenerate
   the lock (the tool never overwrites, so write a new file and move it):

   ```powershell
   python -m pip install -r requirements-release.txt
   python scripts/lock_release_sources.py --manifest manifests/v2.0.0-rc.1.repos --output release-config.rc1.next.json --cache-dir input/lock --version 2.0.0-rc.1
   Move-Item -Force release-config.rc1.next.json release-config.rc1.json
   ```

   Commit both files (DCO sign-off) to the #18 branch.
2. In the openamrobot-manifest change of step 3, the same SHA in
   `releases/v2.0.0-rc.1.repos`.

## 3. Workspace manifest parity: openamrobot-manifest

The builder's CI compares `manifests/v2.0.0-rc.1.repos` with
`releases/v2.0.0-rc.1.repos` on openamrobot-manifest main and fails on any
difference. That repository still holds the 19 Oct pins, so #18's
`pinned-release` check is red until this step is merged.
`openamrobot-manifest-rc1-pins.patch` in this directory is the change
(rc.1 pins, openamrobot-embodied-ai added to both manifests, two counting
tests 13 -> 14 and 11 -> 12); its 42 tests pass locally.

```powershell
# from the folder that holds your openamrobot-release clone
git clone https://github.com/openAMRobot/openamrobot-manifest.git
cd openamrobot-manifest
git switch -c release/v2.0.0-rc.1-pins
git am ..\openamrobot-release\release-metadata\v2.0.0-rc.1\openamrobot-manifest-rc1-pins.patch
# only for 2b: replace a3a93c60b0de2865c6ce09499cfad566d7072659 in releases/v2.0.0-rc.1.repos, then git commit -a -s --amend --no-edit
git push -u origin release/v2.0.0-rc.1-pins
gh pr create --repo openAMRobot/openamrobot-manifest --fill
```

Merge it when its checks (manifest validation, Jazzy driver sources) are green.

## 4. Merge the notes, pins and lock: openamrobot-release #18

https://github.com/openAMRobot/openamrobot-release/pull/18

1. After steps 1 and 3, re-run the checks of #18 (Checks tab, "Re-run all
   jobs") so `pinned-release` fetches the updated workspace manifest.
2. Required green: `pinned-release` (tests, parity, two fetch builds, `cmp`,
   `sha256sum -c`), DCO, repository-quality.
3. Owner writes adopt in the thread, marks it ready, merges (merge commit).

## 5. Build the archive

On openamrobot-release main, from CI (no local tools needed):

```powershell
gh workflow run pinned-release.yml --repo openAMRobot/openamrobot-release --ref main
gh run list --repo openAMRobot/openamrobot-release --workflow pinned-release.yml --limit 1
gh run watch <run-id> --repo openAMRobot/openamrobot-release
gh run download <run-id> --repo openAMRobot/openamrobot-release --name OpenAMRobot-v2.0.0-rc.1-candidate --dir rc1
```

The run builds twice from independent fetches and fails unless both zips are
byte-identical and match the lock. Write the run ID down for the notes.

Local alternative (Python 3.10+, Git), from a clone of main:

```powershell
python -m pip install -r requirements-release.txt
python scripts/build_release.py --config release-config.rc1.json --input-dir input/first --output-dir dist/first --fetch
python scripts/build_release.py --config release-config.rc1.json --input-dir input/second --output-dir dist/second --fetch
python scripts/validate_release.py dist/first/OpenAMRobot-v2.0.0-rc.1-source.zip
(Get-FileHash dist/first/OpenAMRobot-v2.0.0-rc.1-source.zip).Hash; (Get-FileHash dist/second/OpenAMRobot-v2.0.0-rc.1-source.zip).Hash
```

## 6. Verify the checksum

```powershell
(Get-FileHash rc1\OpenAMRobot-v2.0.0-rc.1-source.zip -Algorithm SHA256).Hash.ToLower()
Get-Content rc1\OpenAMRobot-v2.0.0-rc.1-source.zip.sha256
```

bash: `cd rc1 && sha256sum -c OpenAMRobot-v2.0.0-rc.1-source.zip.sha256`.

Both values must be equal and, for the lock as committed (path 2a), equal to
the trial build of 20 Nov:

```
657ed9b3aa59d9c669af53bcf1ff2612d1b068c969af3cd966b9d76ae1f6530c  OpenAMRobot-v2.0.0-rc.1-source.zip  (400568111 bytes)
```

With path 2b the value is new; the CI run of step 5 is then its reference.
A mismatch stops the release: do not edit a checksum to make it pass.

## 7. Model tag (only with path 2b)

Create the tag on the upperbody-sw #74 merge commit; the Model bundle
workflow builds the bundle and attaches it to a draft release there:

```powershell
gh api repos/openAMRobot/openamr-upperbody-sw/git/refs -f ref=refs/tags/model-2.0.0-rc.1 -f sha=<#74 merge commit SHA>
```

Check the workflow run is green, then publish that draft as a pre-release:
`gh release edit model-2.0.0-rc.1 --repo openAMRobot/openamr-upperbody-sw --draft=false --prerelease --latest=false`.

## 8. Baseline 1 strict acceptance: decide the row

The row "Strict reviewed acceptance run on reviewed integration heads" counts
as passed only for a run of `baseline1-acceptance.yml` on
openamr-upperbody-sw `integration/baseline1` (not a `diag/` or `scratch/`
branch, not titled DIAGNOSTIC), strict sequence, CycloneDDS, conclusion
success, on heads that carry the reviewed fixes.

```powershell
gh run list --repo openAMRobot/openamr-upperbody-sw --workflow baseline1-acceptance.yml --branch integration/baseline1 --limit 5
```

- **Passed**: in the release body (step 9) set that row to
  `demonstrated in simulation (<run ID>)` with the two integration head SHAs,
  add the run to the Baseline 1 table, and replace the "Why the strict
  reviewed acceptance has not been run" list with one line naming the run.
  It stays development evidence: sim-oracle profile, integration branches
  never merged, not physical or safety acceptance. Commit the same change to
  `RELEASE_NOTES.md` on main afterwards.
- **Not passed or not run**: leave the row `not verified` and the reasons list
  as they are.

## 9. Create the draft release

```powershell
gh release create v2.0.0-rc.1 --repo openAMRobot/openamrobot-release --draft --prerelease --target <main SHA after step 4> --title "OpenAMRobot v2.0.0-rc.1" --notes-file release-metadata/v2.0.0-rc.1/RELEASE_NOTES.md rc1/OpenAMRobot-v2.0.0-rc.1-source.zip rc1/OpenAMRobot-v2.0.0-rc.1-source.zip.sha256
```

A draft creates no tag. In the release editor
(https://github.com/openAMRobot/openamrobot-release/releases):

1. Change the first "Status:" paragraph to: "Pre-release, published 2026-11-23.
   Source archive built by pinned-release run <run ID>." Keep every other
   status as written, with the step 8 change only.
2. Add the checksum line of step 6.
3. Download the attached zip once and repeat step 6 on the download.

## 10. Switch to pre-release (publish)

Only when all of these hold: step 6 passed on the downloaded asset, the
status table is final (step 8 applied), "Set as a pre-release" is ticked and
"Set as the latest release" is not.

```powershell
gh release edit v2.0.0-rc.1 --repo openAMRobot/openamrobot-release --draft=false --prerelease --latest=false
```

Publishing creates the tag `v2.0.0-rc.1` on the target commit. Component
navigation tags in other repositories are optional and are aids only; the
archive in this release is the ground truth.

## If something fails

Stop at the failing step. Do not re-lock, re-tag, move a published tag or
change a status to make a step pass. Record the command and the error in #18.

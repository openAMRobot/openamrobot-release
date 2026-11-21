# v2.0.0-rc.1 publication runbook (Monday 23 Nov 2026)

Who: the release owner. Nothing here is done by CI or by an agent: merges, the
tag and the publication are owner actions. Commands are for PowerShell (Windows
PowerShell 5.1 or PowerShell 7) with the GitHub CLI (`gh`) signed in and Git
and Python 3.10+ on the path; a bash form is given where it differs.

The release is a source pre-release. Its statuses come from
`RELEASE_NOTES.md` in this directory and must stay as they are unless a step
below says otherwise. No status is upgraded because a step passed that does
not measure it.

Dry run of 20 Nov 2026, 19:00 to 20:00 UTC: steps 0, 3 (on a scratch clone, not
pushed), 5 (local build, one fetch) and 6 were executed with the commands below;
steps 1, 2, 4 and 7 to 10 change GitHub state and were checked against the
repository settings and rules only.

## Order at a glance

1. Step 0 (pins unchanged), then D4 (release date, section "Register entry
   RELEASE-MILESTONES") decided.
2. Repository setting: allow merge commits (step 1a).
3. #12 approved by a code owner and merged with a merge commit (step 1b).
4. openamrobot-manifest PR from the patch, reviewed and merged (step 3).
5. #18 re-run, approved by the release owner, ready, merged (step 4).
6. Archive built on main, checksum checked (steps 5 and 6).
7. Status table refreshed (step 8), draft release, published (steps 9, 10).

## 0. Check that nothing moved since the lock

The lock (`release-config.rc1.json`) holds one SHA-256 per source. If a main
branch moved, the lock is still valid (it pins SHAs, not branches), but the
"reviewed main" label in the notes then needs a fresh read. From the root of
the openamrobot-release clone, on the #18 branch (`git switch
release/v2.0.0-rc.1-draft-notes` then `git pull`) or on main after step 4:

```powershell
$text = Get-Content manifests/v2.0.0-rc.1.repos -Raw
$rx = "url: https://github.com/(?<repo>\S+?)\.git\s+version: (?<sha>[0-9a-f]{40})"
foreach ($m in [regex]::Matches($text, $rx)) { $repo = $m.Groups["repo"].Value; $pin = $m.Groups["sha"].Value; $ref = "HEAD"; if ($repo -eq "micro-ROS/micro-ROS-Agent") { $ref = "refs/heads/jazzy" }; $head = ((git ls-remote "https://github.com/$repo.git" $ref) -split "\s")[0]; if ($head -eq $pin) { $s = "same" } else { $s = "MOVED to $head" }; "{0,-40} {1} {2}" -f $repo, $pin.Substring(0,12), $s }
```

bash:

```bash
grep -oP 'url: https://github.com/\K\S+(?=\.git)|version: \K[0-9a-f]{40}' manifests/v2.0.0-rc.1.repos | paste - - | while read repo pin; do ref=HEAD; [ "$repo" = micro-ROS/micro-ROS-Agent ] && ref=refs/heads/jazzy; head=$(git ls-remote "https://github.com/$repo.git" "$ref" | cut -f1); [ "$head" = "$pin" ] && s=same || s="MOVED to $head"; printf '%-40s %s %s\n' "$repo" "${pin:0:12}" "$s"; done
```

Expected: 15 lines, each `same` (read 20 Nov 2026, 18:55 UTC). micro-ROS-Agent
is compared with its `jazzy` branch, every other repository with its default
branch. A `MOVED` line for openamr-upperbody-sw that names the #74 merge
commit means path 2b. Any other `MOVED` line: stop and decide whether rc.1
takes the new commit; if it does, the new commit must be reviewed and merged
on its main, then redo the lock as in step 2b for that entry.

## 1. Merge the rc.1 builder: openamrobot-release #12

https://github.com/openAMRobot/openamrobot-release/pull/12

State read 20 Nov: head e7a41dd, open, not draft, checks green (DCO,
license/cla, install, pinned-release, repository-quality), adopted 27 Oct,
approved by the software lead on e7a41dd. GitHub still shows it as blocked for
two reasons:

- the ruleset on main requires a code-owner approval, and the code owners of
  this repository are KARTHIKEYAN124 and BotshareAI; the software lead's
  approval is not a code-owner approval here. #12 is authored by
  KARTHIKEYAN124, so a BotshareAI approval counts.
- the repository allows squash merges only (Settings, General, Pull Requests:
  "Allow merge commits" is off), so "Create a merge commit" is not offered.

Use a merge commit (not squash): #18 already contains #12's commits (merge
b685a93), so a merge commit keeps #18's diff to its own files.

### 1a. Allow merge commits (repository admin, once)

Browser: https://github.com/openAMRobot/openamrobot-release/settings, section
"Pull Requests", tick "Allow merge commits", leave "Allow squash merging" on.
Or:

```powershell
gh api -X PATCH repos/openAMRobot/openamrobot-release -F allow_merge_commit=true --jq "{allow_merge_commit, allow_squash_merge, allow_rebase_merge}"
```

Expected output: `{"allow_merge_commit":true,"allow_rebase_merge":false,"allow_squash_merge":true}`.

### 1b. Approve and merge

```powershell
gh pr review 12 --repo openAMRobot/openamrobot-release --approve --body "Approved as code owner for the rc.1 builder on e7a41dd (software lead approval of 30 Oct on the same head)."
gh pr merge 12 --repo openAMRobot/openamrobot-release --merge --match-head-commit e7a41dd763eec4e3011a082e4ac179bdfb3d7f0c
gh api repos/openAMRobot/openamrobot-release/commits/main --jq "[.sha, .parents[].sha]"
```

Expected: the last command prints a new main SHA with two parents,
c39eda70d8cf2e4f98ae09a51afc3a0750350a11 and
e7a41dd763eec4e3011a082e4ac179bdfb3d7f0c.

## 2. Model bundle and platform pin: openamr-upperbody-sw #74 (optional for rc.1)

https://github.com/openAMRobot/openamr-upperbody-sw/pull/74

#74 carries the model bundle workflow (now listening for `model-2.0.0-rc.1`
and `model-2.0.0`) and the combined-model platform pin 8e7a454 -> 69847ab.
It can merge only when: the model owner's three additions are done or
deferred in the thread, the software lead writes adopt, A6 and A7 are green on
its head (PLATFORM-PIN needs both), and it is marked ready. State read 20 Nov:
head c0c405c, draft, no review.

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
   git add manifests/v2.0.0-rc.1.repos release-config.rc1.json
   git commit -s -m "rc.1: upperbody-sw pin to the #74 merge commit, lock regenerated"
   git push
   ```

2. In the openamrobot-manifest change of step 3, the same SHA in
   `releases/v2.0.0-rc.1.repos`.

The notes rows "Combined model platform pin" and "Public model bundle" then
change as described in step 8.

## 3. Workspace manifest parity: openamrobot-manifest

The builder's CI compares `manifests/v2.0.0-rc.1.repos` with
`releases/v2.0.0-rc.1.repos` on openamrobot-manifest main and fails on any
difference. That repository still holds the 19 Oct pins (main 5b782ac), so
#18's `pinned-release` check is red until this step is merged.
`openamrobot-manifest-rc1-pins.patch` in this directory is the change
(rc.1 pins, openamrobot-embodied-ai added to both manifests, two counting
tests 13 -> 14 and 11 -> 12). Checked 20 Nov 19:10 UTC on manifest main
5b782ac: it applies with `git am`, the 42 validator tests pass, both validators
pass, and the parity check of this repository matches 14 repositories.

Open manifest PR #22 (branch release/rc1-pins-2026-11-10, 10 Nov pins and a
cross-pin checker) changes the same file with older pins. It must not merge
before or after this change for rc.1: its pins are not the rc.1 pins, and its
checker would fail rc.1 while upperbody-sw main pins platform-sw 8e7a454 (the
"Combined model platform pin" row). Its owner closes it as superseded for the
pins or rebases the checker alone after rc.1.

From any working folder (the patch is downloaded at a fixed commit, so the
state of your openamrobot-release clone does not matter):

```powershell
git clone -c core.autocrlf=false https://github.com/openAMRobot/openamrobot-manifest.git
cd openamrobot-manifest
git rev-parse HEAD
git switch -c release/v2.0.0-rc.1-pins
curl.exe -sSL -o rc1-pins.patch https://raw.githubusercontent.com/openAMRobot/openamrobot-release/18bb3c8c8b6670c87598614278b478c53ef8a151/release-metadata/v2.0.0-rc.1/openamrobot-manifest-rc1-pins.patch
(Get-FileHash rc1-pins.patch -Algorithm SHA256).Hash.ToLower()
git am rc1-pins.patch
Remove-Item rc1-pins.patch
git log -1 --format="%an <%ae>%n%(trailers)"
```

Expected: `git rev-parse HEAD` prints
5b782ac25f471d2006cae07bc06da4a88e7dca8e (if not, main moved: run `git am`
anyway; if it fails, stop and report it in #18); the patch hash is
`5ff714130a8b5d27540b3413273d29bd1462d1a4577ae125fb45e9af57c57ab9`; the log
shows the author `Alex Reznichenko <info@botshare.ai>` and the trailer
`Signed-off-by: Alex Reznichenko <info@botshare.ai>` (DCO). bash: replace
`curl.exe` with `curl`, the hash line with `sha256sum rc1-pins.patch` and
`Remove-Item` with `rm`.

Only for path 2b: replace a3a93c60b0de2865c6ce09499cfad566d7072659 in
`releases/v2.0.0-rc.1.repos` with the #74 merge commit SHA, then
`git commit -a -s --amend --no-edit`.

Optional local test before pushing (about 1 minute):

```powershell
python -m pip install yamllint==1.38.0 vcstool==0.3.0 PyYAML==6.0.2 setuptools==79.0.1
python -m unittest discover -s tests
python tools/check_manifest.py --offline releases/v2.0.0-rc.1.repos
python tools/check_release_manifest.py releases/v2.0.0-rc.1.repos --development openamrobot.repos
```

Expected: `Ran 42 tests ... OK`, `PASS development coverage and sources`,
`PASS immutable refs: 14 repositories`.

Push and open the PR. The body file `openamrobot-manifest-pr-body.md` is in
this directory; the commands download it from the #18 branch and write the
pushed commit SHA into its Evidence section (the evidence rules compare it with
the PR head). bash: `sed -i "s/PUSHED_HEAD_SHA/$(git rev-parse HEAD)/" pr-body.md`
in place of the two lines that build `$body`.

```powershell
git push -u origin release/v2.0.0-rc.1-pins
curl.exe -sSL -o pr-body.md https://raw.githubusercontent.com/openAMRobot/openamrobot-release/release/v2.0.0-rc.1-draft-notes/release-metadata/v2.0.0-rc.1/openamrobot-manifest-pr-body.md
$body = (Get-Content pr-body.md -Raw).Replace("PUSHED_HEAD_SHA", (git rev-parse HEAD))
[IO.File]::WriteAllText((Join-Path $PWD "pr-body.md"), $body, (New-Object Text.UTF8Encoding $false))
Select-String "Head SHA" pr-body.md
gh pr create --repo openAMRobot/openamrobot-manifest --base main --head release/v2.0.0-rc.1-pins --title "releases: v2.0.0-rc.1 pins to the reviewed main of each repository" --body-file pr-body.md --reviewer KARTHIKEYAN124,panthera-momagdii
Remove-Item pr-body.md
```

Review: the code owners of openamrobot-manifest are KARTHIKEYAN124 (release
owner) and panthera-momagdii (software lead). BotshareAI is the author, so its
approval does not count; one of the two approves. Merge it when its checks
(manifest validation, Jazzy driver sources, repository-quality, DCO) are green,
with any merge method the repository offers (the parity check compares file
content, not commits). Then confirm:

```powershell
gh api "repos/openAMRobot/openamrobot-manifest/contents/releases/v2.0.0-rc.1.repos?ref=main" -H "Accept: application/vnd.github.raw" | Select-String "version:"
```

Expected: the 14 SHAs of `manifests/v2.0.0-rc.1.repos` in this repository
(governance/.github is not in the workspace manifest).

## 4. Merge the notes, pins and lock: openamrobot-release #18

https://github.com/openAMRobot/openamrobot-release/pull/18

1. After steps 1 and 3, re-run the `pinned-release` workflow on the head of
   #18 so it fetches the updated workspace manifest:

   ```powershell
   $run = gh run list --repo openAMRobot/openamrobot-release --workflow pinned-release.yml --branch release/v2.0.0-rc.1-draft-notes --limit 1 --json databaseId --jq ".[0].databaseId"
   gh run rerun $run --repo openAMRobot/openamrobot-release
   gh run watch $run --repo openAMRobot/openamrobot-release
   ```

   (Browser: the Checks tab of #18, "Re-run all jobs".) A push to the #18
   branch after step 1 starts a fresh run as well; then use that run.
2. Required green: `pinned-release` (35 tests, parity, two fetch builds,
   `cmp`, `sha256sum -c`), DCO, license/cla, repository-quality. Write the
   run ID down.
3. #18 is authored by BotshareAI, so its approval does not count: the release
   owner KARTHIKEYAN124 (the only other code owner) reviews and approves.
4. The owner writes adopt in the thread, marks it ready, merges with a merge
   commit:

   ```powershell
   gh pr ready 18 --repo openAMRobot/openamrobot-release
   gh pr merge 18 --repo openAMRobot/openamrobot-release --merge
   gh api repos/openAMRobot/openamrobot-release/commits/main --jq .sha
   ```

   The last line is the main SHA used in steps 5 and 9.

## 5. Build the archive

On openamrobot-release main, from CI (no local tools needed). The workflow
file reaches main with #12 (step 1):

```powershell
gh workflow run pinned-release.yml --repo openAMRobot/openamrobot-release --ref main
Start-Sleep -Seconds 10
$run = gh run list --repo openAMRobot/openamrobot-release --workflow pinned-release.yml --branch main --event workflow_dispatch --limit 1 --json databaseId --jq ".[0].databaseId"
$run
gh run watch $run --repo openAMRobot/openamrobot-release --exit-status
gh run download $run --repo openAMRobot/openamrobot-release --name OpenAMRobot-v2.0.0-rc.1-candidate --dir rc1
```

The run builds twice from independent fetches and fails unless both zips are
byte-identical and match the lock. Write the run ID down for the notes.
`rc1` then holds `OpenAMRobot-v2.0.0-rc.1-source.zip` and
`OpenAMRobot-v2.0.0-rc.1-source.zip.sha256`.

Local alternative (Python 3.10+, Git, about 1 minute and 1.6 GB of disk per
build), from a clone of main:

```powershell
python -m pip install -r requirements-release.txt
python scripts/build_release.py --config release-config.rc1.json --input-dir input/first --output-dir dist/first --fetch
python scripts/build_release.py --config release-config.rc1.json --input-dir input/second --output-dir dist/second --fetch
python scripts/validate_release.py dist/first/OpenAMRobot-v2.0.0-rc.1-source.zip
(Get-FileHash dist/first/OpenAMRobot-v2.0.0-rc.1-source.zip).Hash -eq (Get-FileHash dist/second/OpenAMRobot-v2.0.0-rc.1-source.zip).Hash
```

Expected: each build prints the zip path with the hash of step 6,
`PASS: 3061 files verified`, then `True`. A local build is a check, not the
published artifact; publish the CI artifact.

## 6. Verify the checksum

```powershell
$h = (Get-FileHash rc1\OpenAMRobot-v2.0.0-rc.1-source.zip -Algorithm SHA256).Hash.ToLower()
$e = (Get-Content rc1\OpenAMRobot-v2.0.0-rc.1-source.zip.sha256).Split(" ")[0]
"computed $h"; "recorded $e"; "size $((Get-Item rc1\OpenAMRobot-v2.0.0-rc.1-source.zip).Length)"
($h -eq $e) -and ($h -eq "657ed9b3aa59d9c669af53bcf1ff2612d1b068c969af3cd966b9d76ae1f6530c")
```

bash: `cd rc1 && sha256sum -c OpenAMRobot-v2.0.0-rc.1-source.zip.sha256 && sha256sum OpenAMRobot-v2.0.0-rc.1-source.zip`.

For the lock as committed (path 2a) the last PowerShell line prints `True`
(bash: `OK`, then the hash below), and the size is 400568111 bytes, equal to the
trial builds of 20 Nov:

```
657ed9b3aa59d9c669af53bcf1ff2612d1b068c969af3cd966b9d76ae1f6530c  OpenAMRobot-v2.0.0-rc.1-source.zip  (400568111 bytes)
```

With path 2b the value is new: compare only `$h -eq $e`, and the CI run of
step 5 is then its reference. A mismatch stops the release: do not edit a
checksum to make it pass.

## 7. Model tag (only with path 2b)

Create the tag on the upperbody-sw #74 merge commit; the Model bundle
workflow builds the bundle and attaches it to a draft release there:

```powershell
gh api repos/openAMRobot/openamr-upperbody-sw/git/refs -f ref=refs/tags/model-2.0.0-rc.1 -f sha=<#74 merge commit SHA>
```

Check the workflow run is green, then publish that draft as a pre-release:
`gh release edit model-2.0.0-rc.1 --repo openAMRobot/openamr-upperbody-sw --draft=false --prerelease --latest=false`.

## 8. Monday morning: refresh the status table

The notes on main are the 20 Nov text plus anything merged into #18 since.
Before step 9, update `RELEASE_NOTES.md` for what changed over the weekend,
on a branch from main, as one reviewed PR (or as the last commit on #18 before
step 4). Change only rows whose evidence changed; every changed row names its
PR, approval or run ID with the SHA.

1. Read the state of every PR named in the tables:

   ```powershell
   foreach ($p in "openamr-platform-sw/90","openamr-platform-sw/91","openamr-platform-sw/92","openamr-platform-sw/164","openamr-platform-sw/167","openamr-platform-sw/169","openamr-platform-sw/170","openamr-platform-sw/175","openamr-upperbody-sw/74","openamr-upperbody-sw/84","openamr-upperbody-sw/86","openamr-upperbody-sw/94","openamr-upperbody-sw/95","openamr-upperbody-sw/98","openamr-upperbody-sw/99","openamr-upperbody-sw/168","openamr-platform-hw/43","openamr-platform-fw/22","openamr-platform-fw/63","openamrobot-interfaces/39","openamrobot-interfaces/42","openamrobot-ui/56","openamrobot-embodied-ai/8") { $r, $n = $p.Split("/"); $pr = gh api "repos/openAMRobot/$r/pulls/$n" --jq "[.number, .state, .draft, .head.sha[0:7], .merged_at] | @tsv"; $rv = (gh api "repos/openAMRobot/$r/pulls/$n/reviews" --jq ".[] | [.user.login, .state, .commit_id[0:7]] | @tsv") -join "; "; "$r`t$pr`t$rv" }
   ```

   Each line: repository, number, state, draft, head, merge time, then every
   review with its commit. Row rules: merged into main and every check on the merge commit green:
   the row moves to "merged and CI green" only if that commit is one of the
   rc.1 pins; a merge after the lock is not in rc.1 and the row says
   "merged after rc.1 (SHA), not in this release". Approved but not merged:
   still "proposed (draft PR)", with "approved by <role> at <SHA>" in the
   evidence. Nothing else changes a status.
2. Pins: re-run step 0. Pins do not move over the weekend unless the owner
   decides it (step 2b is the only planned case).
3. Integration snapshot: read the two integration heads and put them in
   `integration-snapshot.repos` and the "Integration snapshot" paragraph:

   ```powershell
   git ls-remote https://github.com/openAMRobot/openamr-platform-sw.git refs/heads/integration/baseline1
   git ls-remote https://github.com/openAMRobot/openamr-upperbody-sw.git refs/heads/integration/baseline1
   ```

   With a qualifying strict run (item 4), the snapshot records the pins that
   run declares, not the branch heads.
4. Baseline 1 strict acceptance. The row "Strict reviewed acceptance run on
   reviewed integration heads" stays `not verified` unless a run meets every
   condition below:

   ```powershell
   gh run list --repo openAMRobot/openamr-upperbody-sw --workflow baseline1-acceptance.yml --branch integration/baseline1 --event workflow_dispatch --limit 10 --json databaseId,headSha,conclusion,displayTitle,createdAt
   gh run view <run-id> --repo openAMRobot/openamr-upperbody-sw --json jobs --jq ".jobs[] | [.name, .conclusion] | @tsv"
   gh run download <run-id> --repo openAMRobot/openamr-upperbody-sw --name baseline1-strict-verdict-attempt1 --dir verdict
   (Get-Content verdict\verdict.json -Raw | ConvertFrom-Json) | Select-Object verdict, expect, problems, pins | Format-List
   ```

   - branch `integration/baseline1` of openamr-upperbody-sw (not `diag/`,
     not `scratch/`), event `workflow_dispatch`, title not starting with
     DIAGNOSTIC;
   - jobs "Baseline 1 whole-robot mission, leg 1", "... leg 2" and "Strict
     Baseline 1 verdict" all `success`; runs without the verdict job (before
     20 Nov, for example 44309817813) never qualify;
   - `verdict.json`: `verdict` PASS, `expect` 2, `problems` empty; the pins in
     it are the integration heads that carry the reviewed fixes (each fix
     approved by its code owner on the commit the pins contain);
   - the number of such dispatches meets decision D1 (one dispatch with two
     legs, or two dispatches back to back, as Alex decides); if D1 is not
     decided, the row stays `not verified`;
   - with a later attempt the artifact name ends in that attempt number.

   **Passed**: set the row to `demonstrated in simulation (<run ID>)` with
   the two integration head SHAs, add the run to the Baseline 1 table, and
   replace the "Why the strict reviewed acceptance has not been run" list with
   one line naming the run. It stays development evidence: sim-oracle
   profile, integration branches never merged, not physical or safety
   acceptance.
   **Not passed or not run**: leave the row `not verified` and update the
   reasons list only where a reason no longer holds.
5. Publication text (only at step 9): the first "Status:" paragraph, the
   title line "(DRAFT)", the version table date (per D4), and the limitation
   "The rc.1 builder (PR #12) is not merged ..." are replaced as listed in
   step 9.

## 9. Create the draft release

From the clone, on main after step 4 and the refresh of step 8
(`git switch main` then `git pull`):

```powershell
$main = gh api repos/openAMRobot/openamrobot-release/commits/main --jq .sha
gh release create v2.0.0-rc.1 --repo openAMRobot/openamrobot-release --draft --prerelease --target $main --title "OpenAMRobot v2.0.0-rc.1" --notes-file release-metadata/v2.0.0-rc.1/RELEASE_NOTES.md rc1/OpenAMRobot-v2.0.0-rc.1-source.zip rc1/OpenAMRobot-v2.0.0-rc.1-source.zip.sha256
```

A draft creates no tag. In the release editor
(https://github.com/openAMRobot/openamrobot-release/releases):

1. Title line: remove "(DRAFT)".
2. Replace the first "Status:" paragraph with: "Pre-release, published
   2026-11-23. Source archive built by pinned-release run <run ID> on
   openamrobot-release <main SHA>. This repository holds the release archive
   and is the ground truth; version tags in component repositories are
   navigation aids only."
3. Version table, first row: the date decided under D4 (section "Register
   entry RELEASE-MILESTONES").
4. Known limitations: delete the line "The rc.1 builder (PR #12) is not
   merged ..." (true no longer).
5. Add the checksum line of step 6 under "Source pins and lock", with the run
   ID.
6. Keep every other status as written, with the step 8 changes only.
7. Download the attached zip once and repeat step 6 on the download:

   ```powershell
   gh release download v2.0.0-rc.1 --repo openAMRobot/openamrobot-release --dir rc1-check
   ```

   (or download both files from the draft page in the browser into
   `rc1-check`), then run step 6 with `rc1-check` in place of `rc1`.

## 10. Switch to pre-release (publish)

Only when all of these hold: step 6 passed on the downloaded asset, the
status table is final (step 8 applied), "Set as a pre-release" is ticked and
"Set as the latest release" is not.

```powershell
gh release edit v2.0.0-rc.1 --repo openAMRobot/openamrobot-release --draft=false --prerelease --latest=false
gh api repos/openAMRobot/openamrobot-release/git/ref/tags/v2.0.0-rc.1 --jq .object.sha
```

Publishing creates the tag `v2.0.0-rc.1` on the target commit; the second
command prints it and must equal `$main`. Component navigation tags in other
repositories are optional and are aids only; the archive in this release is
the ground truth. Afterwards, commit the published text of the notes to
`RELEASE_NOTES.md` on main through a PR, so the file and the release body
match.

## Register entry RELEASE-MILESTONES (decision D4)

The register (openAMRobot/.github decisions.yaml at 87c8486) records
"v2.0.0-rc.1 on 20 November 2026". Publication is 23 Nov. The register's
text checks do not flag an rc.1 date, so no check turns red either way; the
rule is that no file states a value contradicting the register. The owner
(platform-lead) picks one option before step 9:

- Option A: change the register to 23 Nov through a contract change request
  and one reviewed PR in openAMRobot/.github; the notes then say 2026-11-23
  plainly.
- Option B: keep the register at 20 Nov and publish with the date
  2026-11-23 and a `decision-allow: RELEASE-MILESTONES` note on the same line.

## If something fails

Stop at the failing step. Do not re-lock, re-tag, move a published tag or
change a status to make a step pass. Record the command and the error in #18.

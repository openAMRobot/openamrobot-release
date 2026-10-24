# Build the rc.1 candidate

`release-config.rc1.json` locks a release-local snapshot in
`manifests/v2.0.0-rc.1.repos`. Every repository uses a full commit SHA.
The snapshot includes the 13 workspace repositories and a separately pinned
`governance/.github` export, preserving the legacy release's governance input.
The configuration locks both the manifest bytes and each source archive with
SHA-256. The candidate is dated 2026-10-19; final component acceptance is pending.

## Build and verify

Requires Python 3.10 or newer, Git and network access to the pinned repositories:

```sh
python -m pip install -r requirements-release.txt
python -m unittest discover -s tests -v
python scripts/build_release.py --config release-config.rc1.json --input-dir input/first --output-dir dist/first --fetch
python scripts/build_release.py --config release-config.rc1.json --input-dir input/second --output-dir dist/second --fetch
python scripts/validate_release.py dist/first/OpenAMRobot-v2.0.0-rc.1-source.zip
python scripts/validate_release.py dist/second/OpenAMRobot-v2.0.0-rc.1-source.zip
cmp dist/first/OpenAMRobot-v2.0.0-rc.1-source.zip dist/second/OpenAMRobot-v2.0.0-rc.1-source.zip
(cd dist/first && sha256sum -c OpenAMRobot-v2.0.0-rc.1-source.zip.sha256)
```

On PowerShell, compare the two files using `Get-FileHash` instead of `cmp`.
`--fetch` uses `git fetch --depth=1 URL FULL_SHA`, verifies the fetched commit,
and exports it using `git archive`. No moving branch or main archive is used.
Omit `--fetch` to rebuild offline from the already verified source cache.
Missing cache entries or any checksum mismatch fail the build.

Source ZIPs are normalized before hashing: fixed date, sorted files, stored
compression, normalized executable/link modes and the exact commit as ZIP
comment. Git export explicitly sets `core.autocrlf=false` and `core.eol=lf`
so host line-ending defaults cannot change source bytes; repository attributes
still apply. The final ZIP uses the same fixed metadata, retains symlinks as links,
and contains no wall-clock build timestamp or machine-specific paths.
Submodules fail explicitly until represented by separate pinned entries.

## Outputs

- `OpenAMRobot-v2.0.0-rc.1-source.zip` and its external `.sha256` file.
- Inside the ZIP: checkout paths from the release manifest, `release.repos`,
  `MANIFEST.json` with repository URLs, SHAs and source hashes, and
  `checksums.sha256` covering every other file.

The rc.1 layout follows workspace paths rather than the numbered v0.0.1 layout.
The legacy configuration and its metadata retain their original behavior.
Validation checks every inventory entry and rejects extra or duplicate members
without extracting source symlinks. Checksums detect corruption; they are not
a cryptographic signature or proof of release approval.

## Refresh a candidate intentionally

Review the component SHAs first, then create a new manifest and a new lock:

```sh
python scripts/lock_release_sources.py --manifest manifests/next-candidate.repos --output release-config.next.json --cache-dir input/next --version 2.0.0-rc.1
```

Review both files in the same PR. The lock command refuses to overwrite an
existing configuration. Updating a checksum is an explicit source-selection
change, never an automatic fallback after a build failure.

## Dependencies and limitations

The tooling adds PyYAML 6.0.3 (MIT), from https://github.com/yaml/pyyaml.
The source snapshot includes upstream SLAMTEC sllidar_ros2 (package declares
BSD; see its retained upstream licence) and micro-ROS-Agent (Apache-2.0 with
upstream third-party notices). All original repository files and notices are
preserved by Git export; no upstream source is vendored into this builder repo.

This validates source packaging only. Ubuntu/Jazzy package builds, driver
operation, hardware tests, compiled binary reproducibility and upstream
build-time dependency downloads are outside OA-05 verification. Final rc.1
selection still depends on the other audit findings. No release is published
by the pull-request workflow; it uploads a candidate artifact for review.

# Release issue #5: local pinned-install evidence

Validated **6 October 2026** on a Windows host using fresh Linux amd64
containers, Ubuntu 24.04 and ROS 2 Jazzy. Final result: **PASS**, twice.

| Identifier | Recorded value |
|---|---|
| Interfaces source commit | `fa7c438e33bd807c174fa0747119d7d627faa3bf` |
| Package | `openamr_nav_msgs` |
| Package version | `0.0.0` |
| Runtime contract version | `1` |
| Base image | `ros@sha256:c3706ef0a0aa45413c07803cf433602f543b22e45b4855f6fca955c2d8ecc4e8` |
| Source archive SHA-256 | `692f105fd5415ea2203e95ab31f954412a0ba1451249e31136b94d7c3f22bb73` |

## Results

Both ordinary source builds produced install tarballs. Each was consumed by
a separate fresh container receiving **only the install tarball and test
fixtures**. No interfaces source or producer build tree was available to it.
All 11 generated messages passed lookup, import and native serialization.
Both C++ consumers configured, built, linked and ran. Both absent-install
negative controls failed as expected with `openamr_nav_msgs` unavailable.

The **159** generated header/IDL hashes, expanded message definitions, and
resolved producer and consumer dependency inventories matched between runs.
Install tarballs have independent recorded digests; compiled binary or tarball
byte reproducibility is not claimed.

Eight release-builder regression tests pass. A separate integration fixture
using the **actual validated source archive** also passed and emitted the
[pinned component entry](navigation-manifest-component.json). That fixture is
not a complete product build; [its command/output](navigation-manifest-integration.log)
is recorded separately.

## Exact commands

From `openamrobot-release`, on this Windows host:

```powershell
python scripts/validate_navigation_install.py --evidence evidence/navigation-install-20261006-final
python -m unittest discover -s tests -v
python -m compileall -q scripts tests
& 'C:\Program Files\Git\bin\bash.exe' -n scripts/nav-install/producer.sh
& 'C:\Program Files\Git\bin\bash.exe' -n scripts/nav-install/consumer.sh
git diff --check
```

The workflow YAML was parsed with PyYAML. No hosted Actions run is claimed.
The validation runner's exact Docker arguments and shell-source snapshot are
included in the evidence below. An earlier run in
`evidence/navigation-install-20261006` also passed, but mounted the producer
artifact directory read-only. The final run tightened this to the install
tarball alone and saved the verifier sources. Final evidence is authoritative
for this change; the earlier run is retained locally.

## Reviewable files

- [Machine-readable result](../evidence/navigation-install-20261006-final/result.json)
- [Manifest snapshot](../evidence/navigation-install-20261006-final/manifest.json)
- [Docker command arguments](../evidence/navigation-install-20261006-final/commands.json)
- [Evidence checksums](../evidence/navigation-install-20261006-final/checksums.sha256)
- [First producer log](../evidence/navigation-install-20261006-final/first/producer/validation.log)
- [First consumer log](../evidence/navigation-install-20261006-final/first/consumer/validation.log)
- [Second producer log](../evidence/navigation-install-20261006-final/second/producer/validation.log)
- [Second consumer log](../evidence/navigation-install-20261006-final/second/consumer/validation.log)
- [Generated file inventory](../evidence/navigation-install-20261006-final/first/consumer/generated.sha256)
- [Expanded message definitions](../evidence/navigation-install-20261006-final/first/consumer/interfaces.txt)
- [Resolved consumer dependencies](../evidence/navigation-install-20261006-final/first/consumer/dependencies.txt)
- [Install and troubleshooting instructions](navigation-install.md)

Full colcon logs, both install tarballs, source ZIPs, and all other raw files
are retained locally in the final evidence directory and bundled in
[the complete evidence ZIP](evidence/release-issue5-evidence-20261006.zip) with its
[SHA-256 checksum](evidence/release-issue5-evidence-20261006.zip.sha256). Compact
results and logs are prepared for source review; the workflow uploads the
complete evidence directory on hosted execution.

## Scope and remaining review

This proves the pinned navigation **source install** and installed-package
consumption. It does not publish a binary package or certify whole-product
readiness, semantic interoperability, or hardware safety. The candidate
release configuration still needs other component pins and current product
metadata before a full product build. The historical v0.0.1 configuration and
earlier evidence are preserved.

The navigation CI workflow is prepared but has not been pushed or run on
GitHub. Reviewer acceptance and issue closure remain pending; no GitHub
comment, merge, tag or release was performed.

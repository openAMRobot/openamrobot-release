# Proposed update for release issue #5

Release-level pinned-install validation is complete locally for
`openamrobot-interfaces@fa7c438e33bd807c174fa0747119d7d627faa3bf`,
`openamr_nav_msgs` package `0.0.0`, runtime contract `1`.

Two clean producer/consumer pairs passed on digest-pinned Ubuntu 24.04 /
ROS 2 Jazzy. Each downstream container received only the ordinary install
tarball and test fixtures, with no producer source/build tree or developer
overlay. All 11 generated messages loaded and serialized successfully;
the independent C++ consumer built and ran. The absent-install negative
control failed as expected. The 159 generated header/IDL hashes and resolved
dependency inventories matched between runs.

The release-owned installation manifest records the exact pin and versions.
A candidate builder configuration carries them into `MANIFEST.json` together
with install-artifact digests and verification evidence. Builder tests reject
failing evidence and pin/archive/package/contract mismatches; all eight tests
pass. A separate integration check used the actual validated source archive.

Installation and troubleshooting instructions, exact Docker arguments,
verification-source snapshots, both full logs, dependency inventories, and
checksums are prepared in the evidence bundle. See
[the evidence index](navigation-install-evidence.md) and
[installation instructions](navigation-install.md).

This is source-install evidence, not a published binary or complete product
release. Hosted CI and reviewer acceptance remain pending. Please review
the prepared changes and evidence before closing issue #5.

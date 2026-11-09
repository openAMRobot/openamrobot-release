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

Separate interfaces-repin preparation (2026-11-01): the source-free navigation
consumer now takes an explicit package version and contract from its manifest.
A test-only fixture checks interfaces PR #28 head 1194346 with contract 2 and
its existing 0.0.0 package version; it is not an approved release selection.
Contract-1 regression validation remains active. Release pins/checksums stay
unchanged. Repinning waits for author DCO correction, approved package versions,
consumer acceptance and an accepted source commit. Platform-sw #73 still has
requested changes. Local Docker is unavailable; hosted checks supply builds.

2026-11-04: refresh only the unmerged test fixture to interfaces #28 head
119434654f910ba9932f4f6663423952aee5f821. Its package versions remain
0.0.0; DCO still needs author action and no release-version approval is
recorded. Upperbody #14 merged at 41ff4ea; full Gate A acceptance remains
required before the separate four-component pin refresh.

2026-11-09: test-only fixture targets fbb7b3f and explicitly checks the
additional MapIdentity generated type (13 navigation messages total). This
checks installation/serialization, not acceptance of proposed contract #34.
The stale compatibility snapshot fix is offered to the author in
skunal3318/openamrobot-interfaces#1; DCO/version/consumer decisions remain open.

2026-11-09 P2 review fix: preflight and installed verifier share one unique
message inventory. Extras cannot repeat baseline names or contract-2
SiteConfigStatus. Consumer evidence lists verified names; counts come from
that checked list. Negative overlap controls and positive MapIdentity control
pass; 44 local tests pass. Draft and release/contract acceptance gates remain.

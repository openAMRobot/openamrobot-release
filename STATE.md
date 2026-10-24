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

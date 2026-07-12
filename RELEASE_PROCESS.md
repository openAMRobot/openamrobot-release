# OpenAMRobot Release Process

This repository builds a product-level OpenAMRobot release from the project's distributed repositories.

## Directory Structure

```text
openamrobot-release/
├── input/                 # Component ZIP archives; ignored by Git
├── dist/                  # Generated release assets; ignored by Git
├── release-metadata/      # Product-level README and release documents
├── scripts/
│   ├── build_release.py
│   └── validate_release.py
├── release-config.json
└── RELEASE_PROCESS.md
```

## 1. Prepare Component Archives

Download the required repository archives into:

```text
input/
```

The archive filenames must match the values in `release-config.json`.

## 2. Update Release Metadata

Review and update:

```text
release-metadata/README.md
release-metadata/RELEASE_NOTES.md
release-metadata/KNOWN_LIMITATIONS.md
release-metadata/RELEASE_SCOPE.md
```

Update the product version and component information in:

```text
release-config.json
```

## 3. Build the Release

From the repository root, run:

```bash
rm -rf dist/*

python3 scripts/build_release.py \
  --config release-config.json \
  --input-dir input \
  --output-dir dist
```

## 4. Validate the Release

```bash
python3 scripts/validate_release.py \
  dist/OpenAMRobot-v0.0.1-source.zip
```

Replace the filename with the current version.

## 5. Verify the External Checksum

```bash
cd dist
sha256sum -c OpenAMRobot-v0.0.1-source.zip.sha256
cd ..
```

## 6. Inspect the Generated Assets

```bash
ls -lh dist
cat dist/build-report.md
```

Expected outputs include:

```text
OpenAMRobot-vX.Y.Z-source.zip
OpenAMRobot-vX.Y.Z-source.zip.sha256
OpenAMRobot-vX.Y.Z-inventory.csv
build-report.md
```

## 7. Publish

Create a Git tag and GitHub Release using the same version.

Upload the generated files from `dist/` as custom release assets.

GitHub's automatic `Source code` archives contain only this builder repository and are not the complete OpenAMRobot product release.

## Important

The `input/` and `dist/` directories are intentionally excluded from Git. Component archives are temporary build inputs, while generated packages belong in GitHub Release assets.

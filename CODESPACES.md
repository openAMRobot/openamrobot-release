# Codespaces instructions

## 1. Create the release repository

Create `openAMRobot/openamrobot-release`, upload the contents of this builder package, commit, and open the repository in Codespaces.

## 2. Add source archives

In the Codespaces terminal:

```bash
mkdir -p input dist
```

Upload these files into `input/`:

```text
openamr-platform-hw-main.zip
openamr-platform-sw-main(2).zip
openamr-platform-fw-main.zip
openamrobot-ui-main.zip
openamrobot-interfaces-main.zip
openamrobot-comm-main.zip
openamrobot-docs-main.zip
github-main.zip
```

For the final public build, replace branch archives with archives downloaded from the exact `v0.0.1` tags and update their names in `release-config.json`.

## 3. Build

```bash
python3 scripts/build_release.py   --config release-config.json   --input-dir input   --output-dir dist
```

## 4. Validate

```bash
python3 scripts/validate_release.py   dist/OpenAMRobot-v0.0.1-source.zip
```

## 5. Inspect

```bash
cat dist/build-report.md
cat dist/OpenAMRobot-v0.0.1-source.zip.sha256
unzip -l dist/OpenAMRobot-v0.0.1-source.zip | less
```

## 6. Publish

Create a GitHub Release in the product-level release repository:

- Tag: `v0.0.1`
- Title: `OpenAMRobot v0.0.1 — First Public Platform Release`
- Upload:
  - `OpenAMRobot-v0.0.1-source.zip`
  - `OpenAMRobot-v0.0.1-source.zip.sha256`
  - `OpenAMRobot-v0.0.1-inventory.csv`
  - `build-report.md`

Do not use GitHub's automatic source archive as the main product package.

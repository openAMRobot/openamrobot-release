# OpenAMRobot Release Builder

This repository builds a single, frozen, self-contained product package from the distributed OpenAMRobot repositories.

The generated source archive contains the actual files from every component repository—not Git submodule pointers—and remains usable if the live repositories change later.

## Output

```text
OpenAMRobot-v0.0.1-source.zip
OpenAMRobot-v0.0.1-source.zip.sha256
OpenAMRobot-v0.0.1-inventory.csv
```

## Use in GitHub Codespaces

1. Create a new repository, for example `openamrobot-release`.
2. Copy this release-builder repository into it and open it in Codespaces.
3. Upload the component ZIP archives into `input/`.
4. Run:

```bash
python3 scripts/build_release.py \
  --config release-config.json \
  --input-dir input \
  --output-dir dist
```

5. Validate the generated package:

```bash
python3 scripts/validate_release.py dist/OpenAMRobot-v0.0.1-source.zip
```

6. Inspect `dist/build-report.md`. Do not publish until all required checks pass.

## Important scope statement

This builder creates a complete **OpenAMRobot project-source package** containing hardware, software, firmware, UI, interfaces, communication, documentation, and governance files.

It does **not yet create a fully offline operating-system dependency bundle**. ROS, Ubuntu, Docker base images, Python packages, Node packages, and toolchains may still require internet access unless separately cached and added. Do not describe v0.0.1 as “fully offline installable” until it has passed a clean-machine, network-disconnected validation.

## Release workflow

- Freeze and tag each component repository.
- Download each tagged repository archive.
- Update `release-config.json` with the correct archive names and source revisions.
- Build and validate the package.
- Test assembly, flashing, simulation, navigation, docking, and UI using only the package.
- Upload the generated ZIP and checksum to one product-level GitHub Release.

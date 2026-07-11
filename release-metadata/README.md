# OpenAMRobot v0.0.1

**Using a robot should not require a robotics team.**

OpenAMRobot is an open-source platform designed so that the person who understands a task can ultimately teach a robot by demonstration rather than traditional robot programming.

The long-term workflow is **Show → Correct → Judge**: demonstrate a task, intervene when needed, and evaluate the result. The platform translates this domain knowledge into imitation learning, reward modelling, simulation, and reinforcement learning.

## This release

v0.0.1 is the first public, product-level source package for the autonomous mobile robot platform. It freezes the hardware, ROS 2 software, embedded firmware, web UI, interfaces, communication definitions, project documentation, and governance files into one archive.

## Start here

1. Read `RELEASE_NOTES.md` and `KNOWN_LIMITATIONS.md`.
2. Review `01_Getting_Started/RELEASE_SCOPE.md`.
3. Open the component README files:
   - `02_Hardware/README.md`
   - `03_Software/README.md`
   - `04_Firmware/README.md`
   - `05_User_Interface/README.md`
4. Follow the assembly, flashing, bring-up, and operation procedures included in the component documentation.
5. Check `MANIFEST.json` and `checksums.sha256` to verify package contents and provenance.

## Supported uses

- Autonomous mobile robot research and prototyping
- ROS 2 navigation, mapping, and docking development
- Hardware, firmware, and UI education
- No-code robot programming experiments
- Early business-use-case validation
- Foundation-model and embodied-AI research groundwork

## Licensing and safety

The platform is open source, but individual components can contain their own notices and third-party terms. Review all `LICENSE`, `NOTICE`, and third-party files before redistribution.

This is an early hobby/research-grade release. It is not certified for safety-critical, industrial, medical, or unsupervised public operation.

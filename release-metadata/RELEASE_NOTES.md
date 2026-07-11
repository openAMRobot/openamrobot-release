# OpenAMRobot v0.0.1 — Release Notes

## First public product release

This release provides one frozen package containing the distributed OpenAMRobot hardware, software, firmware, UI, interfaces, communication, documentation, and governance sources.

### Hardware

- Differential-drive mobile platform
- Laser-cut and bent sheet-metal chassis
- Raspberry Pi 5 and Teensy 4.0 architecture
- LiDAR, IMU, and wheel encoders
- CAD, drawings, manufacturing files, BOM, wiring, datasheets, and safety documentation

### Software

- ROS 2 Jazzy and Gazebo Harmonic
- Nav2 autonomous navigation and LiDAR SLAM
- AprilTag-based visual auto-docking
- Visual odometry, URDF/Xacro, launch architecture, simulation, and Docker tooling

### Firmware

- Teensy 4.0 firmware and micro-ROS integration
- Differential-drive control, encoder odometry, IMU integration, PID control, diagnostics, calibration, and initial motion-safety mechanisms

### User interface

- Web operator interface
- Blockly no-code programming
- Maps, telemetry, diagnostics, and camera streaming
- Voice and large-language-model command workflow

## Planned next development cycle

During the next two months, the project plans to:

- Port the embedded firmware to STM32
- Introduce modular electronics and custom PCBs
- Improve power distribution and charging logic
- Add emergency-stop circuitry, watchdogs, fuses, overcurrent protection, electromagnetic-interference protection, and hot-swap concepts
- Improve electronics mounting, wiring, and serviceability
- Test and debug the navigation, docking, firmware, and UI stacks
- Expand documentation for workshops, corporate training, and university education

## Education roadmap

Planned learning material covers chassis design, manufacturing, electrical and electromechanical calculations, electronics, sensor integration, embedded real-time systems, micro-ROS, ROS 2 nodes, PID control, safety, URDF, user interfaces, commissioning, and maintenance.

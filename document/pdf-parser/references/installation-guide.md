# Installation Guide

## Prerequisites

| Dependency | Minimum Version | Required | Notes |
|---|---|---|---|
| Java (JDK) | 11+ | Yes | Must be on system PATH |
| Python | 3.10+ | Yes | For CLI and SDK |
| pip | Latest | Yes | Package manager |
| GPU | — | No | CPU-only operation |

## Java Installation

### Windows

1. Download the JDK installer from [Adoptium / Eclipse Temurin](https://adoptium.net/)
2. Run the installer (adds Java to PATH automatically)
3. Close and reopen the terminal, then verify:

```bash
java -version
# Expected output: openjdk version "11.x.x" or later
```

If `java -version` still fails after installation, manually add the JDK bin directory to the system PATH:
```
C:\Program Files\Eclipse Adoptium\jdk-<version>\bin
```

### macOS

```bash
brew install --cask temurin
```

### Ubuntu / Debian

```bash
sudo apt update
sudo apt install openjdk-17-jdk
```

## pip Installation

```bash
# Basic installation (local/deterministic mode)
pip install -U opendataloader-pdf

# With hybrid mode support (AI backends for tables, OCR, formulas)
pip install -U "opendataloader-pdf[hybrid]"
```

## Environment Verification

Run these commands to confirm everything is set up correctly:

```bash
# 1. Check Java
java -version
# Should output: openjdk version "11.x.x" or later

# 2. Check Python
python --version
# Should output: Python 3.10.x or later

# 3. Check opendataloader-pdf
opendataloader-pdf --help
# Should display the CLI usage information
```

## Hybrid Mode Additional Requirements

Hybrid mode downloads AI models on first run. Ensure:

| Resource | Requirement |
|---|---|
| RAM | ~2-4 GB (models loaded into memory) |
| Disk | ~1-2 GB (model files, cached after first download) |
| Network | Required for first-time model download |
| Port | Default 5002 (ensure not blocked by firewall) |

After installing with hybrid support:

```bash
# Start the hybrid backend server
opendataloader-pdf-hybrid --port 5002
```

## Uninstall

```bash
pip uninstall opendataloader-pdf
```

## License

opendataloader-pdf is released under the **Apache License 2.0** — fully permissive, commercial use allowed.

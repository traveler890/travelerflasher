![TravelerFlasher Logo](assets/traveler-logo.png)

*Flash fast. Travel far.*

[![License: GPLv3](https://img.shields.io/badge/license-GPLv3-blue)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-brightgreen)](https://www.python.org)

A minimalist, open-source utility for flashing TravelerOS ISO images to USB drives with persistent overlay support and UEFI compatibility.

## ✨ Features

- 📥 **Choose any version!** — Choose which TravelerOS release to install directly from the repo
- 🔍 **Drive Detection** — Safely identifies removable USB devices for flashing, so that way no horrible mistakes happen.
- 🧠 **Smart Flashing** — Formats, verifies, and writes ISO content with integrity checks
- 🔐 **ISO Verification** — SHA-256 hash comparison and layout inspection
- 🖥️ **Cross-platform Compatibility** — Designed for Linux, and Windows. (via PyInstaller builds)

## 🛠️ Installation

> TravelerFlasher is built in Python and packaged with PyQt6 for GUI support.

### Requirements
- Python 3.10+
- `PyQt6`, `requests`, `psutil`, `mtools`, `xorriso` (platform-dependent)
- Run:
```bash
pip install -r requirements.txt

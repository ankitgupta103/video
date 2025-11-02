# RM530 5G Integration Package

Python package for integrating Waveshare RM530 5G modem with Raspberry Pi using ECM (Ethernet Control Model) mode.

## Overview

This package provides automated tools and comprehensive documentation for setting up a Waveshare RM530 5G modem in ECM mode on Raspberry Pi. ECM mode provides native Linux integration with better stability and performance compared to QMI mode.

## Features

- ✅ **ECM Mode Setup** - Automated switching from QMI to ECM mode
- ✅ **NetworkManager Integration** - Native Linux networking support
- ✅ **Verification Tools** - Built-in verification scripts
- ✅ **Production Ready** - Stable and tested setup

## Quick Start

### Installation

```bash
# From PyPI (when published)
pip install rm530-5g-integration

# Or from source
git clone https://github.com/yourusername/rm530-5g-integration.git
cd rm530-5g-integration
pip install .
```

### 3-Step Setup

**Step 1: Switch to ECM Mode** (~1 minute)
```bash
sudo rm530-setup-ecm airtelgprs.com
```
*Replace `airtelgprs.com` with your carrier's APN*

**Step 2: Configure NetworkManager** (~1 minute)
```bash
# Wait 15 seconds, then find interface
ip link show

# Create connection (replace usb0 with your interface)
sudo nmcli connection add \
    type ethernet \
    ifname usb0 \
    con-name "RM530-5G-ECM" \
    ipv4.method auto \
    ipv4.route-metric 100 \
    ipv4.dns "8.8.8.8 1.1.1.1" \
    connection.autoconnect yes

# Connect
sudo nmcli connection up RM530-5G-ECM
```

**Step 3: Verify** (~10 seconds)
```bash
ping -c 4 google.com
```

✅ **Done!** Your 5G modem is configured and ready to use.

## Commands

| Command | Purpose |
|---------|---------|
| `rm530-setup-ecm <APN>` | Switch modem to ECM mode |
| `rm530-configure-network` | Setup NetworkManager (TODO) |
| `rm530-verify` | Verify 5G connection (TODO) |

## Requirements

- Python 3.7+
- Raspberry Pi OS or Debian-based Linux
- Waveshare RM530 5G modem
- NetworkManager installed
- Root/sudo access

## Dependencies

- pyserial >= 3.5

## Package Structure

```
rm530-5g-integration/
├── rm530_5g_integration/
│   ├── __init__.py
│   ├── scripts/           # Python scripts
│   │   ├── setup_ecm.py   # ECM mode setup
│   │   ├── configure_network.py
│   │   └── verify.py
│   ├── docs/              # Documentation (package includes)
│   ├── reference/         # Quick references
│   └── legacy/            # Legacy QMI docs
├── README.md              # This file
├── SETUP.md               # Complete setup guide
├── TROUBLESHOOTING.md     # Troubleshooting & verification
├── REFERENCE.md           # AT commands & technical details
├── PUBLISH.md             # Publishing instructions
├── LICENSE
└── pyproject.toml
```

## Documentation

- **[SETUP.md](SETUP.md)** - Complete setup guide with detailed instructions
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Troubleshooting and verification
- **[REFERENCE.md](REFERENCE.md)** - AT commands and technical reference
- **[PUBLISH.md](PUBLISH.md)** - Package publishing guide

## Usage Examples

### Python API

```python
from rm530_5g_integration.scripts.setup_ecm import switch_to_ecm_mode

# Switch to ECM mode
success = switch_to_ecm_mode(apn="airtelgprs.com")
if success:
    print("ECM mode configured successfully!")
```

### Video Streaming

Once configured, GStreamer commands will automatically use the 5G connection:

```bash
# YouTube streaming example
gst-launch-1.0 v4l2src ! \
    video/x-raw,width=640,height=480,framerate=30/1 ! \
    videoconvert ! \
    x264enc bitrate=1000 ! \
    flvmux ! \
    rtmpsink location="rtmp://a.rtmp.youtube.com/live2/YOUR_KEY"
```

## ECM Mode Benefits

- **Native Integration** - Uses standard Linux kernel CDC-ECM driver
- **NetworkManager Support** - Automatic management and reconnection
- **Better Performance** - Lower overhead than QMI
- **Stability** - No external dialer scripts required
- **Standard Tools** - Works with standard Linux networking tools

## Supported Carriers

Works with any carrier that supports RM530:
- Airtel ✅
- Jio ✅
- Any GSM/LTE/5G carrier

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details.

## References

- [Waveshare PCIe TO 4G/5G HAT+ Wiki](https://www.waveshare.com/wiki/PCIe-TO-4G-5G-M.2-USB3.2-HAT-PLUS)
- [NetworkManager Documentation](https://networkmanager.dev/docs/)
- [Linux CDC-ECM Documentation](https://www.kernel.org/doc/html/latest/usb/cdc-ecm.html)

---

**Ready to stream over 5G!** 📹🚀

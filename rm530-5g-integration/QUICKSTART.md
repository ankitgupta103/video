# Quick Start Guide

Get started with rm530-5g-integration in minutes.

## Installation

### From PyPI

```bash
pip install rm530-5g-integration
```

### From Source

```bash
git clone https://github.com/yourusername/rm530-5g-integration.git
cd rm530-5g-integration
pip install .
```

## Quick Setup (3 Steps)

### Step 1: Switch to ECM Mode

```bash
sudo rm530-setup-ecm airtelgprs.com
```

Replace `airtelgprs.com` with your carrier's APN.

**What it does**:
- Finds your modem serial port
- Switches from QMI to ECM mode
- Configures APN
- Resets modem

**Time**: ~1 minute

### Step 2: Configure NetworkManager

Wait 15 seconds for the modem to restart, then:

```bash
# Find the interface
ip link show

# Create NetworkManager connection (replace usb0 with your interface)
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

**Time**: ~1 minute

### Step 3: Verify

```bash
# Test internet
ping -c 4 google.com
```

**Time**: ~10 seconds

## Total Time: ~3 Minutes

✅ Done! Your 5G modem is configured and ready to use.

## What Next?

### Stream Video

Your GStreamer streaming commands will automatically use the 5G connection:

```bash
# YouTube streaming example
gst-launch-1.0 v4l2src ! \
    video/x-raw,width=640,height=480,framerate=30/1 ! \
    videoconvert ! \
    x264enc bitrate=1000 ! \
    flvmux ! \
    rtmpsink location="rtmp://a.rtmp.youtube.com/live2/YOUR_KEY"
```

### Monitor Connection

```bash
# Check status
ip route | grep default
nmcli connection show --active

# Check signal
sudo screen /dev/ttyUSB2 115200
# Type: AT+CSQ
# Exit: Ctrl+A then K
```

### Troubleshooting

```bash
# Verify connection
rm530-verify

# Restart connection
sudo nmcli connection up RM530-5G-ECM
```

See `rm530_5g_integration/reference/TROUBLESHOOTING.md` for detailed help.

## Need More Help?

- **Documentation**: `rm530_5g_integration/docs/`
- **References**: `rm530_5g_integration/reference/`
- **AT Commands**: `rm530_5g_integration/reference/AT-COMMANDS.md`
- **Issues**: Open a GitHub issue

## Features

✅ **ECM Mode** - Native Linux integration  
✅ **Automatic Setup** - One command configuration  
✅ **NetworkManager** - Standard Linux networking  
✅ **Production Ready** - Stable and tested  
✅ **Well Documented** - Complete guides included  

## Supported Carriers

Works with any carrier that supports RM530:
- Airtel ✅
- Jio ✅
- Any GSM/LTE/5G carrier

Just use the correct APN in Step 1.

---

**Ready to stream over 5G!** 📹🚀


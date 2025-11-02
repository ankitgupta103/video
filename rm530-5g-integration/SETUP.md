# Complete Setup Guide

Complete guide for setting up RM530 5G modem in ECM mode on Raspberry Pi.

## Overview

This guide will help you configure your **Waveshare RM530 5G modem** to use **ECM (Ethernet Control Model)** mode. ECM mode provides:
- ✅ Native Linux kernel driver integration
- ✅ Automatic network interface creation
- ✅ Seamless NetworkManager support
- ✅ Stable and responsive connectivity
- ✅ No external dialer tools required

## Prerequisites

- Raspberry Pi with Waveshare RM530 5G modem connected
- Python 3.7+ installed
- Root/sudo access
- NetworkManager installed (default on Raspberry Pi OS)

## Installation

### Install Package

```bash
# From PyPI (when published)
pip install rm530-5g-integration

# Or from source
git clone https://github.com/yourusername/rm530-5g-integration.git
cd rm530-5g-integration
pip install .
```

### Install Dependencies

```bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-serial usbutils
```

## Setup Steps

### Step 1: Find Modem Serial Interface

Find the modem's serial interface:

```bash
# List all serial devices
ls -la /dev/ttyUSB*

# Or check kernel messages
sudo dmesg | grep -i "tty\|usb\|modem"

# List USB devices
usb-devices | grep -A 20 "Qualcomm"
```

Typically, you'll find `/dev/ttyUSB2` or `/dev/ttyUSB3` as the AT command interface.

### Step 2: Switch Modem to ECM Mode

#### Option A: Automated Script (Recommended)

```bash
# Run the setup script (replace APN with your carrier)
sudo rm530-setup-ecm airtelgprs.com
```

The script will:
- Automatically find the modem serial port
- Test modem communication
- Switch to ECM mode
- Configure data interface
- Set your APN
- Reset the modem

#### Option B: Manual AT Commands

If you prefer manual setup:

```bash
# Install terminal emulator
sudo apt-get install -y screen

# Connect to modem (replace ttyUSB2 with your device)
sudo screen /dev/ttyUSB2 115200
```

Send these AT commands:
```
AT
AT+QCFG="usbnet",1
AT+QCFG="data_interface",0,0
AT+CGDCONT=1,"IP","airtelgprs.com"
AT+CFUN=1,1
```

**Exit screen**: Press `Ctrl+A` then `K`, then `Y` to confirm.

**Command explanation**:
- `AT` - Verify communication
- `AT+QCFG="usbnet",1` - Switch to ECM mode (1=ECM, 0=QMI, 2=MBIM, 3=RNDIS)
- `AT+QCFG="data_interface",0,0` - Configure data interface
- `AT+CGDCONT=1,"IP","airtelgprs.com"` - Set APN
- `AT+CFUN=1,1` - Full reset to apply changes

### Step 3: Wait for Modem Reset

Wait 15 seconds for the modem to restart:

```bash
echo "Waiting for modem to restart..."
sleep 15
```

### Step 4: Check for Network Interface

Verify the modem created a network interface:

```bash
ip link show
```

You should see a new interface like `usb0` or `wwan0` that wasn't there before.

### Step 5: Configure NetworkManager

Create a NetworkManager connection profile:

```bash
# Find your interface name first
ip link show

# Create connection (replace usb0 with your actual interface)
sudo nmcli connection add \
    type ethernet \
    ifname usb0 \
    con-name "RM530-5G-ECM" \
    ipv4.method auto \
    ipv4.never-default no \
    ipv4.route-metric 100 \
    ipv4.dns "8.8.8.8 1.1.1.1" \
    connection.autoconnect yes
```

**Parameters explained**:
- `type ethernet` - Treats modem as Ethernet interface
- `ifname usb0` - Specific interface name
- `con-name` - Friendly connection name
- `ipv4.method auto` - DHCP mode
- `ipv4.never-default no` - Allow this to be default route
- `ipv4.route-metric 100` - Higher priority than Wi-Fi
- `ipv4.dns` - Static DNS servers
- `connection.autoconnect yes` - Auto-connect on boot

### Step 6: Connect to 5G

Activate the connection:

```bash
sudo nmcli connection up RM530-5G-ECM
```

### Step 7: Prioritize 5G Over Other Connections

Ensure 5G has higher priority than Wi-Fi/Ethernet:

```bash
# List all connections
nmcli connection show

# Lower priority for Wi-Fi (replace with your connection name)
sudo nmcli connection modify "<wifi-name>" ipv4.route-metric 600
sudo nmcli connection modify "<wifi-name>" ipv4.never-default yes

# Lower priority for Ethernet (replace with your connection name)
sudo nmcli connection modify "<ethernet-name>" ipv4.route-metric 600
sudo nmcli connection modify "<ethernet-name>" ipv4.never-default yes
```

### Step 8: Verify Setup

Test connectivity:

```bash
# Check interface status
ip addr show usb0

# Check routing
ip route

# Test internet connectivity
ping -c 4 8.8.8.8
ping -c 4 google.com

# Check which interface is used
ip route get 8.8.8.8
```

You should see `dev usb0` or `dev wwan0` as the default route.

## After Setup

### Your Modem is Now Configured

Your 5G modem will:
- ✅ Auto-connect on boot
- ✅ Be managed by NetworkManager
- ✅ Have stable 5G connectivity
- ✅ Use proper routing (5G default, Wi-Fi/Ethernet secondary)
- ✅ Auto-reconnect on connection drops

### Using for Video Streaming

Your GStreamer applications will automatically use the 5G connection:

```bash
# Example: YouTube streaming
gst-launch-1.0 v4l2src ! \
    video/x-raw,width=640,height=480,framerate=30/1 ! \
    videoconvert ! \
    x264enc bitrate=1000 ! \
    flvmux ! \
    rtmpsink location="rtmp://a.rtmp.youtube.com/live2/YOUR_KEY"
```

### Monitor Connection

```bash
# Check connection status
nmcli connection show RM530-5G-ECM

# View statistics
ip addr show usb0
ip route show

# Check NetworkManager logs
journalctl -u NetworkManager -f
```

### Performance Expectations

- **Latency**: ~7-23ms (excellent)
- **Upload**: 100+ Mbps (5G)
- **Download**: 200+ Mbps (5G)
- **Stable for**: 720p, 1080p, 4K streaming

## Advanced Configuration

### Persistent ECM Mode (Optional)

To ensure ECM mode persists after power cycles, create a udev rule:

```bash
sudo apt-get install -y atinout

sudo tee /etc/udev/rules.d/99-rm530-ecm.rules << 'EOF'
# Switch RM530 to ECM mode when detected
ACTION=="add", SUBSYSTEM=="tty", ATTRS{idVendor}=="05c6", ATTRS{idProduct}=="90db", \
    RUN+="/bin/bash -c 'echo AT+QCFG=\"usbnet\",1 | atinout - /dev/%k /dev/null'"

# Reset modem after switching mode
ACTION=="add", SUBSYSTEM=="tty", ATTRS{idVendor}=="05c6", ATTRS{idProduct}=="90db", \
    RUN+="/bin/bash -c 'sleep 2 && echo AT+CFUN=1,1 | atinout - /dev/%k /dev/null'"
EOF

sudo udevadm control --reload-rules
sudo udevadm trigger
```

### Clean Up Old QMI Setup (Optional)

If you previously used waveshare-CM:

```bash
# Stop and disable waveshare service
sudo systemctl stop waveshare-CM 2>/dev/null
sudo systemctl disable waveshare-CM 2>/dev/null

# Remove waveshare script
sudo rm -f /usr/local/bin/waveshare-CM

# Disable old systemd service
sudo systemctl disable start-5g.service 2>/dev/null
sudo rm -f /etc/systemd/system/start-5g.service
sudo rm -f /usr/local/bin/start-5g.sh
sudo systemctl daemon-reload
```

## Troubleshooting Setup Issues

### Script Can't Find Modem

```bash
# Stop ModemManager (it may lock the port)
sudo systemctl stop ModemManager

# Run setup again
sudo rm530-setup-ecm airtelgprs.com

# Restart ModemManager after
sudo systemctl start ModemManager
```

### Modem Not Detected

```bash
# Check USB connections
lsusb | grep Qualcomm

# Check kernel messages
sudo dmesg | grep -i qualcomm

# Verify PCIe link
lspci | grep -i pcie
```

### Interface Not Created

```bash
# Verify ECM mode is set
sudo screen /dev/ttyUSB2 115200
AT+QCFG="usbnet"
# Should return: +QCFG: "usbnet",1
# Exit: Ctrl+A then K

# Manually reset if needed
sudo screen /dev/ttyUSB2 115200
AT+CFUN=1,1
```

### No IP Assignment

```bash
# Check DHCP client logs
sudo journalctl -u NetworkManager -f

# Try manual DHCP
sudo dhclient usb0

# Check if interface is up
ip link set usb0 up
```

For more troubleshooting, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

## ECM vs QMI Comparison

| Feature | QMI Mode | ECM Mode |
|---------|----------|----------|
| **Setup** | Complex (multiple tools) | Simple (native) |
| **Stability** | Good | Excellent |
| **Reconnection** | Manual/scripted | Automatic |
| **DNS Management** | Manual/chattr | NetworkManager |
| **Interface** | wwan0 | usb0/wwan0 |
| **Speed** | Good | Better (less overhead) |
| **Debugging** | Limited tools | Standard Linux tools |

**Recommendation**: Use ECM mode for better stability and simpler management.

## Expected Result

After completing this setup:

✅ Modem automatically starts in ECM mode at boot  
✅ NetworkManager creates interface automatically  
✅ Stable 5G connectivity without interruptions  
✅ Automatic DNS configuration  
✅ Proper routing (5G is default, Wi-Fi/Ethernet secondary)  
✅ Auto-reconnect on connection drops  
✅ Ready for video streaming applications  

## Next Steps

- Verify your connection: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Learn AT commands: See [REFERENCE.md](REFERENCE.md)
- Start streaming: Your GStreamer commands will automatically use 5G

---

**Setup complete!** Your 5G modem is now ready for high-speed video streaming. 📹🚀


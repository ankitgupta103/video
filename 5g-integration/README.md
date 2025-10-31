# RM530 5G Modem Integration

This directory contains integration guides and scripts for configuring the Waveshare RM530 5G modem with Raspberry Pi.

## Integration Options

### Option 1: ECM Mode (Recommended) ✅

**Best for**: Stable, uninterrupted connectivity with native Linux integration

**File**: `ecm-integration.md`

**Benefits**:
- Uses native Linux kernel ECM driver
- Managed by NetworkManager (standard Linux networking)
- No external dialer tools needed
- More stable than QMI
- Automatic reconnection
- Better performance

**Use this if**: You want reliable, uninterrupted internet without custom scripts.

### Option 2: QMI Mode

**Best for**: Legacy compatibility with waveshare-CM tools

**File**: `integration.md`

**Benefits**:
- Well-documented by Waveshare
- Works with official Waveshare tools

**Limitations**:
- Requires waveshare-CM external dialer
- Potential connectivity interruptions
- Manual DNS management
- More complex setup

**Use this if**: You have specific requirements for QMI mode or legacy compatibility.

---

## Quick Start: ECM Mode

### 1. Install Python Serial Library

```bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-serial
```

### 2. Run ECM Setup Script

```bash
cd 5g-integration
sudo python3 setup-ecm-mode.py airtelgprs.com
```

Replace `airtelgprs.com` with your carrier's APN.

### 3. Wait for Modem Reset

Wait 15 seconds for the modem to restart in ECM mode.

### 4. Configure NetworkManager

```bash
# Find the new interface name
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

### 5. Verify Connectivity

```bash
# Check IP
ip addr show usb0

# Test internet
ping -c 4 8.8.8.8
ping -c 4 google.com
```

---

## Files in This Directory

| File | Purpose |
|------|---------|
| `ecm-integration.md` | Complete ECM mode setup guide |
| `integration.md` | QMI mode setup guide (legacy) |
| `setup-ecm-mode.py` | Python script to switch modem to ECM mode |
| `README.md` | This file |

---

## Understanding the Difference

### QMI (Qualcomm MSM Interface)

- Protocol: Qualcomm-specific QMI protocol
- Tools: waveshare-CM, qmicli
- Interface: wwan0
- Management: External scripts
- Stability: Can have interruptions

### ECM (Ethernet Control Model)

- Protocol: Standard USB CDC-ECM
- Tools: Native Linux kernel driver
- Interface: usb0 or wwan0
- Management: NetworkManager
- Stability: More stable, native support

---

## Troubleshooting

### Can't Find Modem

```bash
# Check USB devices
lsusb | grep Qualcomm

# Check serial ports
ls -la /dev/ttyUSB*

# Check dmesg
sudo dmesg | grep -i "tty\|usb\|qualcomm"
```

### Interface Not Created

```bash
# Verify ECM mode is set
sudo screen /dev/ttyUSB2 115200
# Type: AT+QCFG="usbnet"
# Should return: +QCFG: "usbnet",1
```

### No Internet

```bash
# Check interface status
ip link show usb0

# Check routing
ip route

# Check DNS
cat /etc/resolv.conf
```

See `ecm-integration.md` for detailed troubleshooting steps.

---

## References

- [Waveshare PCIe TO 4G/5G M.2 USB3.2 HAT+ Wiki](https://www.waveshare.com/wiki/PCIe-TO-4G-5G-M.2-USB3.2-HAT-PLUS)
- [RM530 AT Commands](https://www.waveshare.com/wiki/RM520N-GL-5G-HAT-PLUS)
- [NetworkManager Documentation](https://networkmanager.dev/docs/)
- [Linux USB CDC-ECM Documentation](https://www.kernel.org/doc/html/latest/usb/cdc-ecm.html)


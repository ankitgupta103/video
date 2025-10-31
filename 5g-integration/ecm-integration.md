# RM530 5G Modem - ECM Mode Integration (Native NetworkManager)

## Overview

Configure the **Waveshare RM530 5G modem** to use **ECM (Ethernet Control Model)** mode instead of QMI. This approach:
- ✅ Uses native Linux kernel drivers (no QMI overhead)
- ✅ Automatically creates a network interface
- ✅ Works seamlessly with NetworkManager
- ✅ More stable and responsive connectivity
- ✅ No interruptions from waveshare-CM dialer

**Goal**: Use ECM mode for native Linux network integration without external dialer tools.

---

## Prerequisites

- Raspberry Pi with Waveshare RM530 5G modem connected
- Serial terminal access to the modem (for AT commands)
- Root/sudo access
- NetworkManager installed (default on Raspberry Pi OS)

---

## Step 1: Access Modem Serial Interface

First, find the modem's serial interface:

```bash
# List all serial devices
ls -la /dev/ttyUSB*

# Or check syslog for modem detection
sudo dmesg | grep -i "tty\|usb\|modem"
```

Typically, you'll see `/dev/ttyUSB2` or `/dev/ttyUSB3` as the AT command interface. You can verify by checking device descriptions:

```bash
# Install useful tools if not present
sudo apt-get update
sudo apt-get install -y usbutils modemmanager

# List USB devices
usb-devices | grep -A 20 "Qualcomm"

# Or use mmcli if ModemManager is running
mmcli -L
```

---

## Step 2: Switch Modem to ECM Mode

### Option A: Automated Script (Recommended)

Use the provided Python script for easy setup:

```bash
# Install Python serial library
sudo apt-get update
sudo apt-get install -y python3-pip python3-serial

# Run the setup script (replace APN with your carrier)
cd /path/to/video/5g-integration
sudo python3 setup-ecm-mode.py airtelgprs.com
```

The script will:
- Automatically find the modem serial port
- Test modem communication
- Switch to ECM mode
- Configure data interface
- Set your APN
- Reset the modem

**Proceed to Step 3 after the script completes.**

### Option B: Manual AT Commands

If you prefer manual setup or the script doesn't work:

```bash
# Install terminal emulator
sudo apt-get install -y screen

# Connect to modem (replace ttyUSB2 with your device)
sudo screen /dev/ttyUSB2 115200
```

Once connected, send the following AT commands to switch to ECM mode:

```
AT
AT+QCFG="usbnet",1
AT+QCFG="data_interface",0,0
AT+CFUN=1,1
```

**Explanation**:
- `AT` - Verify communication
- `AT+QCFG="usbnet",1` - Switch to ECM mode (1 = ECM, 0 = QMI, 2 = MBIM, 3 = RNDIS)
- `AT+QCFG="data_interface",0,0` - Configure data interface
- `AT+CFUN=1,1` - Full reset to apply changes

**Exit screen**: Press `Ctrl+A` then `K` to kill session, then `Y` to confirm.

---

## Step 3: Verify Modem Reset and ECM Interface

After the modem resets, verify it creates a network interface:

```bash
# Wait a few seconds for modem to restart
sleep 5

# Check for new network interfaces
ip link show

# Look for usb0, wwan0, or similar interface
```

You should see a new interface like `usb0` or `wwan0` that wasn't there before.

---

## Step 4: Configure NetworkManager Connection

Create a NetworkManager connection profile for the ECM interface:

```bash
# Create connection profile with your APN
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
- `type ethernet` - Treats the modem as an Ethernet interface
- `ifname usb0` - Specific interface (adjust if yours has different name)
- `con-name` - Friendly connection name
- `ipv4.method auto` - DHCP mode
- `ipv4.never-default no` - Allow this to be default route
- `ipv4.route-metric 100` - Higher priority than Wi-Fi (lower metric = higher priority)
- `ipv4.dns` - Static DNS servers
- `connection.autoconnect yes` - Auto-connect on boot

---

## Step 5: Prioritize 5G Over Other Connections

Ensure 5G modem has higher priority than Wi-Fi/Ethernet:

```bash
# Set Wi-Fi interfaces to lower priority
sudo nmcli connection modify <wifi-connection-name> ipv4.route-metric 600
sudo nmcli connection modify <wifi-connection-name> ipv4.never-default yes

# Set Ethernet interfaces to lower priority
sudo nmcli connection modify <ethernet-connection-name> ipv4.route-metric 600
sudo nmcli connection modify <ethernet-connection-name> ipv4.never-default yes
```

**List all connections** to get connection names:
```bash
nmcli connection show
```

---

## Step 6: Connect and Test

Activate the new connection:

```bash
# Connect to 5G
sudo nmcli connection up RM530-5G-ECM

# Verify interface got IP
ip addr show usb0

# Check routing table
ip route

# Test connectivity
ping -c 4 8.8.8.8
ping -c 4 google.com
```

---

## Step 7: Configure APN (if needed)

If your carrier requires a specific APN, you may need to set it through AT commands:

```bash
# Connect to modem again
sudo screen /dev/ttyUSB2 115200

# Set APN (example: airtelgprs.com)
AT+CGDCONT=1,"IP","airtelgprs.com"

# Reset to apply
AT+CFUN=1,1
```

---

## Step 8: Create Persistent AT Command Script (Optional)

To ensure ECM mode persists after power cycles, create a udev rule:

```bash
# Create udev rule
sudo tee /etc/udev/rules.d/99-rm530-ecm.rules << 'EOF'
# Switch RM530 to ECM mode when detected
ACTION=="add", SUBSYSTEM=="tty", ATTRS{idVendor}=="05c6", ATTRS{idProduct}=="90db", \
    RUN+="/bin/bash -c 'echo AT+QCFG=\"usbnet\",1 | atinout - /dev/%k /dev/null'"

# Reset modem after switching mode
ACTION=="add", SUBSYSTEM=="tty", ATTRS{idVendor}=="05c6", ATTRS{idProduct}=="90db", \
    RUN+="/bin/bash -c 'sleep 2 && echo AT+CFUN=1,1 | atinout - /dev/%k /dev/null'"
EOF

# Reload udev rules
sudo udevadm control --reload-rules
sudo udevadm trigger
```

**Note**: This requires the `atinout` package:
```bash
sudo apt-get install -y atinout
```

---

## Step 9: Clean Up Old QMI Setup (Optional)

If you previously used waveshare-CM and want to remove it:

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

---

## Troubleshooting

### Script Can't Find Modem Serial Port

If the script fails to find the modem:
```bash
# 1. Check if ModemManager is locking the port
sudo systemctl stop ModemManager

# 2. Run the script again
sudo python3 setup-ecm-mode.py airtelgprs.com

# 3. Re-enable ModemManager after
sudo systemctl start ModemManager
```

The script will automatically detect and offer to stop ModemManager.

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
# Check if ECM mode is set
sudo screen /dev/ttyUSB2 115200
AT+QCFG="usbnet"
# Should return: +QCFG: "usbnet",1

# Manually reset
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

### DNS Issues
```bash
# Verify DNS settings
nmcli connection show RM530-5G-ECM | grep dns

# Test DNS resolution
nslookup google.com 8.8.8.8
```

### Connection Drops
```bash
# Check modem signal strength
sudo screen /dev/ttyUSB2 115200
AT+QCSQ
AT+CSQ

# Check network registration
AT+CREG?
AT+QNWINFO
```

---

## Comparison: ECM vs QMI

| Feature | QMI (waveshare-CM) | ECM (Native) |
|---------|-------------------|--------------|
| **Mode** | External dialer tool | Kernel driver |
| **Interface** | wwan0 | usb0/wwan0 |
| **Management** | waveshare-CM process | NetworkManager |
| **Stability** | Can have interruptions | More stable |
| **Auto-reconnect** | Requires custom script | Native support |
| **DNS Handling** | Manual setup | Integrated |
| **Configuration** | Command line flags | nmcli/gui |
| **Speed** | Good | Better (less overhead) |

---

## Expected Result

After completing this setup:

✅ Modem automatically starts in ECM mode at boot  
✅ NetworkManager creates interface automatically  
✅ Stable 5G connectivity without interruptions  
✅ Automatic DNS configuration  
✅ Proper routing (5G is default, Wi-Fi/Ethernet secondary)  
✅ Auto-reconnect on connection drops  
✅ No need for waveshare-CM or custom scripts  

---

## Additional Resources

- [RM530 AT Command Manual](https://www.waveshare.com/wiki/RM520N-GL-5G-HAT-PLUS)
- [NetworkManager Documentation](https://networkmanager.dev/docs/)
- [Qualcomm 5G Modem Linux Support](https://docs.kernel.org/networking/device_drivers/wwan/)


# Troubleshooting Guide

Common issues and solutions for RM530 5G integration.

---

## 🔴 Connection Issues

### No IP Address Assigned

**Symptoms**: Interface up but no IP

**Check**:
```bash
ip addr show usb0  # Should show inet
```

**Solution**:
```bash
# Request DHCP manually
sudo dhclient usb0

# Check NetworkManager logs
journalctl -u NetworkManager -f
```

### Interface Not Created

**Symptoms**: No usb0 or wwan0 interface

**Check**:
```bash
ip link show | grep -E "usb0|wwan0"
ls -la /dev/ttyUSB*
```

**Solution**:
```bash
# Verify ECM mode is set
sudo screen /dev/ttyUSB2 115200
# Type: AT+QCFG="usbnet"
# Should return: +QCFG: "usbnet",1
# Exit: Ctrl+A then K

# Reset modem if wrong mode
# Re-run: python3 scripts/setup-ecm-mode.py airtelgprs.com
```

### Cannot Reach Internet

**Symptoms**: Has IP but can't ping 8.8.8.8

**Check**:
```bash
ping -c 3 8.8.8.8
ip route
```

**Solution**:
```bash
# Ensure default route uses usb0
sudo ip route replace default dev usb0

# Check DNS
cat /etc/resolv.conf

# Restart NetworkManager
sudo systemctl restart NetworkManager
sudo nmcli connection up RM530-5G-ECM
```

---

## 📶 Signal Issues

### Poor Signal Strength

**Check**:
```bash
sudo screen /dev/ttyUSB2 115200
# Type: AT+CSQ
# Exit: Ctrl+A then K
```

**Interpretation**:
- 0-10: Poor signal
- 11-20: Fair signal
- 21-31: Good signal

**Solution**:
- Adjust antenna position
- Check antenna connections
- Move device location
- Check if near base station

### Not Registered on Network

**Check**:
```bash
sudo screen /dev/ttyUSB2 115200
# Type: AT+CREG?
# Should show: 0,1 (registered)
```

**Solution**:
- Check SIM card is active
- Verify carrier compatibility
- Check APN settings
- Try: `AT+CFUN=1,1` (reset)

---

## 🔧 NetworkManager Issues

### Connection Won't Activate

**Symptoms**: `nmcli connection up RM530-5G-ECM` fails

**Check**:
```bash
nmcli connection show RM530-5G-ECM
nmcli device status
```

**Solution**:
```bash
# Delete and recreate
nmcli connection delete RM530-5G-ECM
bash scripts/configure-network.sh
```

### ModemManager Conflicts

**Symptoms**: Port locked, can't send AT commands

**Check**:
```bash
systemctl status ModemManager
```

**Solution**:
```bash
# Stop temporarily
sudo systemctl stop ModemManager

# Run your command
sudo python3 scripts/setup-ecm-mode.py

# Restart
sudo systemctl start ModemManager
```

---

## 🔄 Routing Issues

### Wrong Default Route

**Symptoms**: Traffic uses Wi-Fi instead of 5G

**Check**:
```bash
ip route | grep default
```

**Solution**:
```bash
# Make 5G default
sudo nmcli connection modify RM530-5G-ECM ipv4.route-metric 100

# Lower other connection priority
sudo nmcli connection modify "Wi-Fi-Name" ipv4.route-metric 600
sudo nmcli connection modify "Wi-Fi-Name" ipv4.never-default yes

# Reconnect
sudo nmcli connection down RM530-5G-ECM
sudo nmcli connection up RM530-5G-ECM
```

### DNS Issues

**Symptoms**: Can ping IPs but not domain names

**Check**:
```bash
cat /etc/resolv.conf
nslookup google.com
```

**Solution**:
```bash
# Force DNS in connection
nmcli connection modify RM530-5G-ECM ipv4.dns "8.8.8.8 1.1.1.1"

# Restart connection
sudo nmcli connection up RM530-5G-ECM

# Test DNS
nslookup google.com 8.8.8.8
```

---

## 🔴 Hardware Issues

### Modem Not Detected

**Symptoms**: No /dev/ttyUSB* devices

**Check**:
```bash
lsusb | grep Qualcomm
dmesg | grep -i "usb\|qualcomm\|cdc_ecm"
```

**Solution**:
- Check physical connections
- Verify PCIe link is working
- Check power to modem
- Try reboot

### Interface Keeps Disconnecting

**Check**:
```bash
journalctl -u NetworkManager -f
```

**Solution**:
- Check signal strength
- Check antenna connections
- Check for overheating
- Verify power supply

---

## 🐛 Script Issues

### setup-ecm-mode.py Can't Find Modem

**Symptoms**: "Could not find modem serial port"

**Check**:
```bash
ls -la /dev/ttyUSB*
```

**Solution**:
```bash
# Install required packages
sudo apt-get install python3-serial

# Stop ModemManager
sudo systemctl stop ModemManager

# Try manual port specification
# Edit script to use specific port
```

### Permission Denied

**Symptoms**: "PermissionError" on serial port

**Solution**:
```bash
# Add user to dialout group
sudo usermod -aG dialout $USER

# Logout and login again
# Or use sudo
sudo python3 scripts/setup-ecm-mode.py airtelgprs.com
```

---

## 🔍 Diagnostic Commands

### Complete Status Check

```bash
# Run full diagnostic
bash scripts/verify-5g.sh
```

### Manual Checks

```bash
# 1. Interface status
ip link show usb0

# 2. IP address
ip addr show usb0

# 3. Routing
ip route

# 4. DNS
cat /etc/resolv.conf

# 5. Connectivity
ping -c 4 8.8.8.8
ping -c 4 google.com

# 6. NetworkManager
nmcli connection show --active
nmcli device status

# 7. System logs
journalctl -u NetworkManager -n 50

# 8. Modem info
sudo screen /dev/ttyUSB2 115200
# AT+CSQ
# AT+CREG?
# AT+QNWINFO
```

---

## 🆘 Still Not Working?

### Full Reset Sequence

```bash
# 1. Stop all connections
sudo nmcli connection down RM530-5G-ECM
sudo nmcli connection down <wifi-name>

# 2. Restart NetworkManager
sudo systemctl restart NetworkManager

# 3. Re-run setup
sudo python3 scripts/setup-ecm-mode.py airtelgprs.com
sleep 15

# 4. Re-configure network
bash scripts/configure-network.sh

# 5. Verify
bash scripts/verify-5g.sh
```

### Collect Debug Info

```bash
# Save diagnostic info
{
    echo "=== System Info ==="
    uname -a
    echo ""
    echo "=== Interfaces ==="
    ip link show
    echo ""
    echo "=== Routing ==="
    ip route
    echo ""
    echo "=== DNS ==="
    cat /etc/resolv.conf
    echo ""
    echo "=== NetworkManager ==="
    nmcli connection show
    nmcli device status
    echo ""
    echo "=== Modem USB ==="
    lsusb | grep Qualcomm
    echo ""
    echo "=== Logs ==="
    journalctl -u NetworkManager -n 50
} > debug-info.txt

# Share debug-info.txt for help
```

---

## 📞 Getting Help

**Include in your question**:
1. What you're trying to do
2. Exact error message
3. Output of: `bash scripts/verify-5g.sh`
4. Relevant logs

**Resources**:
- Main docs: `docs/ecm-integration.md`
- Waveshare wiki: https://www.waveshare.com/wiki/PCIe-TO-4G-5G-M.2-USB3.2-HAT-PLUS
- NetworkManager: https://networkmanager.dev/docs/

---

## ✅ Prevention

**Best Practices**:
1. Always verify after changes: `bash scripts/verify-5g.sh`
2. Keep scripts backed up
3. Document custom changes
4. Check signal strength periodically
5. Monitor logs: `journalctl -u NetworkManager -f`

---

Last updated: After ECM integration


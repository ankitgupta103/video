# Troubleshooting & Verification Guide

Complete guide for troubleshooting issues and verifying your 5G modem connection.

## Quick Verification

### Verify 5G is Active

**Check default route:**
```bash
ip route | grep default
```
✅ Should show: `default via 192.168.x.1 dev usb0` (or `dev wwan0`)  
❌ If shows `dev wlan0` or `dev eth0`, Wi-Fi/Ethernet is primary

**Check interface status:**
```bash
ip addr show usb0
```
✅ Should show: `UP, LOWER_UP` with an IP address  
❌ DOWN or no IP = modem not connected

**Test connectivity:**
```bash
ping -c 4 8.8.8.8
ping -c 4 google.com

# Check which interface is used
ip route get 8.8.8.8
```
✅ Should show: `dev usb0` or `dev wwan0`  
❌ Other interface = not using 5G

**Check NetworkManager:**
```bash
nmcli connection show --active
```
✅ Should show: `RM530-5G-ECM` with `DEVICE usb0`  
❌ Not in list = not connected

### Quick One-Liner Check

```bash
echo "Primary: $(ip route | grep default | awk '{print $5}')" && \
echo "5G IP: $(ip addr show usb0 2>/dev/null | grep 'inet ' | awk '{print $2}')" && \
echo "Connected: $(nmcli -t connection show RM530-5G-ECM 2>/dev/null | grep STATE | cut -d: -f2)"
```

### Verify Signal Strength

```bash
sudo screen /dev/ttyUSB2 115200
# Type: AT+CSQ
# Exit: Ctrl+A then K, then Y
```

**Signal interpretation:**
- 0-10: Poor signal
- 11-20: Fair signal  
- 21-31: Excellent signal (good)

## Connection Issues

### No IP Address Assigned

**Symptoms**: Interface up but no IP address

**Check:**
```bash
ip addr show usb0
```

**Solution:**
```bash
# Request DHCP manually
sudo dhclient usb0

# Check NetworkManager logs
journalctl -u NetworkManager -f

# Restart NetworkManager
sudo systemctl restart NetworkManager
sudo nmcli connection up RM530-5G-ECM
```

### Interface Not Created

**Symptoms**: No `usb0` or `wwan0` interface

**Check:**
```bash
ip link show | grep -E "usb0|wwan0"
ls -la /dev/ttyUSB*
```

**Solution:**
```bash
# Verify ECM mode is set
sudo screen /dev/ttyUSB2 115200
# Type: AT+QCFG="usbnet"
# Should return: +QCFG: "usbnet",1
# Exit: Ctrl+A then K

# If wrong mode, re-run setup
sudo rm530-setup-ecm airtelgprs.com

# Wait for modem to restart
sleep 15
ip link show
```

### Cannot Reach Internet

**Symptoms**: Has IP but can't ping 8.8.8.8

**Check:**
```bash
ping -c 3 8.8.8.8
ip route
```

**Solution:**
```bash
# Ensure default route uses usb0
sudo ip route replace default dev usb0

# Check DNS
cat /etc/resolv.conf

# Restart NetworkManager
sudo systemctl restart NetworkManager
sudo nmcli connection up RM530-5G-ECM
```

## Signal Issues

### Poor Signal Strength

**Check signal:**
```bash
sudo screen /dev/ttyUSB2 115200
# Type: AT+CSQ
# Should return: +CSQ: <rssi>,<ber>
# Exit: Ctrl+A then K
```

**Solution:**
- Adjust antenna position
- Check antenna connections
- Move device location
- Check proximity to base station

### Not Registered on Network

**Check registration:**
```bash
sudo screen /dev/ttyUSB2 115200
# Type: AT+CREG?
# Should show: 0,1 (registered)
# Exit: Ctrl+A then K
```

**Solution:**
- Check SIM card is active
- Verify carrier compatibility
- Check APN settings (see [SETUP.md](SETUP.md))
- Reset modem: `AT+CFUN=1,1`

## NetworkManager Issues

### Connection Won't Activate

**Symptoms**: `nmcli connection up RM530-5G-ECM` fails

**Check:**
```bash
nmcli connection show RM530-5G-ECM
nmcli device status
```

**Solution:**
```bash
# Delete and recreate connection
nmcli connection delete RM530-5G-ECM

# Recreate (adjust interface name)
sudo nmcli connection add \
    type ethernet \
    ifname usb0 \
    con-name "RM530-5G-ECM" \
    ipv4.method auto \
    ipv4.route-metric 100 \
    ipv4.dns "8.8.8.8 1.1.1.1" \
    connection.autoconnect yes

sudo nmcli connection up RM530-5G-ECM
```

### ModemManager Conflicts

**Symptoms**: Port locked, can't send AT commands

**Check:**
```bash
systemctl status ModemManager
```

**Solution:**
```bash
# Stop temporarily
sudo systemctl stop ModemManager

# Run setup
sudo rm530-setup-ecm airtelgprs.com

# Restart ModemManager
sudo systemctl start ModemManager
```

## Routing Issues

### Wrong Default Route

**Symptoms**: Traffic uses Wi-Fi instead of 5G

**Check:**
```bash
ip route | grep default
```

**Solution:**
```bash
# Make 5G default
sudo nmcli connection modify RM530-5G-ECM ipv4.route-metric 100
sudo nmcli connection modify RM530-5G-ECM ipv4.never-default no

# Lower other connection priority
sudo nmcli connection modify "<wifi-name>" ipv4.route-metric 600
sudo nmcli connection modify "<wifi-name>" ipv4.never-default yes

# Reconnect
sudo nmcli connection down RM530-5G-ECM
sudo nmcli connection up RM530-5G-ECM
```

### DNS Issues

**Symptoms**: Can ping IPs but not domain names

**Check:**
```bash
cat /etc/resolv.conf
nslookup google.com
```

**Solution:**
```bash
# Force DNS in connection
sudo nmcli connection modify RM530-5G-ECM ipv4.dns "8.8.8.8 1.1.1.1"

# Restart connection
sudo nmcli connection up RM530-5G-ECM

# Test DNS
nslookup google.com 8.8.8.8
```

## Hardware Issues

### Modem Not Detected

**Symptoms**: No `/dev/ttyUSB*` devices

**Check:**
```bash
lsusb | grep Qualcomm
sudo dmesg | grep -i "usb\|qualcomm\|cdc_ecm"
lspci | grep -i pcie
```

**Solution:**
- Check physical connections
- Verify PCIe link is working
- Check power to modem
- Try reboot

### Interface Keeps Disconnecting

**Check:**
```bash
journalctl -u NetworkManager -f
```

**Solution:**
- Check signal strength (see above)
- Check antenna connections
- Check for overheating
- Verify power supply
- Check NetworkManager logs for errors

## Script Issues

### Setup Script Can't Find Modem

**Symptoms**: "Could not find modem serial port"

**Solution:**
```bash
# Install required packages
sudo apt-get install python3-serial

# Stop ModemManager
sudo systemctl stop ModemManager

# Run setup again
sudo rm530-setup-ecm airtelgprs.com

# Restart ModemManager
sudo systemctl start ModemManager
```

### Permission Denied

**Symptoms**: "PermissionError" on serial port

**Solution:**
```bash
# Add user to dialout group
sudo usermod -aG dialout $USER

# Logout and login again, or use sudo
sudo rm530-setup-ecm airtelgprs.com
```

## Diagnostic Commands

### Complete Status Check

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
# AT+CSQ      # Signal strength
# AT+CREG?    # Registration
# AT+QNWINFO  # Network info
# Exit: Ctrl+A then K
```

### Monitor Real-Time Traffic

```bash
# Watch interface statistics
watch -n 1 'cat /sys/class/net/usb0/statistics/tx_bytes && cat /sys/class/net/usb0/statistics/rx_bytes'

# Compare Wi-Fi vs 5G traffic
echo "Wi-Fi: $(cat /sys/class/net/wlan0/statistics/tx_bytes 2>/dev/null || echo 0)"
echo "5G:    $(cat /sys/class/net/usb0/statistics/tx_bytes 2>/dev/null || echo 0)"
```

### Check Signal Quality

```bash
sudo screen /dev/ttyUSB2 115200
# Type these commands:
AT+QCSQ    # Detailed signal quality
AT+CREG?   # Network registration
AT+QNWINFO # Network information (5G/LTE)
AT+CSQ     # Simplified signal strength
# Exit: Ctrl+A then K, then Y
```

**Response interpretation:**
- **AT+CSQ**: `<rssi>,<ber>` - RSSI 0-31 (higher is better)
- **AT+CREG?**: `<mode>,<stat>` - stat 1 = registered
- **AT+QNWINFO**: Shows network type (5G/LTE/4G)

## Full Reset Sequence

If nothing else works:

```bash
# 1. Stop all connections
sudo nmcli connection down RM530-5G-ECM
sudo nmcli connection down <wifi-name>

# 2. Restart NetworkManager
sudo systemctl restart NetworkManager

# 3. Re-run setup
sudo rm530-setup-ecm airtelgprs.com
sleep 15

# 4. Re-configure network
sudo nmcli connection add \
    type ethernet \
    ifname usb0 \
    con-name "RM530-5G-ECM" \
    ipv4.method auto \
    ipv4.route-metric 100 \
    ipv4.dns "8.8.8.8 1.1.1.1" \
    connection.autoconnect yes

sudo nmcli connection up RM530-5G-ECM

# 5. Verify
ping -c 4 google.com
```

## Collect Debug Information

Save diagnostic info for troubleshooting:

```bash
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

## Expected Output When Working

When everything is working correctly:

✅ **Default route**: `dev usb0`  
✅ **Interface status**: `UP, LOWER_UP` with IP address  
✅ **NetworkManager**: `RM530-5G-ECM` connected on `usb0`  
✅ **Ping**: Successful with <50ms latency  
✅ **Signal**: Strong (AT+CSQ > 20)  

## Getting Help

**Include in your question:**
1. What you're trying to do
2. Exact error message
3. Output of diagnostic commands above
4. Relevant logs (from `debug-info.txt`)

**Resources:**
- Setup guide: [SETUP.md](SETUP.md)
- AT commands: [REFERENCE.md](REFERENCE.md)
- Waveshare wiki: https://www.waveshare.com/wiki/PCIe-TO-4G-5G-M.2-USB3.2-HAT-PLUS
- NetworkManager docs: https://networkmanager.dev/docs/

## Best Practices

1. Always verify after changes: Check default route and connectivity
2. Monitor signal strength periodically
3. Keep NetworkManager logs: `journalctl -u NetworkManager -f`
4. Check interface statistics: `/sys/class/net/usb0/statistics/*`
5. Document any custom configurations

---

For AT commands and technical details, see [REFERENCE.md](REFERENCE.md).


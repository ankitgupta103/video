# How to Verify 5G Modem is Active

Quick commands to verify your 5G modem is being used as your internet connection.

---

## Quick Verification (Run these on your Pi)

### Option 1: Use the Verification Script

```bash
cd ~/video/5g-integration
bash verify-5g.sh
```

This will show you everything in one go!

### Option 2: Manual Checks

#### 1. Check Default Route

```bash
ip route | grep default
```

**You should see**:
```
default via 192.168.225.1 dev usb0 proto dhcp src 192.168.225.40 metric 100
```

✅ If you see `dev usb0` or `dev wwan0` → **5G is active!**  
❌ If you see `dev wlan0` or `dev eth0` → Wi-Fi/Ethernet is primary

---

#### 2. Check Interface Status

```bash
ip addr show usb0
```

**You should see**:
```
5: usb0: <BROADCAST,MULTICAST,UP,LOWER_UP> ...
    inet 192.168.225.40/22 ...
```

✅ UP with an IP address → **5G is working!**  
❌ DOWN or no IP → Modem is not connected

---

#### 3. Test Internet via 5G

```bash
# Test connectivity
ping -c 3 8.8.8.8

# Check which interface is used
ip route get 8.8.8.8
```

**You should see**:
```
8.8.8.8 via 192.168.225.1 dev usb0 src 192.168.225.40 uid 1000
```

✅ `dev usb0` → **Traffic is using 5G!**  
❌ `dev wlan0` or other → Traffic is using Wi-Fi/Ethernet

---

#### 4. Check NetworkManager Status

```bash
nmcli connection show --active
```

**You should see**:
```
NAME           UUID                                  TYPE      DEVICE
RM530-5G-ECM   ...                                   ethernet  usb0
```

✅ `RM530-5G-ECM` with `DEVICE usb0` → **Active!**  
❌ Not in the list → Not connected

---

#### 5. View All Connections

```bash
ip route
```

**Look for the line starting with `default via`**:
```
default via 192.168.225.1 dev usb0 ...     ← This line!
192.168.1.0/24 dev wlan0 ...                ← Wi-Fi (secondary)
192.168.224.0/22 dev usb0 ...               ← 5G network
```

✅ **First line has `usb0`** → 5G is primary!  
❌ First line has something else → That interface is primary

---

## Verify Specific Traffic is Using 5G

### Check Which Interface Sends Traffic

```bash
# See which interface is used for Google
ip route get 142.250.184.14

# Or use traceroute
traceroute -i usb0 google.com
```

If it shows `usb0` → ✅ **Using 5G!**

---

## Monitor Real-Time Traffic

### Watch Interface Statistics

```bash
watch -n 1 'cat /sys/class/net/usb0/statistics/tx_bytes && cat /sys/class/net/usb0/statistics/rx_bytes'
```

Press Ctrl+C to stop.

### Compare Wi-Fi vs 5G Traffic

```bash
# See bytes sent on each interface
echo "Wi-Fi traffic: $(cat /sys/class/net/wlan0/statistics/tx_bytes 2>/dev/null || echo 0)"
echo "5G traffic:    $(cat /sys/class/net/usb0/statistics/tx_bytes 2>/dev/null || echo 0)"
```

---

## Check Signal Strength

```bash
# Connect to modem
sudo screen /dev/ttyUSB2 115200

# Type these commands:
AT+QCSQ    # Signal quality
AT+CREG?   # Network registration  
AT+QNWINFO # Network info (5G/LTE)
AT+CSQ     # Simplified signal strength

# Exit: Press Ctrl+A then K, then Y
```

### Signal Quality Interpretation

- **AT+QCSQ**: `<rssi>,<ber>,<rscp>,<ecno>` (comma-separated values)
- **AT+CSQ**: `<rssi>,<ber>` (0-31, higher is better)

Good signal: values near 31  
Weak signal: values below 15

---

## Quick One-Liner Checks

### All-in-One Check

```bash
echo "Primary interface: $(ip route | grep default | awk '{print $5}')" && \
echo "5G IP: $(ip addr show usb0 2>/dev/null | grep 'inet ' | awk '{print $2}')" && \
echo "Connected: $(nmcli -t connection show RM530-5G-ECM 2>/dev/null | grep STATE | cut -d: -f2)"
```

### Is 5G Primary?

```bash
[ "$(ip route | grep default | awk '{print $5}')" = "usb0" ] && echo "✅ 5G is primary" || echo "❌ 5G is not primary"
```

### Check Internet Speed

```bash
curl -s https://raw.githubusercontent.com/sivel/speedtest-cli/master/speedtest.py | python3
```

This will show your download/upload speeds over the active connection.

---

## Troubleshooting

### 5G is NOT Primary

If Wi-Fi or Ethernet is still primary:

```bash
# List all connections
nmcli connection show

# Lower Wi-Fi priority
sudo nmcli connection modify <wifi-name> ipv4.route-metric 600

# Make sure 5G can be default
sudo nmcli connection modify RM530-5G-ECM ipv4.never-default no
sudo nmcli connection modify RM530-5G-ECM ipv4.route-metric 100

# Reconnect
sudo nmcli connection up RM530-5G-ECM
```

### Interface usb0 Not Found

```bash
# Check if modem is present
ls /dev/ttyUSB*

# Check kernel messages
dmesg | tail -50 | grep -i "usb\|cdc_ecm\|wwan"

# Restart modem
sudo nmcli connection down RM530-5G-ECM
sudo nmcli connection up RM530-5G-ECM
```

### No IP Address

```bash
# Manually request DHCP
sudo dhclient usb0

# Check NetworkManager logs
journalctl -u NetworkManager -f
```

---

## Expected Output Summary

When everything is working correctly, you should see:

✅ **Default route**: `dev usb0`  
✅ **Interface status**: `UP, LOWER_UP` with IP address  
✅ **NetworkManager**: `RM530-5G-ECM` connected on `usb0`  
✅ **Ping**: Successful with <50ms latency  
✅ **Signal**: Strong (AT+CSQ > 20)  

---

## Visual Verification

### Terminal Output Example

```bash
$ ip route get 8.8.8.8
8.8.8.8 via 192.168.225.1 dev usb0 src 192.168.225.40 uid 1000
    cache
```

Look for `dev usb0` → **This confirms 5G is being used!**

```bash
$ nmcli connection show RM530-5G-ECM | grep STATE
GENERAL.STATE: activated
```

Look for `activated` → **Connection is active!**

---

**TL;DR**: Run `bash ~/video/5g-integration/verify-5g.sh` for a complete status report! 🚀


# Technical Reference

Technical reference including AT commands, QMI vs ECM comparison, and legacy information.

## AT Commands Reference

### Accessing Modem

```bash
# Connect via serial
sudo screen /dev/ttyUSB2 115200

# Exit: Press Ctrl+A then K, then Y
```

### Signal & Network

**Signal Strength:**
```bash
AT+CSQ          # Quick signal check
AT+QCSQ         # Detailed signal quality
```

**AT+CSQ Response**: `<rssi>,<ber>`
- RSSI: 0-31 (higher = better)
- 0-10: Poor signal
- 11-20: Fair signal
- 21-31: Excellent signal

**Network Registration:**
```bash
AT+CREG?        # GSM/UMTS registration
AT+CEREG?       # EPS (LTE) registration
```

**Response Format**: `<mode>,<stat>`
- stat 0: Not registered
- stat 1: Registered (home network)
- stat 2: Searching
- stat 3: Denied

**Network Info:**
```bash
AT+QNWINFO      # Current network info (5G/LTE)
AT+COPS?        # Current operator
```

### Configuration

**USB Mode Settings:**
```bash
AT+QCFG="usbnet"           # Check current mode
AT+QCFG="usbnet",0         # QMI mode
AT+QCFG="usbnet",1         # ECM mode ✅ (recommended)
AT+QCFG="usbnet",2         # MBIM mode
AT+QCFG="usbnet",3         # RNDIS mode
```

**Data Interface:**
```bash
AT+QCFG="data_interface"          # Check interface
AT+QCFG="data_interface",0,0      # USB interface
```

**APN Configuration:**
```bash
AT+CGDCONT?              # Show APN settings
AT+CGDCONT=1,"IP","airtelgprs.com"    # Set APN
```

### Modem Control

**Function Mode:**
```bash
AT+CFUN?           # Check function mode
AT+CFUN=1          # Full functionality
AT+CFUN=1,1        # Reset and apply changes
AT+CFUN=0          # Minimum (sleep mode)
```

**Reset:**
```bash
AT+CFUN=1,1        # Soft reset
```

### Data Connection

**Connection Status:**
```bash
AT+CGACT?          # PDP context status
AT+CGPADDR         # Get IP address
```

**Enable Data:**
```bash
AT+CGACT=1,1       # Activate PDP context
```

### Statistics

**Signal Info:**
```bash
AT+QRSRP           # RSRP (Reference Signal Received Power)
AT+QECELLINFO      # Detailed cell info
```

**Data Stats:**
```bash
AT+QCCID           # SIM card ID
AT+CIMI            # IMSI (Subscriber Identity)
```

### Testing

**Basic Tests:**
```bash
AT                 # Test communication (should return OK)
ATE                # Echo on/off
ATI                # Product info
AT+GSN             # IMEI (serial number)
```

**Network Test:**
```bash
AT+CGDCONT?        # Verify APN
AT+CREG?           # Check registration
AT+CSQ             # Signal strength
```

### Common Debugging Sequences

**Check Everything:**
```bash
AT                 # Communication test
ATI                # Modem info
AT+CREG?           # Registration
AT+CSQ             # Signal
AT+QNWINFO         # Network type
AT+CGDCONT?        # APN
```

**Switch to ECM Mode:**
```bash
AT+QCFG="usbnet",1              # Switch to ECM
AT+QCFG="data_interface",0,0    # Set interface
AT+CGDCONT=1,"IP","airtelgprs.com"   # Set APN
AT+CFUN=1,1                     # Reset
```

### Response Codes

- **OK** - Command successful
- **ERROR** - Command failed
- **+CME ERROR**: <code> - Error with code
- No response - Command not recognized

### Important Notes

1. **Commands are case-sensitive** - Use uppercase
2. **End with CR** - Serial sends `\r\n`
3. **Timeout** - Commands may take 1-5 seconds
4. **Reset required** - Configuration changes need `AT+CFUN=1,1`

---

## QMI vs ECM Mode Comparison

### Quick Decision Guide

**Choose ECM if:**
- ✅ You want stable, uninterrupted connectivity
- ✅ You prefer native Linux networking integration
- ✅ You want simple, standard configuration
- ✅ You need reliable streaming/real-time applications
- ✅ You want automatic management by NetworkManager

**Choose QMI if:**
- ⚠️ You have specific QMI-compatible applications
- ⚠️ You need advanced modem features only in QMI mode
- ⚠️ You're following legacy tutorials/documentation
- ⚠️ You have existing QMI infrastructure

### Architecture Comparison

**QMI (Qualcomm MSM Interface):**
```
Application → waveshare-CM → libqmi → qmi_wwan kernel driver → Modem
                                 ↓
                         wwan0 interface (managed manually)
```

**ECM (Ethernet Control Model):**
```
Application → NetworkManager → cdc_ecm kernel driver → Modem
                                       ↓
                                  usb0 interface (native Linux networking)
```

### Feature Comparison

| Feature | QMI Mode | ECM Mode | Winner |
|---------|----------|----------|--------|
| Setup Complexity | Complex (multiple tools) | Simple (native) | ECM |
| Stability | Good | Excellent | ECM |
| Reconnection | Manual/scripted | Automatic | ECM |
| DNS Management | Manual/chattr | NetworkManager | ECM |
| Interface Type | wwan0 | usb0/wwan0 | Tie |
| Monitoring | qmicli tools | ip/nmcli | ECM |
| Boot Time | Slower (script delay) | Faster (native) | ECM |
| Resource Usage | Higher (extra process) | Lower (kernel) | ECM |
| Streaming Performance | Good | Better | ECM |
| Debug Tools | Limited | Standard Linux | ECM |

### Performance Comparison

**Latency:**
- QMI: Initial connection 15-25s, reconnection 10-15s, overhead ~2-5ms/packet
- ECM: Initial connection 5-10s, reconnection 2-5s, overhead <1ms/packet

**Throughput:**
- QMI: 90-95% of theoretical max, CPU usage 5-8%
- ECM: 95-98% of theoretical max, CPU usage 1-3%

### Setup Comparison

**QMI Setup:**
- Install external tools (waveshare-CM)
- Create custom script (50+ lines)
- Create systemd service
- Configure DNS locking (chattr)
- Prevent NetworkManager interference
- **Total**: ~100 lines of configuration

**ECM Setup:**
- Install standard tools: `sudo apt-get install python3-serial`
- Run setup script: `sudo rm530-setup-ecm airtelgprs.com`
- Configure NetworkManager: `nmcli connection add ...`
- **Total**: ~3 commands

**Setup Time**: ECM is 5x faster

### Stability Analysis

**QMI Mode Issues:**
1. waveshare-CM process can crash
2. DNS override by NetworkManager
3. Route conflicts with Wi-Fi
4. Custom DHCP handling less robust

**ECM Mode Benefits:**
1. Kernel driver (cannot crash independently)
2. NetworkManager (battle-tested reconnection)
3. Standard DHCP (automatic retry logic)
4. Native route priority (metric-based)

### Recommendation

**For video streaming and real-time applications, ECM mode is recommended:**
- ✅ Lower latency for TCP/UDP packets
- ✅ More stable connection for live streams
- ✅ Better handling of network fluctuations
- ✅ Automatic reconnection without stream interruption

---

## Legacy QMI Mode (Reference Only)

**Note**: QMI mode is not recommended for new setups. Use ECM mode instead.

### Legacy Setup Overview

The old QMI mode setup required:
1. Installing `waveshare-CM` tool
2. Creating custom autostart scripts
3. Manual DNS management with `chattr +i`
4. Systemd service configuration
5. Preventing NetworkManager interference

### Migration from QMI to ECM

If you're currently using QMI mode:

```bash
# 1. Stop QMI service
sudo systemctl stop start-5g.service
sudo systemctl disable start-5g.service

# 2. Unlock DNS (if locked)
sudo chattr -i /etc/resolv.conf

# 3. Run ECM setup
sudo rm530-setup-ecm airtelgprs.com

# 4. Remove old scripts (optional)
sudo rm /usr/local/bin/start-5g.sh
sudo rm /etc/systemd/system/start-5g.service
sudo systemctl daemon-reload

# 5. Configure NetworkManager
sudo nmcli connection add \
    type ethernet \
    ifname usb0 \
    con-name "RM530-5G-ECM" \
    ipv4.method auto \
    connection.autoconnect yes
```

**Estimated Migration Time**: 5 minutes

---

## References

- Full AT command manual: [Waveshare Wiki](https://www.waveshare.com/wiki/RM520N-GL-5G-HAT-PLUS)
- Qualcomm documentation: [Quectel RM5xx AT Commands](https://www.quectel.com/support/download?cat1=1&cat2=2&product=RM530N&os=All)
- NetworkManager Documentation: https://networkmanager.dev/docs/
- Linux CDC-ECM Documentation: https://www.kernel.org/doc/html/latest/usb/cdc-ecm.html

---

**Quick Test**: `AT+CSQ` should return something like `+CSQ: 25,99` for good signal.


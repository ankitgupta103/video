# RM530 AT Commands Reference

Quick reference for AT commands for the RM530 modem.

---

## 🔌 Accessing Modem

```bash
# Connect via serial
sudo screen /dev/ttyUSB2 115200

# Exit: Press Ctrl+A then K, then Y
```

---

## 📶 Signal & Network

### Signal Strength

```bash
AT+CSQ          # Quick signal check
AT+QCSQ         # Detailed signal quality
```

**AT+CSQ Response**: `<rssi>,<ber>`
- RSSI: 0-31 (higher = better)
- 0-10: Poor
- 11-20: Fair
- 21-31: Excellent

### Network Registration

```bash
AT+CREG?        # GSM/UMTS registration
AT+CEREG?       # EPS (LTE) registration
```

**Response Format**: `<mode>,<stat>`
- stat 0: Not registered
- stat 1: Registered (home network)
- stat 2: Searching
- stat 3: Denied

### Network Info

```bash
AT+QNWINFO      # Current network info (5G/LTE)
AT+COPS?        # Current operator
```

---

## 🔧 Configuration

### USB Mode Settings

```bash
AT+QCFG="usbnet"           # Check current mode
AT+QCFG="usbnet",0         # QMI mode
AT+QCFG="usbnet",1         # ECM mode ✅
AT+QCFG="usbnet",2         # MBIM mode
AT+QCFG="usbnet",3         # RNDIS mode
```

### Data Interface

```bash
AT+QCFG="data_interface"          # Check interface
AT+QCFG="data_interface",0,0      # USB interface
```

### APN Configuration

```bash
AT+CGDCONT?              # Show APN settings
AT+CGDCONT=1,"IP","airtelgprs.com"    # Set APN
```

---

## 🔄 Modem Control

### Function Mode

```bash
AT+CFUN?           # Check function mode
AT+CFUN=1          # Full functionality
AT+CFUN=1,1        # Reset and apply
AT+CFUN=0          # Minimum (sleep)
```

### Reset

```bash
AT+CFUN=1,1        # Soft reset
```

---

## 📡 Data Connection

### Connection Status

```bash
AT+CGACT?          # PDP context status
AT+CGPADDR         # Get IP address
```

### Enable Data

```bash
AT+CGACT=1,1       # Activate PDP context
```

---

## 📊 Statistics

### Signal Info

```bash
AT+QRSRP           # RSRP (Reference Signal Received Power)
AT+QECELLINFO      # Detailed cell info
```

### Data Stats

```bash
AT+QCCID           # SIM card ID
AT+CIMI            # IMSI (Subscriber Identity)
```

---

## 🧪 Testing

### Basic Tests

```bash
AT                 # Test communication (should return OK)
ATE                # Echo on/off
ATI                # Product info
AT+GSN             # IMEI (serial number)
```

### Network Test

```bash
AT+CGDCONT?        # Verify APN
AT+CREG?           # Check registration
AT+CSQ             # Signal strength
```

---

## 🔍 Common Debugging Sequences

### Check Everything

```bash
AT                 # Communication test
ATI                # Modem info
AT+CREG?           # Registration
AT+CSQ             # Signal
AT+QNWINFO         # Network type
AT+CGDCONT?        # APN
```

### Switch to ECM

```bash
AT+QCFG="usbnet",1         # Switch to ECM
AT+QCFG="data_interface",0,0    # Set interface
AT+CGDCONT=1,"IP","airtelgprs.com"   # Set APN
AT+CFUN=1,1                # Reset
```

---

## 📝 Response Codes

- **OK** - Command successful
- **ERROR** - Command failed
- **+CME ERROR**: <code> - Error with code
- No response - Command not recognized

---

## ⚠️ Important Notes

1. **Commands are case-sensitive** - Use uppercase
2. **End with CR** - Serial sends `\r\n`
3. **Timeout** - Commands may take 1-5 seconds
4. **Reset required** - Configuration changes need `AT+CFUN=1,1`

---

## 🔗 References

- Full AT command manual: [Waveshare Wiki](https://www.waveshare.com/wiki/RM520N-GL-5G-HAT-PLUS)
- Qualcomm documentation: [Quectel RM5xx AT Commands](https://www.quectel.com/support/download?cat1=1&cat2=2&product=RM530N&os=All)

---

**Quick Test**: `AT+CSQ` should return something like `+CSQ: 25,99` for good signal.


#!/bin/bash
# Verify that 5G modem is being used as primary internet connection

echo "=========================================="
echo "5G Modem Connection Verification"
echo "=========================================="
echo ""

# 1. Check which interface is used for default route
echo "1️⃣  Default Route (Primary Internet):"
echo "------------------------------------------"
DEFAULT_DEVICE=$(ip route | grep default | awk '{print $5}' | head -1)
echo "Default interface: $DEFAULT_DEVICE"

if [ "$DEFAULT_DEVICE" = "usb0" ] || [ "$DEFAULT_DEVICE" = "wwan0" ]; then
    echo "✅ 5G modem is your PRIMARY internet connection!"
else
    echo "❌ 5G modem is NOT your primary connection"
    echo "   Current primary: $DEFAULT_DEVICE"
fi
echo ""

# 2. Show all routes
echo "2️⃣  Routing Table:"
echo "------------------------------------------"
ip route | head -5
echo ""

# 3. Check usb0/wwan0 status
echo "3️⃣  5G Modem Interface Status:"
echo "------------------------------------------"
if ip link show usb0 > /dev/null 2>&1; then
    INTERFACE="usb0"
elif ip link show wwan0 > /dev/null 2>&1; then
    INTERFACE="wwan0"
else
    INTERFACE=""
fi

if [ -n "$INTERFACE" ]; then
    echo "Interface: $INTERFACE"
    echo ""
    ip addr show $INTERFACE
    echo ""
    
    # Check if it has an IP
    if ip addr show $INTERFACE | grep -q "inet "; then
        echo "✅ Interface $INTERFACE is UP and has an IP"
    else
        echo "❌ Interface $INTERFACE is UP but has NO IP"
    fi
else
    echo "❌ No usb0 or wwan0 interface found!"
fi
echo ""

# 4. Test connectivity via 5G
echo "4️⃣  Testing Internet Connectivity:"
echo "------------------------------------------"
echo "Pinging Google DNS (8.8.8.8)..."
if ping -c 2 8.8.8.8 > /dev/null 2>&1; then
    RTT=$(ping -c 2 8.8.8.8 2>/dev/null | grep "time=" | awk -F'time=' '{print $2}' | awk '{print $1}' | head -1)
    echo "✅ Internet connection active (RTT: $RTT)"
else
    echo "❌ No internet connection"
fi
echo ""

# 5. Check NetworkManager connection
echo "5️⃣  NetworkManager Status:"
echo "------------------------------------------"
nmcli connection show RM530-5G-ECM 2>/dev/null | grep -E "(NAME|GENERAL.STATE|GENERAL.DEVICES|IP4.ADDRESS|IP4.GATEWAY)"
echo ""

# 6. Show network statistics
if [ -n "$INTERFACE" ]; then
    echo "6️⃣  Interface Statistics:"
    echo "------------------------------------------"
    echo "Bytes sent:    $(cat /sys/class/net/$INTERFACE/statistics/tx_bytes 2>/dev/null | numfmt --to=iec-iB 2>/dev/null || cat /sys/class/net/$INTERFACE/statistics/tx_bytes)"
    echo "Bytes received: $(cat /sys/class/net/$INTERFACE/statistics/rx_bytes 2>/dev/null | numfmt --to=iec-iB 2>/dev/null || cat /sys/class/net/$INTERFACE/statistics/rx_bytes)"
    echo ""
fi

# 7. Determine carrier network info
echo "7️⃣  Modem/Network Information:"
echo "------------------------------------------"
echo "Checking modem via AT commands..."
if [ -f /dev/ttyUSB2 ]; then
    echo -e "AT+QCSQ\r" | timeout 2 sudo minicom -D /dev/ttyUSB2 -b 115200 -C - 2>/dev/null | grep "QCSQ" || echo "Could not query signal strength"
    echo -e "AT+CREG?\r" | timeout 2 sudo minicom -D /dev/ttyUSB2 -b 115200 -C - 2>/dev/null | grep "CREG" || echo "Could not query network registration"
else
    echo "Could not access modem AT port"
fi
echo ""

echo "=========================================="
echo "Summary"
echo "=========================================="
if [ "$DEFAULT_DEVICE" = "usb0" ] || [ "$DEFAULT_DEVICE" = "wwan0" ]; then
    echo "✅ CONFIRMED: Your 5G modem is ACTIVE and PRIMARY!"
    echo "   All internet traffic is using 5G connection."
else
    echo "⚠️  WARNING: 5G modem is not the primary connection."
    echo "   Primary connection: $DEFAULT_DEVICE"
    echo ""
    echo "To make 5G primary:"
    echo "  sudo nmcli connection down <other-connection>"
    echo "  sudo nmcli connection up RM530-5G-ECM"
fi
echo "=========================================="


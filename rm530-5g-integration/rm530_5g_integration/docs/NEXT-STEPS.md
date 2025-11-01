# Next Steps After Running setup-ecm-mode.py

Follow these commands **on your Raspberry Pi** to complete the ECM setup:

## Step 1: Wait for Modem to Restart (15 seconds)

```bash
echo "Waiting for modem to restart..."
sleep 15
```

## Step 2: Check for New Network Interface

```bash
ip link show
```

Look for a new interface like `wwan0` or `usb0`. Write down the name!

## Step 3: Configure NetworkManager

**Replace `wwan0` with your actual interface name** from Step 2:

```bash
sudo nmcli connection add \
    type ethernet \
    ifname wwan0 \
    con-name "RM530-5G-ECM" \
    ipv4.method auto \
    ipv4.never-default no \
    ipv4.route-metric 100 \
    ipv4.dns "8.8.8.8 1.1.1.1" \
    connection.autoconnect yes
```

## Step 4: Connect to 5G

```bash
sudo nmcli connection up RM530-5G-ECM
```

## Step 5: Verify it Worked

```bash
# Check if interface has an IP
ip addr show wwan0

# Check routing
ip route

# Test internet
ping -c 4 8.8.8.8
ping -c 4 google.com
```

## Step 6: Make 5G Default Route (Important!)

Check your current route and ensure 5G is default:

```bash
ip route | head -5
```

You should see something like:
```
default via 192.168.x.1 dev wwan0
```

## Step 7: Lower Priority for Other Connections (Optional)

To ensure 5G is always primary over Wi-Fi:

```bash
# See all connections
nmcli connection show

# Set Wi-Fi to lower priority (replace 'Wifi-Name' with your actual connection)
sudo nmcli connection modify "Wifi-Name" ipv4.route-metric 600
sudo nmcli connection modify "Wifi-Name" ipv4.never-default yes
```

---

## Troubleshooting

### Interface Not Found

If you don't see a new interface after 15 seconds:

```bash
# Check if modem is resetting
ls -la /dev/ttyUSB*

# Check kernel messages
dmesg | tail -30

# Try waiting longer
sleep 10
ip link show
```

### Can't Connect

```bash
# Check connection status
nmcli connection show RM530-5G-ECM

# Check for errors
sudo journalctl -u NetworkManager -n 50

# Try manual DHCP
sudo dhclient wwan0
```

### No Internet

```bash
# Check DNS
cat /etc/resolv.conf

# Check if modem is registered
sudo screen /dev/ttyUSB2 115200
# Type: AT+CREG?
# Should show: 0,1 (registered on home network)
# Press Ctrl+A then K to exit
```

---

## Success!

If `ping google.com` works, you're all set! Your 5G modem is now:

✅ Running in ECM mode  
✅ Managed by NetworkManager  
✅ Connected to internet  
✅ Ready for streaming  

Your integration is complete! 🎉


# RM530 5G Modem Integration Guide

## Overview

Configure the **Waveshare RM530 5G modem** to automatically connect at boot, set as the default internet route, and configure DNS correctly—while preventing Wi-Fi or Ethernet from overriding the 5G connection.

**Goal**: Ensure all internet traffic routes through the 5G modem with stable DNS configuration.

---

## Prerequisites

- Raspberry Pi with Waveshare RM530 5G modem connected
- Root/sudo access
- Internet connectivity for initial setup

---

## Step 1: Install Waveshare 5G Tools

Install `waveshare-CM` to manage the modem connection in QMI mode:

```bash
sudo wget -O - https://files.waveshare.com/wiki/PCIe-TO-4G-5G-M.2-USB3.2-HAT-Plus/install.sh | sudo bash
```

**Why**: Automates dialing, IP setup, and modem configuration without NetworkManager interference.

---

## Step 2: Test the Modem Manually

Verify the modem is detected:

```bash
ip link show wwan0
```

Start the connection manually:

```bash
sudo waveshare-CM -s airtelgprs.com
```

Verify it gets an IP and has connectivity:

```bash
ip addr show wwan0
ping -c 4 8.8.8.8
```

**Why**: Ensures the modem works correctly before automation.

---

## Step 3: Create Autostart Script

Create the script at `/usr/local/bin/start-5g.sh`:

```bash
#!/bin/bash
# Waveshare RM530 5G autostart

# Wait for USB modem
for i in {1..20}; do
    if ip link show wwan0 &>/dev/null; then
        echo "wwan0 detected"
        break
    fi
    sleep 2
done

# Start 5G connection
sudo /usr/local/bin/waveshare-CM -s airtelgprs.com

# Wait until wwan0 has an IP
for i in {1..15}; do
    IP=$(ip -4 addr show wwan0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}')
    if [[ -n "$IP" ]]; then
        echo "wwan0 IP: $IP"
        break
    fi
    sleep 2
done

# Set default route via wwan0
sudo ip route replace default dev wwan0

# Apply static DNS
sudo chattr -i /etc/resolv.conf 2>/dev/null
echo -e "nameserver 8.8.8.8\nnameserver 1.1.1.1" | sudo tee /etc/resolv.conf >/dev/null
sudo chattr +i /etc/resolv.conf

# Ensure Wi-Fi does not override default route
sudo nmcli connection modify "Airtel_anki_3363_5g" ipv4.never-default yes ipv4.route-metric 600
```

**What it does**:
- Waits for modem detection (up to 40 seconds)
- Connects via waveshare-CM
- Waits for IP assignment
- Sets wwan0 as default route
- Locks DNS configuration to prevent NetworkManager from changing it
- Prevents Wi-Fi from becoming the default route

---

## Step 4: Make Script Executable

```bash
sudo chmod +x /usr/local/bin/start-5g.sh
```

---

## Step 5: Create Systemd Service

Create the service file at `/etc/systemd/system/start-5g.service`:

```ini
[Unit]
Description=Auto start Waveshare RM530 5G modem
After=network.target
Wants=network.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/start-5g.sh
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```

Reload systemd and enable the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable start-5g.service
sudo systemctl start start-5g.service
```

**Why**: Ensures the 5G modem connects at boot before NetworkManager interferes.

---

## Step 6: Verify Routing and DNS

Check the default route:

```bash
ip route
```

**Expected output**:
```
default via <5G_gateway> dev wwan0
```

Check DNS configuration:

```bash
cat /etc/resolv.conf
```

**Expected output**:
```
nameserver 8.8.8.8
nameserver 1.1.1.1
```

Test internet connectivity:

```bash
ping -c 4 google.com
```

---

## Notes and Tips

- **DNS Protection**: `chattr +i /etc/resolv.conf` makes the file immutable, preventing NetworkManager from overwriting DNS settings
- **Wi-Fi Behavior**: Wi-Fi remains connected but won't become the default route
- **Testing**: Always test the script manually (`sudo /usr/local/bin/start-5g.sh`) before relying on the service
- **Debugging**: Use `journalctl -u start-5g.service -f` to monitor service logs and debug boot-time issues
- **APN Configuration**: Update `airtelgprs.com` with your carrier's APN as needed

---

## Expected Result

On every reboot, the Raspberry Pi will:
- ✅ Automatically connect to the 5G modem
- ✅ Use 5G for all internet traffic (even if Wi-Fi is connected)
- ✅ Maintain stable DNS configuration (8.8.8.8 and 1.1.1.1)
- ✅ Prevent NetworkManager from interfering with routing or DNS
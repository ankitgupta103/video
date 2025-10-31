#!/bin/bash
# Quick NetworkManager configuration for RM530 ECM mode

echo "=========================================="
echo "Configuring NetworkManager for RM530-5G"
echo "=========================================="

# Step 1: Create connection profile
echo ""
echo "Creating NetworkManager connection..."
sudo nmcli connection add \
    type ethernet \
    ifname usb0 \
    con-name "RM530-5G-ECM" \
    ipv4.method auto \
    ipv4.never-default no \
    ipv4.route-metric 100 \
    ipv4.dns "8.8.8.8 1.1.1.1" \
    connection.autoconnect yes

echo "✓ Connection profile created: RM530-5G-ECM"

# Step 2: Connect
echo ""
echo "Activating connection..."
sudo nmcli connection up RM530-5G-ECM

# Step 3: Wait for IP assignment
echo ""
echo "Waiting for IP assignment..."
sleep 5

# Step 4: Show status
echo ""
echo "=========================================="
echo "Interface Status:"
echo "=========================================="
ip addr show usb0

echo ""
echo "=========================================="
echo "Routing Table:"
echo "=========================================="
ip route | head -10

echo ""
echo "=========================================="
echo "Testing Connectivity:"
echo "=========================================="
ping -c 3 8.8.8.8
ping -c 3 google.com

echo ""
echo "=========================================="
echo "Configuration complete!"
echo "=========================================="
echo ""
echo "If you see successful pings, your 5G modem is connected!"
echo "Your interface is: usb0"


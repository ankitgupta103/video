#!/usr/bin/env python3
"""
RM530 5G Modem - ECM Mode Setup Script

This script switches the Qualcomm RM530 modem from QMI to ECM mode
and optionally sets the APN for automatic connection.
"""

import serial
import time
import sys
import glob
import os

# Configuration
APN = "airtelgprs.com"  # Change this to your carrier's APN
AT_BAUDRATE = 115200
TIMEOUT = 2


def find_modem_serial():
    """
    Find the Qualcomm modem's AT command port.
    Typically /dev/ttyUSB2 or /dev/ttyUSB3
    """
    # List all ttyUSB devices
    ports = glob.glob('/dev/ttyUSB*')
    
    for port in sorted(ports):
        try:
            # Try to open and send AT command
            ser = serial.Serial(port, AT_BAUDRATE, timeout=TIMEOUT)
            ser.write(b'AT\r\n')
            time.sleep(0.5)
            response = ser.read(100).decode('utf-8', errors='ignore')
            ser.close()
            
            if 'OK' in response:
                print(f"✓ Found modem at: {port}")
                return port
        except (serial.SerialException, PermissionError) as e:
            continue
    
    return None


def send_at_command(ser, command, expected="OK", timeout=5):
    """
    Send AT command and wait for expected response.
    Returns True on success, False otherwise.
    """
    try:
        # Send command
        ser.write(f"{command}\r\n".encode())
        time.sleep(0.5)
        
        # Read response with timeout
        start_time = time.time()
        response = b''
        while time.time() - start_time < timeout:
            if ser.in_waiting:
                response += ser.read(ser.in_waiting)
                if b'\r\n' in response:
                    break
            time.sleep(0.1)
        
        response_str = response.decode('utf-8', errors='ignore')
        print(f"  Command: {command}")
        print(f"  Response: {response_str.strip()}")
        
        if expected in response_str:
            return True
        return False
        
    except Exception as e:
        print(f"  Error: {e}")
        return False


def switch_to_ecm_mode(apn=None):
    """
    Switch modem to ECM mode and optionally set APN.
    """
    # Find modem port
    port = find_modem_serial()
    if not port:
        print("✗ Could not find modem serial port")
        return False
    
    try:
        # Open serial connection
        print(f"\nOpening connection to {port}...")
        ser = serial.Serial(port, AT_BAUDRATE, timeout=TIMEOUT)
        time.sleep(1)
        
        # Test communication
        print("\n1. Testing modem communication...")
        if not send_at_command(ser, "AT"):
            print("✗ No response from modem")
            ser.close()
            return False
        
        # Get current USB net mode
        print("\n2. Checking current USB mode...")
        if ser.in_waiting:
            ser.read(ser.in_waiting)  # Clear buffer
        ser.write(b"AT+QCFG=\"usbnet\"\r\n")
        time.sleep(1)
        response = ser.read(100).decode('utf-8', errors='ignore')
        print(f"  Current mode: {response.strip()}")
        
        # Switch to ECM mode
        print("\n3. Switching to ECM mode...")
        if not send_at_command(ser, 'AT+QCFG="usbnet",1'):
            print("✗ Failed to set ECM mode")
            ser.close()
            return False
        
        # Configure data interface
        print("\n4. Configuring data interface...")
        send_at_command(ser, 'AT+QCFG="data_interface",0,0')
        
        # Set APN if provided
        if apn:
            print(f"\n5. Setting APN to: {apn}")
            send_at_command(ser, f'AT+CGDCONT=1,"IP","{apn}"')
        
        # Apply settings (soft reset)
        print("\n6. Applying settings...")
        send_at_command(ser, "AT+CFUN=1,1", expected="", timeout=10)
        
        # Close connection
        ser.close()
        print("\n✓ ECM mode configuration complete!")
        print("  Modem will reset and restart in ECM mode.")
        print("  Wait 10-15 seconds for modem to restart...")
        
        return True
        
    except serial.SerialException as e:
        print(f"✗ Serial error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


def main():
    """
    Main entry point.
    """
    print("=" * 60)
    print("RM530 5G Modem - ECM Mode Configuration")
    print("=" * 60)
    
    # Check if running as root
    if os.geteuid() != 0:
        print("\n✗ This script must be run as root (sudo)")
        sys.exit(1)
    
    # Get APN from command line or use default
    apn = None
    if len(sys.argv) > 1:
        apn = sys.argv[1]
    else:
        # Ask user for APN
        print(f"\nDefault APN: {APN}")
        user_apn = input("Enter your APN (or press Enter to use default): ").strip()
        if user_apn:
            apn = user_apn
        else:
            apn = APN
    
    # Switch to ECM mode
    success = switch_to_ecm_mode(apn=apn)
    
    if success:
        print("\n" + "=" * 60)
        print("Setup complete!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Wait 15 seconds for modem to restart")
        print("2. Check interface: ip link show")
        print("3. Configure NetworkManager with:")
        print("   nmcli connection add type ethernet ifname <interface> \\")
        print("      con-name 'RM530-5G-ECM' ipv4.method auto \\")
        print("      connection.autoconnect yes")
        print("\nSee ecm-integration.md for complete setup instructions.")
    else:
        print("\n" + "=" * 60)
        print("Setup failed!")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()


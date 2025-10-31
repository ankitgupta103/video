# RM530 5G Modem Integration

Complete integration guide for Waveshare RM530 5G modem with Raspberry Pi using **ECM (Ethernet Control Model)**.

---

## 🚀 Quick Start (Already Done!)

Your modem is already integrated! Here's what happened:

1. ✅ Switched from QMI to ECM mode
2. ✅ Configured NetworkManager
3. ✅ Connected and verified

**See**: `docs/SETUP-COMPLETE.md` for details.

---

## 📁 Directory Structure

```
5g-integration/
├── README.md                    ← You are here!
├── README-INDEX.md              ← Quick file index
├── GETTING-STARTED.md           ← Navigation guide
│
├── scripts/                     ← Automation scripts
│   ├── setup-ecm-mode.py       ← Switch modem to ECM mode
│   ├── configure-network.sh    ← NetworkManager setup
│   └── verify-5g.sh            ← Verify 5G is active
│
├── docs/                        ← Complete documentation
│   ├── SETUP-COMPLETE.md       ← Success summary & tips
│   ├── ecm-integration.md      ← Full ECM setup guide
│   ├── verify-5g.md            ← How to verify connection
│   └── NEXT-STEPS.md           ← Quick reference
│
├── legacy/                      ← Old QMI mode docs (reference only)
│   ├── integration.md          ← QMI mode setup (don't use)
│   └── comparison-qmi-vs-ecm.md ← Why ECM is better
│
└── reference/                   ← Additional resources
    ├── AT-COMMANDS.md          ← AT command reference
    └── TROUBLESHOOTING.md       ← Troubleshooting guide
```

---

## 📖 Documentation Guide

### 🎯 **Start Here**

| File | When to Use |
|------|-------------|
| **README.md** | This file - main overview |
| **GETTING-STARTED.md** | Navigation guide & quick access |
| **README-INDEX.md** | Complete file index |
| **docs/SETUP-COMPLETE.md** | After successful setup |

### 📚 **Main Documentation**

| File | Purpose |
|------|---------|
| **docs/ecm-integration.md** | Complete ECM setup guide (manual) |
| **docs/verify-5g.md** | How to verify 5G is working |
| **docs/NEXT-STEPS.md** | Quick command reference |

### 🔧 **Scripts**

| File | Purpose | Run It When |
|------|---------|-------------|
| **scripts/setup-ecm-mode.py** | Switch modem to ECM | First time setup only |
| **scripts/configure-network.sh** | Setup NetworkManager | After ECM mode switch |
| **scripts/verify-5g.sh** | Verify 5G is active | Anytime to check status |

### 📜 **Legacy (Reference Only)**

| File | Purpose |
|------|---------|
| **legacy/integration.md** | Old QMI mode setup (don't use) |
| **legacy/comparison-qmi-vs-ecm.md** | Technical comparison |

### 📖 **Reference**

| File | Purpose |
|------|---------|
| **reference/AT-COMMANDS.md** | AT command reference |
| **reference/TROUBLESHOOTING.md** | Complete troubleshooting guide |

---

## 🎯 Common Tasks

### Verify 5G is Working

```bash
bash scripts/verify-5g.sh
```

Or check manually:

```bash
ip route | grep default | grep usb0  # Should show usb0
nmcli connection show --active        # Should show RM530-5G-ECM
ping -c 3 google.com                  # Should work
```

### Troubleshooting

```bash
# Check connection status
nmcli connection show RM530-5G-ECM

# View logs
journalctl -u NetworkManager -f

# Restart connection
sudo nmcli connection up RM530-5G-ECM
```

**Full troubleshooting**: See `reference/TROUBLESHOOTING.md`

### Check Signal Strength

```bash
sudo screen /dev/ttyUSB2 115200
# Type: AT+CSQ
# Exit: Ctrl+A then K
```

---

## 🔧 Re-running Setup

### If You Need to Start Over

```bash
# 1. Switch to ECM mode (if modem reset)
sudo python3 scripts/setup-ecm-mode.py airtelgprs.com

# 2. Configure NetworkManager
bash scripts/configure-network.sh

# 3. Verify
bash scripts/verify-5g.sh
```

### If Only NetworkManager Needs Reset

```bash
# Re-configure NetworkManager
bash scripts/configure-network.sh
```

---

## 📊 Current Status

**Mode**: ECM (Ethernet Control Model)  
**Interface**: usb0  
**Manager**: NetworkManager  
**Auto-connect**: Yes  
**Primary Route**: Yes  

**Configuration**: Production-ready ✅

---

## 🆚 ECM vs QMI

**Why ECM?**
- ✅ Native Linux integration
- ✅ More stable
- ✅ No custom scripts
- ✅ Standard tools
- ✅ Better performance

**Why NOT QMI?**
- ❌ Requires waveshare-CM
- ❌ More complex
- ❌ Can have interruptions
- ❌ Manual DNS management

**Details**: See `legacy/comparison-qmi-vs-ecm.md`

---

## 🔗 Quick Links

- **Setup Complete**: `docs/SETUP-COMPLETE.md`
- **Verify Connection**: `bash scripts/verify-5g.sh`
- **Troubleshooting**: `docs/ecm-integration.md` section "Troubleshooting"
- **Reference**: `README-INDEX.md`

---

## 📚 External Resources

- [Waveshare PCIe TO 4G/5G HAT+ Wiki](https://www.waveshare.com/wiki/PCIe-TO-4G-5G-M.2-USB3.2-HAT-PLUS)
- [RM530 AT Commands](https://www.waveshare.com/wiki/RM520N-GL-5G-HAT-PLUS)
- [NetworkManager Docs](https://networkmanager.dev/docs/)
- [Linux CDC-ECM](https://www.kernel.org/doc/html/latest/usb/cdc-ecm.html)

---

## 💡 Tips

1. **Always verify** after changes: `bash scripts/verify-5g.sh`
2. **Check signal** if connection is slow: `AT+CSQ` via ttyUSB2
3. **Monitor logs**: `journalctl -u NetworkManager -f`
4. **Keep scripts** executable: `chmod +x scripts/*.sh`

---

## 🎉 Success!

Your 5G modem is integrated and working. Happy streaming! 📹🚀


# File Index - Quick Reference

Quick reference to all files in this directory.

---

## 📄 Main Files

| File | Purpose | Read When |
|------|---------|-----------|
| **README.md** | Main overview and quick start | Always start here |
| **README-INDEX.md** | This file - file index | Finding files |

---

## 🔧 Scripts (`scripts/`)

| File | Purpose | Use Case |
|------|---------|----------|
| **setup-ecm-mode.py** | Switches modem from QMI to ECM | First-time setup |
| **configure-network.sh** | Configures NetworkManager | After ECM switch |
| **verify-5g.sh** | Verifies 5G is active | Any time |

**How to run**: `bash scripts/<filename>` or `python3 scripts/<filename>`

---

## 📚 Documentation (`docs/`)

| File | Purpose | Read When |
|------|---------|-----------|
| **SETUP-COMPLETE.md** | Setup success summary | After setup |
| **ecm-integration.md** | Complete ECM setup guide | Detailed setup |
| **verify-5g.md** | How to verify 5G is working | Troubleshooting |
| **NEXT-STEPS.md** | Quick command reference | Quick reference |

---

## 📜 Legacy (`legacy/`)

| File | Purpose | Read When |
|------|---------|-----------|
| **integration.md** | Old QMI mode setup | Reference only |
| **comparison-qmi-vs-ecm.md** | Technical comparison | Understanding differences |

**Note**: Do not use QMI mode anymore. ECM is better!

---

## 📂 Directory Quick Access

```bash
# View scripts
ls scripts/

# View documentation
ls docs/

# View legacy files
ls legacy/

# View reference
ls reference/
```

---

## 🎯 Common Scenarios

### "I want to verify my setup is working"
→ Read: `docs/verify-5g.md`  
→ Run: `bash scripts/verify-5g.sh`

### "I need to troubleshoot connection issues"
→ Read: `docs/ecm-integration.md` section "Troubleshooting"

### "I want to understand what we did"
→ Read: `docs/SETUP-COMPLETE.md`

### "I need to re-run setup"
→ Read: `docs/ecm-integration.md`  
→ Run: `python3 scripts/setup-ecm-mode.py`

### "What's the difference between QMI and ECM?"
→ Read: `legacy/comparison-qmi-vs-ecm.md`

### "I need quick commands"
→ Read: `docs/NEXT-STEPS.md`

---

## 📖 Reading Order

**For first-time users:**
1. README.md
2. docs/SETUP-COMPLETE.md
3. (Optional) docs/ecm-integration.md for details

**For troubleshooting:**
1. README.md
2. docs/verify-5g.md
3. docs/ecm-integration.md (Troubleshooting section)

**For understanding:**
1. README.md
2. legacy/comparison-qmi-vs-ecm.md
3. docs/ecm-integration.md

---

## 🔍 Finding Information

### By Topic

| Want to know about... | File |
|-----------------------|------|
| Setup overview | README.md |
| Switch to ECM | scripts/setup-ecm-mode.py |
| Configure network | scripts/configure-network.sh |
| Verify connection | scripts/verify-5g.sh |
| Detailed setup | docs/ecm-integration.md |
| Quick commands | docs/NEXT-STEPS.md |
| Troubleshooting | docs/ecm-integration.md |
| Why ECM vs QMI | legacy/comparison-qmi-vs-ecm.md |
| Success summary | docs/SETUP-COMPLETE.md |

### By File Type

**Scripts**: Everything in `scripts/`  
**Documentation**: Everything in `docs/`  
**Old/Reference**: Everything in `legacy/`  
**Quick start**: README.md  
**File index**: README-INDEX.md (this file)

---

## 🚀 Quick Commands

```bash
# Navigate to directory
cd ~/video/5g-integration

# View main README
cat README.md

# Run verification
bash scripts/verify-5g.sh

# View all files
tree -L 2

# Search for keywords
grep -r "keyword" docs/
```

---

Last updated: After successful ECM integration

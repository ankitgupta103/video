# Getting Started

Visual guide to navigating this directory.

---

## 🎯 Start Here

```
📁 5g-integration/
├── 📄 README.md                    ⭐ START HERE
│
├── 🔧 scripts/                     Automation tools
├── 📚 docs/                        Documentation
├── 📜 legacy/                      Old QMI docs (reference)
└── 📖 reference/                   Quick references
```

---

## 📖 Reading Path

### 🚀 For Quick Verification

```
README.md → bash scripts/verify-5g.sh → Done! ✅
```

### 📚 For Understanding Setup

```
README.md → docs/SETUP-COMPLETE.md → Done! ✅
```

### 🔧 For Troubleshooting

```
README.md → docs/verify-5g.md → reference/TROUBLESHOOTING.md
```

### 🎓 For Learning

```
README.md → legacy/comparison-qmi-vs-ecm.md → reference/AT-COMMANDS.md
```

---

## 📂 Directory Map

### 📄 Root Files

```
README.md          Main overview, quick start guide
README-INDEX.md    Complete file index
GETTING-STARTED.md This file - navigation guide
```

### 🔧 scripts/

**Purpose**: Executable automation scripts

```
setup-ecm-mode.py       Switch modem to ECM mode
configure-network.sh    Setup NetworkManager
verify-5g.sh           Verify 5G is active
```

**How to use**: `bash scripts/<name>.sh` or `python3 scripts/<name>.py`

### 📚 docs/

**Purpose**: Complete documentation

```
SETUP-COMPLETE.md      ✅ Your setup is done!
ecm-integration.md     Full setup guide
verify-5g.md          How to verify connection
NEXT-STEPS.md         Quick commands
```

**When to read**: After setup, for reference, for troubleshooting

### 📜 legacy/

**Purpose**: Old QMI mode documentation (for reference only)

```
integration.md            Old QMI setup (don't use anymore)
comparison-qmi-vs-ecm.md Why ECM is better than QMI
```

**When to read**: Understanding differences, historical reference

### 📖 reference/

**Purpose**: Quick lookup guides

```
AT-COMMANDS.md       AT command reference
TROUBLESHOOTING.md  Common problems & solutions
```

**When to read**: When you need specific information

---

## 🎯 By Task

### "I want to verify my 5G is working"

**Read**:
1. `docs/verify-5g.md`

**Run**:
```bash
bash scripts/verify-5g.sh
```

### "I need to troubleshoot"

**Read**:
1. `reference/TROUBLESHOOTING.md`
2. Relevant sections in `docs/ecm-integration.md`

**Run**:
```bash
bash scripts/verify-5g.sh
journalctl -u NetworkManager -f
```

### "I want to understand what we did"

**Read**:
1. `docs/SETUP-COMPLETE.md`
2. `legacy/comparison-qmi-vs-ecm.md`

### "I need AT commands"

**Read**:
1. `reference/AT-COMMANDS.md`

### "I want quick commands"

**Read**:
1. `docs/NEXT-STEPS.md`

### "I need to re-run setup"

**Read**:
1. `docs/ecm-integration.md`

**Run**:
```bash
python3 scripts/setup-ecm-mode.py airtelgprs.com
bash scripts/configure-network.sh
```

---

## 🔍 Finding Information

### Search Strategy

**By topic**:
- Setup → `docs/` and `scripts/`
- Troubleshooting → `reference/TROUBLESHOOTING.md`
- AT commands → `reference/AT-COMMANDS.md`
- Comparison → `legacy/comparison-qmi-vs-ecm.md`

**By file type**:
- Scripts → `scripts/`
- Documentation → `docs/`
- References → `reference/`
- Old docs → `legacy/`

**By urgency**:
- Quick check → `bash scripts/verify-5g.sh`
- Quick read → `README.md`
- Deep dive → `docs/ecm-integration.md`

---

## 📋 Quick Commands

```bash
# Navigate
cd ~/video/5g-integration

# Main README
cat README.md

# Verify everything
bash scripts/verify-5g.sh

# View structure
tree -L 2

# Search
grep -r "keyword" docs/

# Get help
cat reference/TROUBLESHOOTING.md | less
```

---

## 🎓 Learning Path

### Beginner

1. Read: `README.md`
2. Verify: `bash scripts/verify-5g.sh`
3. Understand: `docs/SETUP-COMPLETE.md`

### Intermediate

1. Read: `docs/ecm-integration.md`
2. Learn: `legacy/comparison-qmi-vs-ecm.md`
3. Practice: `reference/AT-COMMANDS.md`

### Advanced

1. Read: All files in `docs/` and `reference/`
2. Understand: `legacy/integration.md` (QMI)
3. Customize: Modify scripts as needed

---

## ✅ Success Checklist

After setup, you should be able to:

- [ ] Find the main README
- [ ] Run verification script
- [ ] Understand your setup
- [ ] Know where to find documentation
- [ ] Know how to troubleshoot
- [ ] Access AT command reference

---

## 🆘 Need Help?

**Quick help**:
1. Run: `bash scripts/verify-5g.sh`
2. Read: `reference/TROUBLESHOOTING.md`
3. Check: `docs/ecm-integration.md` Troubleshooting section

**Detailed help**:
1. Collect logs
2. Review all relevant docs
3. Check external resources in README.md

---

## 🎉 You're Ready!

You now know where everything is. Happy exploring! 🚀

**Remember**: When in doubt, start with `README.md` and `bash scripts/verify-5g.sh`


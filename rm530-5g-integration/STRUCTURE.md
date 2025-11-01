# Package Structure

Complete overview of the rm530-5g-integration package.

## Directory Tree

```
rm530-5g-integration/
├── .gitignore                 # Git ignore rules
├── .gitattributes            # Git attributes
├── LICENSE                   # MIT License
├── MANIFEST.in              # Package manifest
├── README.md                # Package README
├── PUBLISH.md               # Publishing instructions
├── STRUCTURE.md             # This file
├── pyproject.toml           # Modern Python packaging config
├── setup.py                 # Legacy setup.py for compatibility
│
└── rm530_5g_integration/    # Main package
    ├── __init__.py          # Package initialization
    │
    ├── docs/                # Documentation
    │   ├── SETUP-COMPLETE.md
    │   ├── ecm-integration.md
    │   ├── verify-5g.md
    │   └── NEXT-STEPS.md
    │
    ├── reference/           # Quick references
    │   ├── AT-COMMANDS.md
    │   └── TROUBLESHOOTING.md
    │
    ├── legacy/              # Legacy documentation
    │   ├── integration.md
    │   └── comparison-qmi-vs-ecm.md
    │
    └── scripts/             # Python scripts
        ├── __init__.py
        ├── setup_ecm.py         # ECM mode setup
        ├── configure_network.py # NetworkManager config
        └── verify.py            # Connection verification
```

## Package Files

### Root Files

| File | Purpose |
|------|---------|
| `README.md` | Main package documentation |
| `LICENSE` | MIT License |
| `pyproject.toml` | Modern packaging configuration |
| `setup.py` | Legacy compatibility |
| `MANIFEST.in` | Included files specification |
| `.gitignore` | Git ignore patterns |
| `.gitattributes` | Git line ending rules |
| `PUBLISH.md` | Publishing instructions |
| `STRUCTURE.md` | This file |

### Package Code

#### `rm530_5g_integration/__init__.py`
- Package initialization
- Version information
- Metadata export

#### Scripts Module

##### `scripts/setup_ecm.py`
**Purpose**: Switch modem from QMI to ECM mode

**Entry Point**: `rm530-setup-ecm`

**Functions**:
- `find_modem_serial()` - Find modem AT port
- `send_at_command()` - Send AT commands
- `switch_to_ecm_mode()` - Main ECM switch logic
- `check_modemmanager()` - Check for ModemManager
- `main()` - CLI entry point

**Usage**:
```bash
sudo rm530-setup-ecm airtelgprs.com
```

##### `scripts/configure_network.py`
**Purpose**: Configure NetworkManager (TODO)

**Entry Point**: `rm530-configure-network`

##### `scripts/verify.py`
**Purpose**: Verify 5G connection (TODO)

**Entry Point**: `rm530-verify`

### Documentation

All markdown files are included in the package for easy access.

#### `docs/` - Main Documentation
- **SETUP-COMPLETE.md**: Success summary and tips
- **ecm-integration.md**: Complete setup guide
- **verify-5g.md**: Verification guide
- **NEXT-STEPS.md**: Quick commands

#### `reference/` - Quick Reference
- **AT-COMMANDS.md**: AT command reference
- **TROUBLESHOOTING.md**: Common issues and solutions

#### `legacy/` - Historical
- **integration.md**: Old QMI mode setup
- **comparison-qmi-vs-ecm.md**: Technical comparison

## Entry Points

Defined in `pyproject.toml`:

| Command | Script | Description |
|---------|--------|-------------|
| `rm530-setup-ecm` | `scripts.setup_ecm:main` | Switch to ECM mode |
| `rm530-configure-network` | `scripts.configure_network:main` | Setup NetworkManager |
| `rm530-verify` | `scripts.verify:main` | Verify connection |

## Installation

### From PyPI
```bash
pip install rm530-5g-integration
```

### From Source
```bash
git clone https://github.com/yourusername/rm530-5g-integration.git
cd rm530-5g-integration
pip install .
```

## Usage

### Command Line
```bash
# Setup ECM mode
sudo rm530-setup-ecm airtelgprs.com

# Configure network
rm530-configure-network

# Verify
rm530-verify
```

### Python API
```python
from rm530_5g_integration.scripts.setup_ecm import switch_to_ecm_mode

success = switch_to_ecm_mode(apn="airtelgprs.com")
```

## Dependencies

Required:
- `pyserial>=3.5` - Serial communication

System requirements:
- Python 3.7+
- Linux (tested on Raspberry Pi OS)
- NetworkManager
- Root/sudo access
- Waveshare RM530 modem

## Package Metadata

- **Name**: rm530-5g-integration
- **Version**: 1.0.0
- **License**: MIT
- **Author**: Anand
- **Python**: 3.7+
- **Platform**: Linux (Raspberry Pi)

## Building

```bash
# Clean
rm -rf build/ dist/ *.egg-info

# Build
python3 -m build

# Check
twine check dist/*
```

## Testing

```bash
# Install locally
pip install dist/rm530_5g_integration-1.0.0-py3-none-any.whl

# Test commands
rm530-setup-ecm --help
python3 -c "import rm530_5g_integration; print(rm530_5g_integration.__version__)"
```

## Distribution Files

After building:
- `dist/rm530-5g-integration-1.0.0.tar.gz` - Source distribution
- `dist/rm530_5g_integration-1.0.0-py3-none-any.whl` - Wheel

## File Sizes

Typical sizes:
- Source: ~100-200 KB
- Wheel: ~100-200 KB
- Installed: ~2-3 MB

## License

MIT License - See LICENSE file for details.

---

Last updated: 2024


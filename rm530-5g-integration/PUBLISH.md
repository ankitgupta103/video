# Publishing rm530-5g-integration Package

Instructions for publishing this package to PyPI.

## Prerequisites

1. **PyPI Account**: Create an account at https://pypi.org/account/register/
2. **API Token**: Get your API token from https://pypi.org/manage/account/token/
3. **Build Tools**: Install required tools

```bash
pip install --upgrade build twine
```

## Building the Package

### 1. Clean Previous Builds

```bash
cd rm530-5g-integration
rm -rf build/ dist/ *.egg-info
```

### 2. Build Distribution

```bash
python3 -m build
```

This will create:
- `dist/rm530-5g-integration-1.0.0.tar.gz` (source distribution)
- `dist/rm530_5g_integration-1.0.0-py3-none-any.whl` (wheel)

### 3. Verify Package Contents

```bash
tar -tzf dist/rm530-5g-integration-1.0.0.tar.gz
```

Check that all necessary files are included.

## Testing the Package Locally

### Install from Local Build

```bash
pip install dist/rm530_5g_integration-1.0.0-py3-none-any.whl
```

### Test Installation

```bash
# Verify package is installed
pip list | grep rm530

# Test commands
rm530-setup-ecm --help
rm530-verify --help
rm530-configure-network --help

# Test Python import
python3 -c "import rm530_5g_integration; print(rm530_5g_integration.__version__)"
```

### Uninstall Test

```bash
pip uninstall rm530-5g-integration
```

## Publishing to PyPI

### Option 1: Using Twine (Recommended)

#### Test First on TestPyPI

```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Install from TestPyPI to verify
pip install --index-url https://test.pypi.org/simple/ rm530-5g-integration
```

#### Upload to PyPI

```bash
# Upload to production PyPI
twine upload dist/*
```

You'll be prompted for:
- Username: `__token__`
- Password: Your PyPI API token

### Option 2: Using GitHub Actions (Recommended for CI/CD)

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [created]

jobs:
  build-and-publish:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.8'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    
    - name: Build package
      run: python -m build
    
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

Add `PYPI_API_TOKEN` to your GitHub repository secrets.

## Post-Publishing

### 1. Create a Git Tag

```bash
git tag v1.0.0
git push origin v1.0.0
```

### 2. Create a GitHub Release

1. Go to your repository on GitHub
2. Click "Releases" → "Create a new release"
3. Tag: `v1.0.0`
4. Title: `Release v1.0.0`
5. Description: Copy from README.md
6. Publish release

### 3. Verify Installation

```bash
# Anyone can now install with:
pip install rm530-5g-integration
```

## Version Management

### Updating Version

1. Update version in `rm530_5g_integration/__init__.py`:
   ```python
   __version__ = "1.0.1"  # or appropriate version
   ```

2. Update version in `pyproject.toml`:
   ```toml
   version = "1.0.1"
   ```

3. Follow build and publish steps above

### Semantic Versioning

- **Major** (2.0.0): Breaking changes
- **Minor** (1.1.0): New features, backward compatible
- **Patch** (1.0.1): Bug fixes

## Testing Checklist

Before publishing, verify:

- [ ] All documentation is updated
- [ ] Version numbers match in all files
- [ ] LICENSE file is present
- [ ] README.md is clear and complete
- [ ] All dependencies are listed in pyproject.toml
- [ ] Package builds successfully
- [ ] Package installs correctly
- [ ] All entry points work
- [ ] Documentation is accessible

## Troubleshooting

### Build Errors

```bash
# Clean and rebuild
python3 -m build --clean
```

### Upload Errors

```bash
# Check file size (must be < 100MB)
ls -lh dist/

# Verify package name is available
curl https://pypi.org/pypi/rm530-5g-integration/json
```

### Installation Issues

```bash
# Check package structure
python3 -m pip show rm530-5g-integration

# Verify entry points
which rm530-setup-ecm
```

## Security Best Practices

1. **Never commit** API tokens or passwords
2. Use **API tokens** instead of passwords
3. Use **GitHub Secrets** for CI/CD
4. Enable **2FA** on PyPI account
5. Review **uploaded files** after publishing

## Resources

- [Python Packaging User Guide](https://packaging.python.org/)
- [PyPI Documentation](https://pypi.org/help/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [TestPyPI](https://test.pypi.org/)

## Support

For issues or questions:
- Open an issue on GitHub
- Check documentation in the package
- Review PyPI guidelines

---

Happy Publishing! 🚀


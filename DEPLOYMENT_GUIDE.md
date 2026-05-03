# Python SDK Deployment & Publishing Guide

This guide explains how to publish the `afconwave` package to PyPI (Python Package Index).

## Prerequisites
1. You must have an account on [PyPI.org](https://pypi.org).
2. Install the required build and publishing tools locally:
   ```bash
   pip install --upgrade build twine
   ```

## Pre-Flight Checklist
- [ ] Run `python test.py` to ensure the module loads without syntax errors.
- [ ] Update the `version` variable inside `setup.py` (e.g., from `1.0.0` to `1.0.1`).

## Publishing Steps

1. **Build the Source Archive and Wheel**
   Run the build module from the directory containing `setup.py`:
   ```bash
   python -m build
   ```
   This will generate a `dist/` folder containing a `.tar.gz` and a `.whl` file.

2. **Upload to PyPI**
   Use `twine` to securely upload the newly built distribution files:
   ```bash
   python -m twine upload dist/*
   ```
   *Note: You will be prompted for your PyPI username and password (or API token).*

3. **Verify**
   Test the installation in a fresh virtual environment:
   ```bash
   pip install afconwave
   ```

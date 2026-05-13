#!/usr/bin/env bash
set -euo pipefail

# Use the system Python which has the required packages installed
PYTHON=/usr/bin/python3

$PYTHON img_to_pdf.py "$@" && $PYTHON ocr_pdf.py

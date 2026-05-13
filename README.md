# img_ocr_pdf

Two small Python scripts for working with image-based PDFs:

- **`img_to_pdf.py`** — Combine a folder of PNG/JPEG images into a single PDF.
- **`ocr_pdf.py`** — Add a searchable OCR text layer to image-based PDFs.

---

## Requirements

- Python 3.9 or newer
- pip

---

## Installation

### macOS

1. Install Python (if not already installed):
   ```bash
   brew install python
   ```

2. Install the Python dependencies:
   ```bash
   pip install img2pdf Pillow
   ```

3. Install `ocrmypdf` and its system dependencies:
   ```bash
   brew install ocrmypdf
   ```

### Windows

1. Install Python 3.9+ from [python.org](https://www.python.org/downloads/). During setup, check **"Add Python to PATH"**.

2. Install the Python dependencies:
   ```cmd
   pip install img2pdf Pillow
   ```

3. Install Tesseract OCR (required by `ocrmypdf`):
   - Download the installer from [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki).
   - Run the installer and note the install path (e.g. `C:\Program Files\Tesseract-OCR`).
   - Add that path to your system `PATH` environment variable.

4. Install Ghostscript (required by `ocrmypdf`):
   - Download from [ghostscript.com](https://www.ghostscript.com/releases/gsdnld.html).
   - Run the installer and add the `bin` folder (e.g. `C:\Program Files\gs\gs10.x.x\bin`) to your `PATH`.

5. Install `ocrmypdf`:
   ```cmd
   pip install ocrmypdf
   ```

---

## Folder structure

```
img_ocr_pdf/
├── input_image/        ← drop your images here
├── pdf_image/          ← image-only PDFs (output of img_to_pdf.py)
└── pdf_searchable/     ← searchable PDFs (output of ocr_pdf.py)
```

All three folders are created automatically if they don't exist.

---

## Usage

### Convert images to PDF — `img_to_pdf.py`

Converts all PNG/JPEG files in a directory into a single PDF. Images are sorted alphabetically by filename, so name them in the order you want them to appear (e.g. `01.jpg`, `02.jpg`, …).

```bash
python img_to_pdf.py [input_image_dir] [output_pdf_path]
```

Both arguments are optional:
- `input_image_dir` defaults to `input_image/`
- `output_pdf_path` defaults to `pdf_image/output.pdf`

**Examples:**
```bash
# use all defaults — drop images in input_image/ first
python img_to_pdf.py

# custom input dir, default output
python img_to_pdf.py ./my_images

# both custom
python img_to_pdf.py ./my_images pdf_image/my_scan.pdf
```

**Supported formats:** `.jpg`, `.jpeg`, `.png`

---

### Add OCR to PDFs — `ocr_pdf.py`

Adds a searchable text layer to image-based PDFs so the text can be copied, searched, and indexed.

**Batch mode (default)** — processes every PDF in `pdf_image/` and writes results to `pdf_searchable/` using the same filenames:

```bash
python ocr_pdf.py
```

**Single-file mode** — provide an explicit input (and optionally an output) path:

```bash
python ocr_pdf.py [input_pdf_path] [output_pdf_path] [options]
```

**Options:**

| Flag | Description |
|---|---|
| `--lang <code>` | OCR language code. Default: `eng`. See [Tesseract language codes](https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html). |
| `--input-dir <dir>` | Source directory for batch mode. Default: `pdf_image/` |
| `--output-dir <dir>` | Destination directory for batch mode. Default: `pdf_searchable/` |
| `--no-deskew` | Disable automatic page deskewing. |
| `--no-rotate-pages` | Disable automatic page rotation correction. |
| `--clean` | Clean page images before OCR (may alter appearance). |
| `--force-ocr` | Force OCR even if the PDF already contains a text layer. |

**Example with options:**
```bash
python ocr_pdf.py --lang por --force-ocr
```

---

## Typical workflow

Drop your images into `input_image/`, then run the full pipeline in one command:

```bash
./run_pipeline.sh
```

Or run each step manually:

```bash
# Step 1: combine images into a PDF
python3 img_to_pdf.py

# Step 2: add OCR so the PDF is searchable
python3 ocr_pdf.py
```

The final searchable PDFs will be in `pdf_searchable/`.

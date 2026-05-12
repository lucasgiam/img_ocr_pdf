# img_ocr_pdf

Two small Python scripts for working with image-based PDFs:

- **`img_to_pdf.py`** — Combine a folder of PNG/JPEG images into a single PDF.
- **`ocr_pdf.py`** — Add a searchable OCR text layer to an image-based PDF.

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

The scripts use two folders by default — both are created automatically if they don't exist:

```
img_ocr_pdf/
├── input_imgs/          ← drop your images here
└── output_pdfs/
    ├── output_img_only.pdf      ← intermediate PDF (images only)
    └── output_searchable.pdf    ← final searchable PDF
```

---

## Usage

### Convert images to PDF — `img_to_pdf.py`

Converts all PNG/JPEG files in a directory into a single PDF. Images are sorted alphabetically by filename, so name them in the order you want them to appear (e.g. `01.jpg`, `02.jpg`, …).

```bash
python img_to_pdf.py [input_image_dir] [output_pdf_path]
```

Both arguments are optional:
- `input_image_dir` defaults to `input_imgs/`
- `output_pdf_path` defaults to `output_pdfs/output_img_only.pdf`

**Examples:**
```bash
# use all defaults — drop images in input_imgs/ first
python img_to_pdf.py

# custom input dir, default output
python img_to_pdf.py ./my_images

# both custom
python img_to_pdf.py ./my_images my_scan.pdf
```

**Supported formats:** `.jpg`, `.jpeg`, `.png`

---

### Add OCR to a PDF — `ocr_pdf.py`

Adds a searchable text layer to an image-based PDF so the text can be copied, searched, and indexed.

```bash
python ocr_pdf.py [input_pdf_path] [output_pdf_path] [options]
```

Both arguments are optional:
- `input_pdf_path` defaults to `output_pdfs/output_img_only.pdf`
- `output_pdf_path` defaults to `output_pdfs/output_searchable.pdf`

**Examples:**
```bash
# use all defaults
python ocr_pdf.py

# custom input, default output
python ocr_pdf.py my_scan.pdf

# both custom
python ocr_pdf.py my_scan.pdf my_final.pdf
```

**Options:**

| Flag | Description |
|---|---|
| `--lang <code>` | OCR language code. Default: `eng`. See [Tesseract language codes](https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html). |
| `--no-deskew` | Disable automatic page deskewing. |
| `--no-rotate-pages` | Disable automatic page rotation correction. |
| `--clean` | Clean page images before OCR (may alter appearance). |
| `--force-ocr` | Force OCR even if the PDF already contains a text layer. |

**Example with options:**
```bash
python ocr_pdf.py output_pdfs/output_img_only.pdf output_pdfs/output_searchable.pdf --lang por --force-ocr
```

---

## Typical workflow

Drop your images into `input_imgs/`, then run:

```bash
# Step 1: combine images into a PDF
python3 img_to_pdf.py

# Step 2: add OCR so the PDF is searchable
python3 ocr_pdf.py
```

Or run the full pipeline in one command:

```bash
python3 img_to_pdf.py && python3 ocr_pdf.py
```

Both output files will be in `output_pdfs/`.

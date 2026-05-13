#!/usr/bin/python3

from pathlib import Path
import argparse
import subprocess
import sys


def run_ocrmypdf(
    input_pdf_path: Path,
    output_pdf_path: Path,
    language: str,
    deskew: bool,
    rotate_pages: bool,
    clean: bool,
    force_ocr: bool,
) -> None:
    output_pdf_path.parent.mkdir(parents=True, exist_ok=True)

    command = ["ocrmypdf"]

    if deskew:
        command.append("--deskew")

    if rotate_pages:
        command.append("--rotate-pages")

    if clean:
        command.append("--clean")

    if force_ocr:
        command.append("--force-ocr")

    command.extend([
        "-l", language,
        str(input_pdf_path),
        str(output_pdf_path),
    ])

    subprocess.run(command, check=True)


def collect_pdfs(input_dir: Path) -> list[Path]:
    if not input_dir.is_dir():
        input_dir.mkdir(parents=True, exist_ok=True)

    pdfs = sorted(
        path for path in input_dir.iterdir()
        if path.is_file() and path.suffix.lower() == ".pdf"
    )

    if not pdfs:
        raise FileNotFoundError(f"No PDF files found in: {input_dir}")

    return pdfs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Add OCR text layer to image-based PDFs."
    )

    parser.add_argument(
        "input_pdf_path",
        type=Path,
        nargs="?",
        default=None,
        help=(
            "Path to a single input PDF. "
            "Omit to process all PDFs in pdf_image/ and write results to pdf_searchable/."
        ),
    )

    parser.add_argument(
        "output_pdf_path",
        type=Path,
        nargs="?",
        default=None,
        help=(
            "Path where the OCR PDF should be saved. "
            "Only used when input_pdf_path is also provided."
        ),
    )

    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path("pdf_image"),
        help="Directory of PDFs to process in batch mode. Default: pdf_image/",
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("pdf_searchable"),
        help="Directory where OCR PDFs are written in batch mode. Default: pdf_searchable/",
    )

    parser.add_argument(
        "--lang",
        default="eng",
        help="OCR language code. Default: eng",
    )

    parser.add_argument(
        "--no-deskew",
        action="store_true",
        help="Disable page deskewing.",
    )

    parser.add_argument(
        "--no-rotate-pages",
        action="store_true",
        help="Disable automatic page rotation.",
    )

    parser.add_argument(
        "--clean",
        action="store_true",
        help="Clean page images before OCR. May change page appearance.",
    )

    parser.add_argument(
        "--force-ocr",
        action="store_true",
        help="Force OCR even if the PDF already has text.",
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()

    ocr_kwargs = dict(
        language=args.lang,
        deskew=not args.no_deskew,
        rotate_pages=not args.no_rotate_pages,
        clean=args.clean,
        force_ocr=args.force_ocr,
    )

    # Single-file mode
    if args.input_pdf_path is not None:
        if not args.input_pdf_path.exists():
            print(f"Error: input PDF does not exist: {args.input_pdf_path}", file=sys.stderr)
            return 1

        output_path = args.output_pdf_path or (
            args.output_dir / args.input_pdf_path.name
        )

        try:
            print(f"Running OCR on {args.input_pdf_path}...")
            run_ocrmypdf(args.input_pdf_path, output_path, **ocr_kwargs)
            print(f"Done: {output_path}")
            return 0
        except subprocess.CalledProcessError as error:
            print("Error: OCRmyPDF failed.", file=sys.stderr)
            print(f"Exit code: {error.returncode}", file=sys.stderr)
            return error.returncode
        except Exception as error:
            print(f"Error: {error}", file=sys.stderr)
            return 1

    # Batch mode: process all PDFs in input_dir
    try:
        pdf_paths = collect_pdfs(args.input_dir)
    except FileNotFoundError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(f"Found {len(pdf_paths)} PDF(s) in {args.input_dir}:")
    for p in pdf_paths:
        print(f"  {p.name}")

    errors = 0
    for pdf_path in pdf_paths:
        output_path = args.output_dir / pdf_path.name
        try:
            print(f"\nRunning OCR on {pdf_path.name}...")
            run_ocrmypdf(pdf_path, output_path, **ocr_kwargs)
            print(f"Done: {output_path}")
        except subprocess.CalledProcessError as error:
            print(f"Error: OCRmyPDF failed on {pdf_path.name} (exit {error.returncode})", file=sys.stderr)
            errors += 1
        except Exception as error:
            print(f"Error processing {pdf_path.name}: {error}", file=sys.stderr)
            errors += 1

    if errors:
        print(f"\n{errors} file(s) failed.", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

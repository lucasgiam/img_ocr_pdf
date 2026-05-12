#!/usr/bin/env python3

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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Add OCR text layer to an image-based PDF."
    )

    parser.add_argument(
        "input_pdf_path",
        type=Path,
        nargs="?",
        default=Path("output_pdfs/output_img_only.pdf"),
        help="Path to the input image-based PDF. Default: output_pdfs/output_img_only.pdf",
    )

    parser.add_argument(
        "output_pdf_path",
        type=Path,
        nargs="?",
        default=Path("output_pdfs/output_searchable.pdf"),
        help="Path where the OCR PDF should be saved. Default: output_pdfs/output_searchable.pdf",
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

    if not args.input_pdf_path.exists():
        print(f"Error: input PDF does not exist: {args.input_pdf_path}", file=sys.stderr)
        return 1

    try:
        print("Running OCR...")
        run_ocrmypdf(
            input_pdf_path=args.input_pdf_path,
            output_pdf_path=args.output_pdf_path,
            language=args.lang,
            deskew=not args.no_deskew,
            rotate_pages=not args.no_rotate_pages,
            clean=args.clean,
            force_ocr=args.force_ocr,
        )

        print(f"Done: {args.output_pdf_path}")
        return 0

    except subprocess.CalledProcessError as error:
        print("Error: OCRmyPDF failed.", file=sys.stderr)
        print(f"Exit code: {error.returncode}", file=sys.stderr)
        return error.returncode

    except Exception as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
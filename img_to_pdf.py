#!/usr/bin/env python3

from pathlib import Path
import argparse
import io
import sys

import img2pdf
from PIL import Image, ImageOps


SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png"}


def collect_images(input_dir: Path) -> list[Path]:
    if not input_dir.is_dir():
        input_dir.mkdir(parents=True, exist_ok=True)

    images = [
        path for path in input_dir.iterdir()
        if path.is_file()
        and not path.name.startswith("._")  # skip macOS AppleDouble resource forks
        and path.suffix.lower() in SUPPORTED_EXTENSIONS
    ]

    images.sort(key=lambda path: path.name.lower())

    if not images:
        raise FileNotFoundError(f"No PNG/JPEG images found in: {input_dir}")

    return images


def load_image(path: Path) -> bytes:
    # Use Pillow to read only the primary image frame, discarding embedded
    # secondary frames (e.g. iPhone MPF/HDR gainmap) that img2pdf would
    # otherwise turn into extra pages.
    with Image.open(path) as img:
        img = ImageOps.exif_transpose(img)
        buf = io.BytesIO()
        if path.suffix.lower() == ".png":
            img.save(buf, format="PNG")
        else:
            if img.mode not in ("RGB", "L", "CMYK"):
                img = img.convert("RGB")
            img.save(buf, format="JPEG", quality=95, subsampling=0)
        return buf.getvalue()


A4 = (img2pdf.mm_to_pt(210), img2pdf.mm_to_pt(297))


def convert_images_to_pdf(image_paths: list[Path], output_pdf_path: Path) -> None:
    output_pdf_path.parent.mkdir(parents=True, exist_ok=True)

    layout = img2pdf.get_layout_fun(pagesize=A4)
    with open(output_pdf_path, "wb") as output_file:
        output_file.write(img2pdf.convert([load_image(p) for p in image_paths], layout_fun=layout))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert a directory of PNG/JPEG images into one PDF."
    )

    parser.add_argument(
        "input_img_dir",
        type=Path,
        nargs="?",
        default=Path("input_imgs"),
        help="Directory containing input images. Default: input_imgs/",
    )

    parser.add_argument(
        "output_pdf_path",
        type=Path,
        nargs="?",
        default=Path("output_pdfs/output_img_only.pdf"),
        help="Path where the output PDF should be saved. Default: output_pdfs/output_img_only.pdf",
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        image_paths = collect_images(args.input_img_dir)

        print(f"Found {len(image_paths)} image(s).")
        print("Image order:")
        for image_path in image_paths:
            print(f"  {image_path.name}")

        print("Converting images to PDF...")
        convert_images_to_pdf(image_paths, args.output_pdf_path)

        print(f"Done: {args.output_pdf_path}")
        return 0

    except Exception as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
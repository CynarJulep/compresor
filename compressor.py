"""Compresión con techo de 1 MB para imágenes y PDF."""

from __future__ import annotations

import io
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageOps

TARGET_BYTES = 1 * 1024 * 1024
SAFE_TARGET = 980 * 1024
MAX_INPUT_BYTES = 80 * 1024 * 1024

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff", ".gif", ".heic", ".heif"}
PDF_EXTS = {".pdf"}

try:
    from pillow_heif import register_heif_opener

    register_heif_opener()
except Exception:
    pass


@dataclass
class CompressResult:
    data: bytes
    filename: str
    original_size: int
    final_size: int
    already_ok: bool
    converted: bool
    note: str = ""

    @property
    def under_limit(self) -> bool:
        return self.final_size <= TARGET_BYTES

    @property
    def ratio(self) -> float:
        if self.original_size <= 0:
            return 1.0
        return self.final_size / self.original_size


def format_size(n: int) -> str:
    if n < 1024:
        return f"{n} B"
    if n < 1024 * 1024:
        return f"{n / 1024:.1f} KB"
    return f"{n / (1024 * 1024):.2f} MB"


def supported_extension(filename: str) -> bool:
    return Path(filename).suffix.lower() in IMAGE_EXTS | PDF_EXTS


def compress_file(data: bytes, filename: str) -> CompressResult:
    if len(data) > MAX_INPUT_BYTES:
        raise ValueError(
            f"El archivo pesa {format_size(len(data))}. "
            f"El máximo es {format_size(MAX_INPUT_BYTES)}."
        )

    ext = Path(filename).suffix.lower()
    stem = Path(filename).stem

    if ext in PDF_EXTS:
        return _compress_pdf(data, stem, len(data))
    if ext in IMAGE_EXTS:
        return _compress_image(data, stem, ext, len(data))

    raise ValueError("Formato no soportado. Usá PDF, JPG, PNG, WEBP, TIFF, BMP, GIF o HEIC.")


def _result(
    data: bytes,
    filename: str,
    original: int,
    *,
    already_ok: bool = False,
    converted: bool = False,
    note: str = "",
) -> CompressResult:
    return CompressResult(
        data=data,
        filename=filename,
        original_size=original,
        final_size=len(data),
        already_ok=already_ok,
        converted=converted,
        note=note,
    )


def _compress_image(data: bytes, stem: str, ext: str, original: int) -> CompressResult:
    if original <= TARGET_BYTES:
        return _result(data, f"{stem}{ext}", original, already_ok=True)

    image = Image.open(io.BytesIO(data))
    image = ImageOps.exif_transpose(image) or image

    prefers_alpha = ext in {".png", ".webp", ".gif"} and _has_useful_alpha(image)
    rgb = _to_rgb(image)
    rgba = image.convert("RGBA") if prefers_alpha else None

    # WebP suele ganar en fotos. JPEG se mantiene si el original era JPEG.
    candidates: list[tuple[str, str, Image.Image]] = []
    if prefers_alpha and rgba is not None:
        candidates.append((".webp", "WEBP", rgba))
    if ext in {".jpg", ".jpeg"}:
        candidates.append((".jpg", "JPEG", rgb))
        candidates.append((".webp", "WEBP", rgb))
    else:
        candidates.append((".webp", "WEBP", rgb if rgba is None else rgba))
        candidates.append((".jpg", "JPEG", rgb))

    best: tuple[bytes, str] | None = None

    for out_ext, fmt, im in candidates:
        encoded, ok = _encode_under_limit(im, fmt)
        if best is None or len(encoded) < len(best[0]):
            best = (encoded, f"{stem}{out_ext}")
        if ok:
            converted = Path(best[1]).suffix.lower() != ext
            note = "Se cambió el formato para llegar a 1 MB." if converted else ""
            return _result(encoded, best[1], original, converted=converted, note=note)

    assert best is not None
    converted = Path(best[1]).suffix.lower() != ext
    note = "No se pudo bajar de 1 MB sin perder demasiado. Se entrega la versión más liviana."
    return _result(best[0], best[1], original, converted=converted, note=note)


def _has_useful_alpha(image: Image.Image) -> bool:
    if image.mode in {"RGBA", "LA"}:
        extrema = image.getchannel("A").getextrema()
        return extrema[0] < 250
    if image.mode == "P" and "transparency" in image.info:
        return True
    return False


def _to_rgb(image: Image.Image) -> Image.Image:
    if image.mode == "RGB":
        return image
    if image.mode in {"RGBA", "LA"}:
        background = Image.new("RGB", image.size, (255, 255, 255))
        rgba = image.convert("RGBA")
        background.paste(rgba, mask=rgba.split()[-1])
        return background
    if image.mode == "P":
        return _to_rgb(image.convert("RGBA"))
    if image.mode == "CMYK":
        return image.convert("RGB")
    return image.convert("RGB")


def _encode_under_limit(image: Image.Image, fmt: str) -> tuple[bytes, bool]:
    max_sides = (None, 2560, 1920, 1600, 1280, 1024, 800, 640, 480)
    best = _encode_image(image, fmt, quality=80, max_side=None)

    for max_side in max_sides:
        lo, hi = 16, 88
        found: bytes | None = None
        while lo <= hi:
            quality = (lo + hi) // 2
            blob = _encode_image(image, fmt, quality=quality, max_side=max_side)
            if len(blob) < len(best):
                best = blob
            if len(blob) <= SAFE_TARGET:
                found = blob
                lo = quality + 1
            else:
                hi = quality - 1
        if found is not None:
            return found, True

    return best, len(best) <= TARGET_BYTES


def _encode_image(image: Image.Image, fmt: str, quality: int, max_side: int | None) -> bytes:
    work = image
    if max_side and max(work.size) > max_side:
        work = work.copy()
        work.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)

    buffer = io.BytesIO()
    if fmt == "JPEG":
        if work.mode != "RGB":
            work = _to_rgb(work)
        work.save(buffer, format="JPEG", quality=quality, optimize=True, progressive=True)
    elif fmt == "WEBP":
        work.save(buffer, format="WEBP", quality=quality, method=4)
    else:
        work.save(buffer, format=fmt, optimize=True)
    return buffer.getvalue()


def _compress_pdf(data: bytes, stem: str, original: int) -> CompressResult:
    import fitz

    if original <= TARGET_BYTES:
        return _result(data, f"{stem}.pdf", original, already_ok=True)

    src = fitz.open(stream=data, filetype="pdf")
    try:
        lossless = _save_pdf(src, garbage=4, deflate=True, clean=True)
        if len(lossless) <= TARGET_BYTES:
            return _result(lossless, f"{stem}.pdf", original)

        best = lossless if len(lossless) < original else data
        plans: list[tuple[int, int, bool]] = [
            (130, 78, False),
            (110, 70, False),
            (96, 62, False),
            (84, 52, False),
            (72, 42, False),
            (64, 34, False),
            (56, 28, True),
            (48, 22, True),
            (40, 18, True),
        ]

        for dpi, quality, gray in plans:
            rebuilt = _rasterize_pdf(src, dpi=dpi, quality=quality, grayscale=gray)
            if len(rebuilt) < len(best):
                best = rebuilt
            if len(rebuilt) <= SAFE_TARGET:
                note = "El PDF se reconstruyó con menor resolución para entrar en 1 MB."
                return _result(rebuilt, f"{stem}.pdf", original, note=note)

        note = "No se pudo bajar de 1 MB. Se entrega la versión más liviana posible."
        return _result(best, f"{stem}.pdf", original, note=note)
    finally:
        src.close()


def _save_pdf(doc, **kwargs) -> bytes:
    buffer = io.BytesIO()
    doc.save(buffer, **kwargs)
    return buffer.getvalue()


def _rasterize_pdf(src, dpi: int, quality: int, grayscale: bool) -> bytes:
    import fitz

    out = fitz.open()
    zoom = dpi / 72
    matrix = fitz.Matrix(zoom, zoom)
    colorspace = fitz.csGRAY if grayscale else fitz.csRGB

    try:
        for page in src:
            pix = page.get_pixmap(matrix=matrix, colorspace=colorspace, alpha=False)
            image = Image.frombytes("L" if grayscale else "RGB", (pix.width, pix.height), pix.samples)
            pix = None
            jpeg = io.BytesIO()
            image.save(jpeg, format="JPEG", quality=quality, optimize=True)
            image.close()
            rect = page.rect
            new_page = out.new_page(width=rect.width, height=rect.height)
            new_page.insert_image(rect, stream=jpeg.getvalue())
        return _save_pdf(out, garbage=4, deflate=True)
    finally:
        out.close()

import io
import os

import pytest
from PIL import Image

from compressor import (
    MAX_FILES,
    TARGET_BYTES,
    compress_file,
    compress_uploads,
    compressed_filename,
    format_size,
    merge_files_to_pdf,
)


def _jpeg(width: int, height: int, quality: int = 95) -> bytes:
    image = Image.frombytes("RGB", (width, height), os.urandom(width * height * 3))
    buf = io.BytesIO()
    image.save(buf, format="JPEG", quality=quality)
    return buf.getvalue()


def test_format_size():
    assert format_size(512) == "512 B"
    assert "KB" in format_size(2048)
    assert "MB" in format_size(2 * 1024 * 1024)


def test_compressed_filename():
    assert compressed_filename("DNI", ".pdf") == "DNI_comprimido.pdf"
    assert compressed_filename("foto", ".jpg") == "foto_comprimido.jpg"
    assert compressed_filename("frente", ".jpg", combined=True) == "frente_combinado_comprimido.pdf"


def test_small_file_passthrough_renamed():
    data = _jpeg(80, 80, quality=40)
    result = compress_file(data, "foto.jpg")
    assert result.already_ok
    assert result.data == data
    assert result.under_limit
    assert result.filename == "foto_comprimido.jpg"


def test_large_jpeg_under_1mb():
    data = _jpeg(2800, 2000, quality=95)
    assert len(data) > TARGET_BYTES
    result = compress_file(data, "foto.jpg")
    assert result.under_limit
    assert result.final_size <= TARGET_BYTES
    assert "_comprimido" in result.filename
    Image.open(io.BytesIO(result.data)).verify()


def test_png_can_convert_to_hit_limit():
    image = Image.frombytes("RGB", (1800, 1400), os.urandom(1800 * 1400 * 3))
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    data = buf.getvalue()
    result = compress_file(data, "captura.png")
    assert result.under_limit
    assert result.filename.startswith("captura_comprimido")
    assert result.filename.lower().endswith((".jpg", ".jpeg", ".webp", ".png"))


def test_pdf_under_1mb():
    import fitz

    photo = _jpeg(1400, 1900, quality=92)
    doc = fitz.open()
    for _ in range(3):
        page = doc.new_page(width=595, height=842)
        page.insert_image(page.rect, stream=photo)
    data = doc.tobytes()
    doc.close()
    assert TARGET_BYTES < len(data) <= 80 * 1024 * 1024
    result = compress_file(data, "scan.pdf")
    assert result.filename == "scan_comprimido.pdf"
    assert result.under_limit


def test_merge_two_jpegs_to_pdf():
    import fitz

    a = _jpeg(400, 300, quality=85)
    b = _jpeg(320, 240, quality=85)
    merged = merge_files_to_pdf([(a, "a.jpg"), (b, "b.jpg")])
    doc = fitz.open(stream=merged, filetype="pdf")
    try:
        assert doc.page_count == 2
    finally:
        doc.close()


def test_compress_uploads_combined_name():
    a = _jpeg(400, 300, quality=80)
    b = _jpeg(400, 300, quality=80)
    result = compress_uploads([(a, "frente.jpg"), (b, "dorso.jpg")])
    assert result.filename == "frente_combinado_comprimido.pdf"
    assert result.under_limit
    assert "unieron" in result.note.lower() or "PDF" in result.note


def test_compress_uploads_rejects_more_than_max():
    tiny = _jpeg(40, 40, quality=40)
    items = [(tiny, f"f{i}.jpg") for i in range(MAX_FILES + 1)]
    with pytest.raises(ValueError, match="Máximo"):
        compress_uploads(items)


def test_compress_uploads_single_delegates():
    data = _jpeg(80, 80, quality=40)
    result = compress_uploads([(data, "solo.jpg")])
    assert result.filename == "solo_comprimido.jpg"

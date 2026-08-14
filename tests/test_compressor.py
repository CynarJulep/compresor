import io
import os

from PIL import Image

from compressor import TARGET_BYTES, compress_file, format_size


def _jpeg(width: int, height: int, quality: int = 95) -> bytes:
    image = Image.frombytes("RGB", (width, height), os.urandom(width * height * 3))
    buf = io.BytesIO()
    image.save(buf, format="JPEG", quality=quality)
    return buf.getvalue()


def test_format_size():
    assert format_size(512) == "512 B"
    assert "KB" in format_size(2048)
    assert "MB" in format_size(2 * 1024 * 1024)


def test_small_file_passthrough():
    data = _jpeg(80, 80, quality=40)
    result = compress_file(data, "foto.jpg")
    assert result.already_ok
    assert result.data == data
    assert result.under_limit


def test_large_jpeg_under_1mb():
    data = _jpeg(2800, 2000, quality=95)
    assert len(data) > TARGET_BYTES
    result = compress_file(data, "foto.jpg")
    assert result.under_limit
    assert result.final_size <= TARGET_BYTES
    Image.open(io.BytesIO(result.data)).verify()


def test_png_can_convert_to_hit_limit():
    image = Image.frombytes("RGB", (1800, 1400), os.urandom(1800 * 1400 * 3))
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    data = buf.getvalue()
    result = compress_file(data, "captura.png")
    assert result.under_limit
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
    assert result.filename.endswith(".pdf")
    assert result.under_limit

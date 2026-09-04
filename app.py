from dataclasses import dataclass
from pathlib import Path

import html

import streamlit as st
import streamlit.components.v1 as components
import streamlit_shadcn_ui as ui

from compressor import (
    IMAGE_EXTS,
    MAX_FILES,
    MAX_INPUT_BYTES,
    TARGET_BYTES,
    compress_uploads,
    format_size,
    supported_extension,
)
from explainer import render_explainer

ROOT = Path(__file__).resolve().parent
LOGO = ROOT / "assets" / "brand" / "msf-horizontal.png"
ICON = ROOT / "assets" / "brand" / "msf-icon.png"
ICONS_DIR = ROOT / "assets" / "icons"

st.set_page_config(
    page_title="Compresor de archivos — Atención Ciudadana",
    page_icon=str(ICON) if ICON.exists() else None,
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=Outfit:wght@400;500;600;700&display=swap');

.stApp {
  background: #F4F6F8;
  color: #0C1929;
  font-family: "Outfit", "Helvetica Neue", sans-serif;
}

.stApp::before {
  content: "";
  position: fixed;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: #0C2644;
  z-index: 100;
}

header[data-testid="stHeader"],
#MainMenu,
footer,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
[data-testid="stHeaderActionElements"],
[data-testid="stAppDeployButton"],
.stAppDeployButton,
a[href*="streamlit.io/cloud"],
a[href*="share.streamlit.io"],
[class*="viewerBadge"],
[class*="ViewerBadge"],
[data-testid="stBaseButton-headerNoPadding"] {
  display: none !important;
  visibility: hidden !important;
  pointer-events: none !important;
}

.block-container {
  max-width: 1040px;
  padding-top: 28px;
  padding-bottom: 20px;
  animation: enter 420ms cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes enter {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: none; }
}

@keyframes stepIn {
  from { opacity: 0; transform: translateY(6px); }
  to { opacity: 1; transform: none; }
}

h1, .hero-title {
  font-family: "Outfit", sans-serif !important;
  font-weight: 650 !important;
  font-size: clamp(2rem, 3.8vw, 2.75rem) !important;
  line-height: 1.1 !important;
  letter-spacing: -0.03em !important;
  color: #0C2644 !important;
  margin: 0 0 0.45rem 0 !important;
  text-shadow:
    0 1px 0 rgba(255, 255, 255, 0.9),
    0 6px 18px rgba(12, 38, 68, 0.12);
}

.welcome {
  color: #2C3D4F;
  font-size: 0.9rem;
  line-height: 1.5;
  max-width: 46rem;
  margin: 0 0 1.1rem 0;
  font-family: "Outfit", sans-serif;
}

.welcome p { margin: 0; }

div[data-testid="stVerticalBlockBorderWrapper"] {
  background: #FFFFFF;
  border: 1px solid #D5DEE8 !important;
  border-radius: 10px !important;
  padding: 2px 4px;
  box-shadow:
    0 1px 0 rgba(255, 255, 255, 0.8) inset,
    0 6px 16px rgba(12, 38, 68, 0.06);
  animation: stepIn 320ms cubic-bezier(0.16, 1, 0.3, 1);
}

#paso-actual { padding: 6px 4px 2px; }

.wizard-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 6px;
}

.wizard-dots {
  display: flex;
  gap: 5px;
}

.wizard-dots span {
  display: block;
  width: 26px;
  height: 3px;
  border-radius: 2px;
  background: #D5DEE8;
}

.wizard-dots span.done,
.wizard-dots span.current { background: #1A4A6E; }

.wizard-title-row {
  display: flex;
  align-items: baseline;
  flex-wrap: wrap;
  gap: 8px 12px;
  margin: 0;
}

.wizard-title {
  margin: 0;
  color: #0C2644;
  font-size: 1.45rem;
  font-weight: 650;
  font-family: "Outfit", sans-serif;
  letter-spacing: -0.02em;
  line-height: 1.2;
}

.wizard-help {
  margin: 0;
  color: #5A6B7A;
  font-size: 0.92rem;
  line-height: 1.3;
  font-family: "Outfit", sans-serif;
}

.file-row [data-testid="stHorizontalBlock"] {
  gap: 8px;
  align-items: center;
}

.file-chip {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  box-sizing: border-box;
  padding: 10px 12px;
  background: #FFFFFF;
  border: 1px solid #D5DEE8;
  border-radius: 8px;
  font-family: "Outfit", sans-serif;
  animation: stepIn 240ms cubic-bezier(0.16, 1, 0.3, 1);
}

.file-chip .icon {
  flex-shrink: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  background: #F0F4F8;
  color: #1A4A6E;
}

.file-chip .body {
  min-width: 0;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.file-chip .name {
  color: #0C2644;
  font-size: 0.86rem;
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.file-chip .meta {
  color: #5A6B7A;
  font-size: 0.75rem;
}

.process-note {
  margin: 0 0 8px 0;
  padding: 8px 10px;
  background: #F0F4F8;
  border: 1px solid #C5D4E3;
  border-radius: 6px;
  color: #1A4A6E;
  font-size: 0.84rem;
  font-family: "Outfit", sans-serif;
}

.action-slot {
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-height: 72px;
  padding-top: 4px;
}

.metrics-line {
  display: flex;
  flex-wrap: wrap;
  gap: 10px 18px;
  margin: 0 0 8px 0;
  font-family: "Outfit", sans-serif;
  font-size: 0.82rem;
  color: #2C3D4F;
}

.metrics-line strong {
  color: #0C2644;
  font-weight: 600;
}

[data-testid="stIconMaterial"] {
  font-family: "Material Symbols Rounded", "Material Symbols Outlined" !important;
  font-weight: 400 !important;
  font-style: normal !important;
  letter-spacing: normal !important;
  text-transform: none !important;
}

[data-testid="stFileUploader"] {
  width: 100%;
}

[data-testid="stFileUploader"] section {
  padding: 0 !important;
  background: transparent !important;
  border: none !important;
}

[data-testid="stFileUploaderDropzone"] {
  position: relative !important;
  min-height: 168px !important;
  cursor: pointer;
  background: #F7FAFC !important;
  border: 1.5px dashed #A8B8C8 !important;
  border-radius: 10px !important;
  transition:
    border-color 160ms ease,
    background 160ms ease,
    box-shadow 160ms ease,
    transform 160ms ease;
}

[data-testid="stFileUploaderDropzone"] > * { opacity: 0 !important; }

[data-testid="stFileUploaderDropzone"]::after {
  content: "Arrastrá archivos acá o hacé clic";
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 18px;
  color: #1A4A6E;
  font-family: "Outfit", sans-serif;
  font-size: 1.05rem;
  font-weight: 550;
  letter-spacing: -0.01em;
  pointer-events: none;
  text-align: center;
  transition: color 160ms ease, font-size 160ms ease, opacity 160ms ease;
}

[data-testid="stFileUploaderDropzone"]:hover {
  border-color: #1A4A6E !important;
  background: #F0F4F8 !important;
}

body.compresor-dragging [data-testid="stVerticalBlockBorderWrapper"]:has([data-testid="stFileUploaderDropzone"]) {
  position: relative !important;
}

body.compresor-dragging [data-testid="stVerticalBlockBorderWrapper"]:has([data-testid="stFileUploaderDropzone"])::before {
  content: "";
  position: absolute;
  inset: 0;
  z-index: 25;
  border-radius: 10px;
  background: rgba(244, 246, 248, 0.55);
  backdrop-filter: blur(7px);
  -webkit-backdrop-filter: blur(7px);
  pointer-events: none;
}

body.compresor-dragging [data-testid="stFileUploader"] > section,
body.compresor-dragging [data-testid="stFileUploaderDropzone"] {
  height: 100% !important;
  min-height: 100% !important;
  border-radius: 10px !important;
  border: 2px dashed #1A4A6E !important;
  background: rgba(255, 255, 255, 0.42) !important;
  box-shadow:
    inset 0 0 0 1px rgba(26, 74, 110, 0.1),
    0 12px 40px rgba(12, 38, 68, 0.08);
}

body.compresor-dragging [data-testid="stFileUploaderDropzone"]::after {
  content: "Soltá el archivo acá";
  font-size: clamp(1.45rem, 3.2vw, 2rem);
  font-weight: 650;
  color: #0C2644;
  letter-spacing: -0.03em;
  text-shadow: 0 1px 0 rgba(255, 255, 255, 0.85);
}

[data-testid="stFileUploaderFile"],
[data-testid="stFileUploaderFileName"],
[data-testid="stFileUploaderDeleteBtn"],
[data-testid="stFileUploaderFileData"],
ul[data-testid="stFileUploaderFileList"],
section[data-testid="stFileUploader"] > div > ul,
[data-testid="stFileUploaderDropzoneInstructions"] {
  display: none !important;
}

div.stButton > button,
[data-testid="stBaseButton-primary"],
[data-testid="baseButton-primary"] {
  background: #1A4A6E !important;
  color: #FFFFFF !important;
  border: 1px solid #1A4A6E !important;
  border-radius: 6px !important;
  font-family: "Outfit", sans-serif !important;
  font-weight: 500 !important;
  box-shadow: 0 2px 6px rgba(12, 38, 68, 0.12) !important;
  min-height: 2.75rem;
  width: 100%;
  transition: background 160ms ease, border-color 160ms ease, transform 120ms ease;
}

div.stButton > button:hover,
[data-testid="stBaseButton-primary"]:hover,
[data-testid="baseButton-primary"]:hover {
  background: #0C2644 !important;
  border-color: #0C2644 !important;
  color: #FFFFFF !important;
  transform: translateY(-1px);
}

div.stDownloadButton > button,
[data-testid="stDownloadButton"] button {
  background: #2F6B5C !important;
  color: #FFFFFF !important;
  border: 1px solid #2F6B5C !important;
  border-radius: 6px !important;
  font-family: "Outfit", sans-serif !important;
  font-weight: 500 !important;
  box-shadow: 0 2px 6px rgba(12, 38, 68, 0.10) !important;
  min-height: 2.75rem;
  width: 100%;
  transition: background 160ms ease, border-color 160ms ease, transform 120ms ease;
}

div.stDownloadButton > button:hover,
[data-testid="stDownloadButton"] button:hover {
  background: #245448 !important;
  border-color: #245448 !important;
  color: #FFFFFF !important;
  transform: translateY(-1px);
}

div.stButton > button:disabled,
[data-testid="stBaseButton-primary"]:disabled,
[data-testid="baseButton-primary"]:disabled {
  background: #1A4A6E !important;
  border-color: #1A4A6E !important;
  color: #FFFFFF !important;
  opacity: 0.45;
  transform: none;
}

/* Botón secundario más bajo */
div.stButton:has(button:not([kind="primary"])) > button,
div.stButton > button[kind="secondary"] {
  background: #FFFFFF !important;
  color: #1A4A6E !important;
  border: 1px solid #C5D4E3 !important;
  box-shadow: none !important;
  min-height: 2.2rem;
}

[data-testid="stImage"] { margin-top: 10px; }
[data-testid="stImage"] img { max-height: 32px; width: auto; }

[data-testid="stHorizontalBlock"]:has(.file-chip) [data-testid="column"]:first-child [data-testid="stImage"] {
  margin: 0 !important;
}
[data-testid="stHorizontalBlock"]:has(.file-chip) [data-testid="column"]:first-child [data-testid="stImage"] img {
  max-height: 36px !important;
  width: 36px !important;
  height: 36px !important;
  object-fit: contain;
}

.footer-bar {
  margin-top: 28px;
  padding-top: 12px;
  border-top: 1px solid #E2E8F0;
}

[data-testid="stHorizontalBlock"]:has(.footer-credits) {
  align-items: center;
  margin-top: 0;
}

.footer-credits {
  text-align: right;
  font-family: "Outfit", sans-serif;
  font-size: 0.66rem;
  line-height: 1.45;
  color: #9AA5B1;
}

.footer-credits .renzo {
  margin-top: 2px;
  color: #8A96A3;
}

[data-testid="stExpander"] {
  margin-top: 1rem;
  border: 1px solid #D5DEE8 !important;
  border-radius: 8px !important;
  background: #FFFFFF;
  box-shadow:
    0 1px 0 rgba(255, 255, 255, 0.8) inset,
    0 4px 12px rgba(12, 38, 68, 0.05);
}

[data-testid="stExpander"] details {
  border: none !important;
}

[data-testid="stExpander"] summary {
  font-family: "Outfit", sans-serif !important;
  font-size: 0.95rem !important;
  font-weight: 500 !important;
  color: #1A4A6E !important;
  padding: 0.65rem 0.85rem !important;
}

[data-testid="stExpander"] summary:hover {
  color: #0C2644 !important;
}

[data-testid="stExpander"] [data-testid="stExpanderDetails"] {
  padding: 0.25rem 0.5rem 0.65rem !important;
  border-top: 1px solid #E8EEF3;
}

@media (prefers-reduced-motion: reduce) {
  .block-container,
  div[data-testid="stVerticalBlockBorderWrapper"],
  .file-chip { animation: none; }
  div.stButton > button:hover,
  div.stDownloadButton > button:hover { transform: none; }
  body.compresor-dragging [data-testid="stVerticalBlockBorderWrapper"]:has([data-testid="stFileUploaderDropzone"])::before {
    backdrop-filter: none;
    -webkit-backdrop-filter: none;
    background: rgba(244, 246, 248, 0.88);
  }
}
</style>
""",
    unsafe_allow_html=True,
)


@dataclass
class HeldFile:
    name: str
    size: int
    data: bytes


def as_file_list(value) -> list:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def ingest_uploads(uploaded) -> bool:
    """Suma archivos nuevos al lote. Devuelve True si cambió."""
    managed: list[HeldFile] = list(st.session_state.get("managed") or [])
    seen = {(f.name, f.size) for f in managed}
    changed = False
    overflow = False
    too_large: str | None = None
    for f in as_file_list(uploaded):
        key = (f.name, f.size)
        if key in seen:
            continue
        if len(managed) >= MAX_FILES:
            overflow = True
            break
        if f.size > MAX_INPUT_BYTES:
            too_large = (
                f"{f.name} pesa {format_size(f.size)}. "
                f"El tamaño máximo es {format_size(MAX_INPUT_BYTES)}."
            )
            continue
        managed.append(HeldFile(name=f.name, size=f.size, data=f.getvalue()))
        seen.add(key)
        changed = True
    st.session_state.managed = managed
    st.session_state.too_many = overflow
    st.session_state.too_large = too_large
    return changed


def bump_uploader() -> None:
    st.session_state.uploader_rev = int(st.session_state.get("uploader_rev") or 0) + 1


def reset_result() -> None:
    st.session_state.compress_result = None
    st.session_state.compress_error = None
    st.session_state.processing = False


def remove_file(index: int) -> None:
    managed = list(st.session_state.get("managed") or [])
    if 0 <= index < len(managed):
        managed.pop(index)
    st.session_state.managed = managed
    st.session_state.too_many = False
    st.session_state.too_large = None
    bump_uploader()
    reset_result()


def clear_all_files() -> None:
    st.session_state.managed = []
    st.session_state.too_many = False
    st.session_state.too_large = None
    bump_uploader()
    reset_result()


def render_upload_alerts() -> None:
    if st.session_state.get("too_many"):
        ui.alert(
            "Máximo 5 archivos",
            description="Quitá algunos para continuar.",
            variant="destructive",
            key="too_many_alert",
        )
    too_large = st.session_state.get("too_large")
    if too_large:
        ui.alert(
            "Archivo demasiado grande",
            description=str(too_large),
            variant="destructive",
            key="too_large_alert",
        )


def inject_dropzone_enhancer() -> None:
    """Detecta drag de archivos y agranda la zona de soltado a todo el componente."""
    components.html(
        """
<script>
(function () {
  const doc = window.parent.document;
  if (doc.documentElement.dataset.compresorDropbound === "1") return;
  doc.documentElement.dataset.compresorDropbound = "1";

  let depth = 0;

  const isFileDrag = (e) => {
    try {
      const types = e.dataTransfer && e.dataTransfer.types;
      if (!types) return false;
      return Array.from(types).includes("Files");
    } catch (_) {
      return false;
    }
  };

  const findWrap = () =>
    doc.querySelector(
      '[data-testid="stVerticalBlockBorderWrapper"]:has([data-testid="stFileUploaderDropzone"])'
    );

  const uploaderVisible = () => {
    const dz = doc.querySelector('[data-testid="stFileUploaderDropzone"]');
    if (!dz) return false;
    const style = window.parent.getComputedStyle(dz);
    const hiddenParent = dz.closest('[data-testid="stFileUploader"]');
    if (hiddenParent) {
      const ps = window.parent.getComputedStyle(hiddenParent);
      if (ps.display === "none" || ps.visibility === "hidden") return false;
    }
    return style.display !== "none" && style.visibility !== "hidden" && dz.offsetHeight > 0;
  };

  const clearUploaderInline = () => {
    doc.querySelectorAll('[data-testid="stFileUploader"]').forEach((el) => {
      el.style.removeProperty("position");
      el.style.removeProperty("left");
      el.style.removeProperty("top");
      el.style.removeProperty("width");
      el.style.removeProperty("height");
      el.style.removeProperty("z-index");
      el.style.removeProperty("margin");
    });
  };

  const setDrag = (on) => {
    const wrap = findWrap();
    const uploader = wrap && wrap.querySelector('[data-testid="stFileUploader"]');

    if (!on || !uploaderVisible() || !wrap || !uploader) {
      doc.body.classList.remove("compresor-dragging");
      clearUploaderInline();
      return;
    }

    doc.body.classList.add("compresor-dragging");
    const r = wrap.getBoundingClientRect();
    uploader.style.position = "fixed";
    uploader.style.left = r.left + "px";
    uploader.style.top = r.top + "px";
    uploader.style.width = r.width + "px";
    uploader.style.height = r.height + "px";
    uploader.style.zIndex = "40";
    uploader.style.margin = "0";
  };

  doc.addEventListener("dragenter", (e) => {
    if (!isFileDrag(e)) return;
    e.preventDefault();
    depth += 1;
    setDrag(true);
  }, true);

  doc.addEventListener("dragover", (e) => {
    if (!isFileDrag(e)) return;
    e.preventDefault();
    setDrag(true);
  }, true);

  doc.addEventListener("dragleave", (e) => {
    if (!isFileDrag(e)) return;
    depth = Math.max(0, depth - 1);
    if (depth === 0) setDrag(false);
  }, true);

  const clear = () => {
    depth = 0;
    setDrag(false);
  };

  doc.addEventListener("drop", clear, true);
  doc.addEventListener("dragend", clear, true);
  window.parent.addEventListener("blur", clear);
})();
</script>
        """,
        height=0,
        width=0,
    )


def step_copy(step: int, n_files: int) -> tuple[str, str]:
    if step == 1:
        return (
            "Subí los archivos",
            "Hasta 5 · PDF o imágenes",
        )
    if step == 2:
        if n_files <= 1:
            return ("Comprimí", "Tocá el botón de la derecha.")
        return (
            "Uní y comprimí",
            f"{n_files} archivos → un PDF bajo 1 MB.",
        )
    return ("Descargá", "Listo para el trámite.")


def render_step_header(step: int, n_files: int) -> None:
    title, help_text = step_copy(step, n_files)
    dots = "".join(
        f'<span class="{"done" if i < step else "current" if i == step else "todo"}"></span>'
        for i in range(1, 4)
    )
    st.markdown(
        '<div id="paso-actual">'
        '<div class="wizard-top">'
        '<div class="wizard-title-row">'
        f'<p class="wizard-title">{title}</p>'
        f'<p class="wizard-help">{help_text}</p>'
        "</div>"
        f'<div class="wizard-dots">{dots}</div>'
        "</div>"
        "</div>",
        unsafe_allow_html=True,
    )


def short_name(name: str, max_len: int = 42) -> str:
    if len(name) <= max_len:
        return name
    ext = Path(name).suffix
    keep = max(12, max_len - len(ext) - 1)
    return f"{name[:keep]}…{ext}"


def icon_path(name: str) -> Path:
    ext = Path(name).suffix.lower()
    if ext in IMAGE_EXTS:
        return ICONS_DIR / "image.png"
    return ICONS_DIR / "document.png"


def render_file_rows(files: list[HeldFile], *, allow_remove: bool) -> None:
    for i, held in enumerate(files[:MAX_FILES]):
        ico, chip, action = st.columns((0.14, 1, 0.16), vertical_alignment="center", gap="small")
        with ico:
            glyph = icon_path(held.name)
            if glyph.exists():
                st.image(glyph, width=36)
        with chip:
            st.html(
                "<style>"
                ".file-chip{display:flex;align-items:center;width:100%;box-sizing:border-box;"
                "padding:10px 12px;background:#fff;border:1px solid #D5DEE8;border-radius:8px;"
                "font-family:Outfit,Helvetica Neue,sans-serif}"
                ".file-chip .body{min-width:0;flex:1;display:flex;flex-direction:column;gap:2px}"
                ".file-chip .name{color:#0C2644;font-size:.86rem;font-weight:500;overflow:hidden;"
                "text-overflow:ellipsis;white-space:nowrap}"
                ".file-chip .meta{color:#5A6B7A;font-size:.75rem}"
                "</style>"
                '<div class="file-chip"><span class="body">'
                f'<span class="name">{html.escape(short_name(held.name))}</span>'
                f'<span class="meta">{format_size(held.size)}</span>'
                "</span></div>"
            )
        with action:
            if allow_remove and st.button(
                "×",
                type="secondary",
                key=f"rm_{i}_{held.size}_{held.name}",
                help=f"Quitar {held.name}",
                use_container_width=True,
            ):
                remove_file(i)
                st.rerun()


# --- Hero compacto ---
st.markdown('<h1 class="hero-title">Compresor de archivos</h1>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="welcome">
      <p>
        Las plataformas municipales rechazan archivos de más de 1 MB.
        Subí hasta 5, comprimilos acá y descargá el resultado para el trámite.
        Todo corre en la red interna: el archivo no sale de los servidores ni se guarda.
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)

if "managed" not in st.session_state:
    st.session_state.managed = []
if "uploader_rev" not in st.session_state:
    st.session_state.uploader_rev = 0

files: list[HeldFile] = list(st.session_state.managed)
has_result = st.session_state.get("compress_result") is not None
if not files:
    step = 1
elif has_result:
    step = 3
else:
    step = 2

UPLOAD_TYPES = ["pdf", "jpg", "jpeg", "png", "webp", "bmp", "tif", "tiff", "gif", "heic", "heif"]
show_uploader = step < 3 and len(files) < MAX_FILES

if step == 3 or not show_uploader:
    st.markdown(
        """
        <style>
        [data-testid='stFileUploader']{
          display:none!important; height:0!important; margin:0!important;
          padding:0!important; overflow:hidden!important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

with st.container(border=True):
    render_step_header(step, len(files))

    def mount_uploader():
        return st.file_uploader(
            "Elegí archivos",
            type=UPLOAD_TYPES,
            accept_multiple_files=True,
            label_visibility="collapsed",
            key=f"upload_{st.session_state.uploader_rev}",
        )

    go = False
    result = st.session_state.get("compress_result")
    too_many = bool(st.session_state.get("too_many"))

    if step == 1:
        uploaded = mount_uploader()
        if ingest_uploads(uploaded):
            st.rerun()
        files = list(st.session_state.managed)
        too_many = bool(st.session_state.get("too_many"))
        render_upload_alerts()
        if files:
            render_file_rows(files, allow_remove=True)
            if st.button("Quitar todos", type="secondary", key="clear_all_1"):
                clear_all_files()
                st.rerun()
    else:
        col_info, col_action = st.columns((1.35, 0.9), gap="medium")

        with col_info:
            if show_uploader:
                uploaded = mount_uploader()
                if ingest_uploads(uploaded):
                    reset_result()
                    st.rerun()
                files = list(st.session_state.managed)
                too_many = bool(st.session_state.get("too_many"))
            else:
                # Hay que montar el widget con la misma key para no perder el lote.
                mount_uploader()

            render_upload_alerts()

            if files:
                render_file_rows(files, allow_remove=step == 2)
                if step == 2 and st.button("Quitar todos", type="secondary", key="clear_all_2"):
                    clear_all_files()
                    st.rerun()

            if st.session_state.get("processing"):
                n = len(files)
                msg = "Comprimiendo…" if n <= 1 else "Uniendo y comprimiendo…"
                st.markdown(f'<p class="process-note">{msg}</p>', unsafe_allow_html=True)

            if st.session_state.get("compress_error"):
                ui.alert(
                    "No se pudo comprimir",
                    description=st.session_state.compress_error,
                    variant="destructive",
                    key="err",
                )

            result = st.session_state.get("compress_result")
            if result is not None and step == 3:
                saved = result.original_size - result.final_size
                st.markdown(
                    '<div class="metrics-line">'
                    f"<span>Original <strong>{format_size(result.original_size)}</strong></span>"
                    f"<span>Resultado <strong>{format_size(result.final_size)}</strong></span>"
                    f"<span>Techo <strong>{format_size(TARGET_BYTES)}</strong></span>"
                    "</div>",
                    unsafe_allow_html=True,
                )
                if result.already_ok:
                    st.caption("Ya estaba bajo 1 MB. Se entrega como versión comprimida.")
                elif result.under_limit:
                    st.caption(result.note or f"Ahorro: {format_size(max(saved, 0))}.")
                else:
                    st.caption(
                        result.note or "Quedó por encima de 1 MB; se entrega lo más liviano posible."
                    )

        with col_action:
            if step == 2 and files and not too_many and not st.session_state.get("processing"):
                label = "Comprimir" if len(files) == 1 else "Unir y comprimir"
                go = st.button(label, type="primary", use_container_width=True)
            elif step == 3 and result is not None:
                mime = (
                    "application/pdf"
                    if result.filename.lower().endswith(".pdf")
                    else "application/octet-stream"
                )
                st.download_button(
                    "Descargar",
                    data=result.data,
                    file_name=result.filename,
                    mime=mime,
                    type="primary",
                    use_container_width=True,
                )
                if st.button("Empezar de nuevo", use_container_width=True):
                    clear_all_files()
                    st.rerun()

    if go:
        st.session_state.processing = True
        st.session_state.compress_error = None
        st.rerun()

    if st.session_state.get("processing") and files and not too_many:
        items = []
        bad = None
        for held in files[:MAX_FILES]:
            if not supported_extension(held.name):
                bad = f"Formato no soportado: {held.name}"
                break
            items.append((held.data, held.name))

        if bad:
            st.session_state.compress_result = None
            st.session_state.compress_error = bad
            st.session_state.processing = False
            st.rerun()
        else:
            try:
                st.session_state.compress_result = compress_uploads(items)
                st.session_state.compress_error = None
            except ValueError as exc:
                st.session_state.compress_result = None
                st.session_state.compress_error = str(exc)
            except Exception:
                st.session_state.compress_result = None
                st.session_state.compress_error = (
                    "No se pudo procesar. Probá con menos archivos o un PDF más corto."
                )
            finally:
                st.session_state.processing = False
            st.rerun()

if show_uploader:
    inject_dropzone_enhancer()

# Animación de funcionamiento debajo de la herramienta (solo en paso 1).
if step == 1:
    with st.expander("¿Para qué sirve este compresor?", expanded=False):
        render_explainer()

st.markdown('<div class="footer-bar"></div>', unsafe_allow_html=True)
foot_logo, foot_copy = st.columns((1, 2), vertical_alignment="center")
with foot_logo:
    if LOGO.exists():
        st.image(str(LOGO), width=160)
with foot_copy:
    st.markdown(
        """
        <div class="footer-credits">
          <div>© 2026 Atención Ciudadana de la Municipalidad de Santa Fe. Todos los derechos reservados.</div>
          <div class="renzo">Desarrollado y mantenido por Renzo.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

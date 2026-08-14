from pathlib import Path

import html

import streamlit as st
import streamlit_shadcn_ui as ui

from compressor import (
    MAX_FILES,
    TARGET_BYTES,
    compress_uploads,
    format_size,
    supported_extension,
)

ROOT = Path(__file__).resolve().parent
LOGO = ROOT / "assets" / "brand" / "msf-horizontal.png"
ICON = ROOT / "assets" / "brand" / "msf-icon.png"

st.set_page_config(
    page_title="Compresor de archivos — Atención Ciudadana",
    page_icon=str(ICON) if ICON.exists() else None,
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&display=swap');

.stApp {
  background: #F4F6F8;
  color: #0C1929;
  font-family: "Outfit", "Helvetica Neue", sans-serif;
}

.stApp::before {
  content: "";
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
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
.viewerBadge_container__1QSob,
.viewerBadge_link__1S137,
.viewerBadge_text__1JaDK,
.styles_viewerBadge__1yB5_,
[class*="viewerBadge"],
[class*="ViewerBadge"],
[data-testid="stBaseButton-headerNoPadding"] {
  display: none !important;
  visibility: hidden !important;
  pointer-events: none !important;
}

.block-container {
  max-width: 980px;
  padding-top: 40px;
  padding-bottom: 32px;
  animation: enter 480ms cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes enter {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: none; }
}

@keyframes stepIn {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: none; }
}

h1, .hero-title {
  font-family: "Outfit", sans-serif !important;
  font-weight: 650 !important;
  font-size: clamp(2.6rem, 5vw, 3.6rem) !important;
  line-height: 1.08 !important;
  letter-spacing: -0.03em !important;
  color: #0C2644 !important;
  margin: 0 0 1.25rem 0 !important;
  text-shadow:
    0 1px 0 rgba(255, 255, 255, 0.9),
    0 8px 22px rgba(12, 38, 68, 0.14);
}

.welcome {
  color: #2C3D4F;
  font-size: 0.95rem;
  line-height: 1.55;
  max-width: 22rem;
  font-family: "Outfit", sans-serif;
}

.welcome p {
  margin: 0;
}

.step-card {
  background: #FFFFFF;
  border: 1px solid #D5DEE8;
  border-radius: 10px;
  padding: 18px 18px 16px;
  box-shadow:
    0 1px 0 rgba(255, 255, 255, 0.8) inset,
    0 8px 20px rgba(12, 38, 68, 0.06);
  animation: stepIn 380ms cubic-bezier(0.16, 1, 0.3, 1);
}

.wizard-dots {
  display: flex;
  gap: 6px;
  margin: 0 0 12px 0;
}

.wizard-dots span {
  display: block;
  width: 28px;
  height: 3px;
  border-radius: 2px;
  background: #D5DEE8;
  transition: background 200ms ease;
}

.wizard-dots span.done,
.wizard-dots span.current {
  background: #1A4A6E;
}

.wizard-kicker {
  margin: 0 0 2px 0;
  color: #1A4A6E;
  font-size: 0.72rem;
  font-weight: 500;
  font-family: "Outfit", sans-serif;
}

.wizard-title {
  margin: 0 0 4px 0;
  color: #0C2644;
  font-size: 1.1rem;
  font-weight: 600;
  font-family: "Outfit", sans-serif;
  letter-spacing: -0.02em;
}

.wizard-help {
  margin: 0 0 14px 0;
  color: #5A6B7A;
  font-size: 0.84rem;
  line-height: 1.4;
  font-family: "Outfit", sans-serif;
}

.file-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin: 0 0 14px 0;
}

.file-chip {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 12px;
  padding: 10px 12px;
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-left: 3px solid #1A4A6E;
  border-radius: 8px;
  font-family: "Outfit", sans-serif;
  animation: stepIn 280ms cubic-bezier(0.16, 1, 0.3, 1);
}

.file-chip .name {
  color: #0C2644;
  font-size: 0.88rem;
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.file-chip .meta {
  color: #5A6B7A;
  font-size: 0.78rem;
  flex-shrink: 0;
}

.process-note {
  margin: 0 0 12px 0;
  padding: 10px 12px;
  background: #F0F4F8;
  border: 1px solid #C5D4E3;
  border-radius: 8px;
  color: #1A4A6E;
  font-size: 0.86rem;
  font-family: "Outfit", sans-serif;
  animation: stepIn 240ms ease;
}

.result-block {
  margin-top: 4px;
  animation: stepIn 380ms cubic-bezier(0.16, 1, 0.3, 1);
}

[data-testid="stIconMaterial"] {
  font-family: "Material Symbols Rounded", "Material Symbols Outlined" !important;
  font-weight: 400 !important;
  font-style: normal !important;
  letter-spacing: normal !important;
  text-transform: none !important;
}

[data-testid="stFileUploader"] section,
[data-testid="stFileUploaderDropzone"] {
  background: #FFFFFF !important;
  border: 1px solid #D5DEE8 !important;
  border-radius: 8px !important;
}

[data-testid="stFileUploaderDropzone"] {
  position: relative !important;
  min-height: 72px !important;
  cursor: pointer;
}

[data-testid="stFileUploaderDropzone"] > * {
  opacity: 0 !important;
}

[data-testid="stFileUploaderDropzone"]::after {
  content: "Arrastrá archivos o hacé clic (hasta 5)";
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 14px;
  color: #1A4A6E;
  font-family: "Outfit", sans-serif;
  font-size: 0.9rem;
  font-weight: 500;
  pointer-events: none;
  text-align: center;
}

[data-testid="stFileUploaderDropzone"]:hover {
  border-color: #1A4A6E !important;
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
div.stDownloadButton > button,
[data-testid="stBaseButton-primary"],
[data-testid="baseButton-primary"] {
  background: #1A4A6E !important;
  color: #FFFFFF !important;
  border: 1px solid #1A4A6E !important;
  border-radius: 6px !important;
  font-family: "Outfit", sans-serif !important;
  font-weight: 500 !important;
  box-shadow: 0 2px 6px rgba(12, 38, 68, 0.12) !important;
  min-height: 2.5rem;
  width: 100%;
  transition: background 180ms ease, border-color 180ms ease, transform 140ms ease;
}

div.stButton > button:hover,
div.stDownloadButton > button:hover,
[data-testid="stBaseButton-primary"]:hover,
[data-testid="baseButton-primary"]:hover {
  background: #0C2644 !important;
  border-color: #0C2644 !important;
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

[data-testid="stImage"] {
  margin-top: 14px;
}

[data-testid="stImage"] img {
  max-height: 36px;
  width: auto;
}

.legal {
  margin-top: 40px;
  padding-top: 16px;
  border-top: 1px solid #E2E8F0;
  color: #7A8794;
  font-size: 0.7rem;
  line-height: 1.6;
  max-width: 40rem;
  font-family: "Outfit", sans-serif;
}

.copy, .renzo {
  font-family: "Outfit", sans-serif;
  font-size: 0.68rem;
}

.copy {
  margin-top: 10px;
  color: #9AA5B1;
}

.renzo {
  margin-top: 2px;
  color: #8A96A3;
}

@media (prefers-reduced-motion: reduce) {
  .block-container, .step-card, .file-chip, .result-block, .process-note {
    animation: none;
  }
  div.stButton > button:hover,
  div.stDownloadButton > button:hover {
    transform: none;
  }
}
</style>
""",
    unsafe_allow_html=True,
)


def as_file_list(value) -> list:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def batch_id(files) -> str | None:
    if not files:
        return None
    return "|".join(f"{f.name}:{f.size}" for f in files)


def step_copy(step: int, n_files: int) -> tuple[str, str, str]:
    if step == 1:
        return (
            "Paso 1 de 3",
            "Subí los archivos",
            "Hasta 5 archivos. PDF o imágenes. Máximo 80 MB cada uno.",
        )
    if step == 2:
        if n_files <= 1:
            return (
                "Paso 2 de 3",
                "Comprimí",
                "Tocá Comprimir para dejarlo bajo 1 MB.",
            )
        return (
            "Paso 2 de 3",
            "Uní y comprimí",
            f"{n_files} archivos. Se unen en un PDF y se comprimen a menos de 1 MB.",
        )
    return (
        "Paso 3 de 3",
        "Descargá",
        "Listo. Descargá el archivo para el trámite.",
    )


def render_step_header(step: int, n_files: int) -> None:
    kicker, title, help_text = step_copy(step, n_files)
    dots = "".join(
        f'<span class="{"done" if i < step else "current" if i == step else "todo"}"></span>'
        for i in range(1, 4)
    )
    st.markdown(
        f"""
        <div id="paso-actual">
          <div class="wizard-dots">{dots}</div>
          <p class="wizard-kicker">{kicker}</p>
          <p class="wizard-title">{title}</p>
          <p class="wizard-help">{help_text}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_file_chips(files) -> None:
    rows = []
    for f in files[:MAX_FILES]:
        rows.append(
            f"""
            <div class="file-chip">
              <span class="name">{html.escape(f.name)}</span>
              <span class="meta">{format_size(f.size)}</span>
            </div>
            """
        )
    st.markdown(f'<div class="file-list">{"".join(rows)}</div>', unsafe_allow_html=True)


def scroll_to_step() -> None:
    # Script inyectado: Streamlit a veces lo filtra; si no corre, no rompe la UI.
    st.markdown(
        """
        <img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
             width="0" height="0" alt=""
             onload="
               (function(){
                 var d = window.parent && window.parent.document ? window.parent.document : document;
                 var el = d.getElementById('paso-actual');
                 if (el) { el.scrollIntoView({ behavior: 'smooth', block: 'nearest' }); }
               })();
             " />
        """,
        unsafe_allow_html=True,
    )


# --- Hero ---
st.markdown('<h1 class="hero-title">Compresor de archivos</h1>', unsafe_allow_html=True)

left, right = st.columns((0.95, 1.15), gap="large")

with left:
    st.markdown(
        """
        <div class="welcome">
          <p>Dejá el archivo bajo 1&nbsp;MB. Se procesa en la red interna.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right:
    # El widget ya vive en session_state antes del rerender
    files = as_file_list(st.session_state.get("upload"))
    current_id = batch_id(files)
    if st.session_state.get("file_id") != current_id:
        st.session_state.file_id = current_id
        st.session_state.compress_result = None
        st.session_state.compress_error = None
        st.session_state.processing = False

    has_result = st.session_state.get("compress_result") is not None
    if not files:
        step = 1
    elif has_result:
        step = 3
    else:
        step = 2

    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    render_step_header(step, len(files))

    if step == 3:
        st.markdown(
            "<style>[data-testid='stFileUploader']{display:none!important}</style>",
            unsafe_allow_html=True,
        )

    # Siempre montar el uploader para no perder el lote en session_state
    uploaded = st.file_uploader(
        "Elegí archivos",
        type=["pdf", "jpg", "jpeg", "png", "webp", "bmp", "tif", "tiff", "gif", "heic", "heif"],
        accept_multiple_files=True,
        label_visibility="collapsed",
        key="upload",
    )
    files = as_file_list(uploaded)

    current_id = batch_id(files)
    if st.session_state.get("file_id") != current_id:
        st.session_state.file_id = current_id
        st.session_state.compress_result = None
        st.session_state.compress_error = None
        st.session_state.processing = False
        has_result = False
        if files:
            step = 2
        else:
            step = 1

    too_many = len(files) > MAX_FILES
    if too_many:
        ui.alert(
            "Máximo 5 archivos",
            description="Quitá algunos para continuar.",
            variant="destructive",
            key="too_many",
        )

    if files and step >= 2:
        render_file_chips(files)

    if st.session_state.get("processing"):
        n = len(files)
        msg = "Comprimiendo…" if n <= 1 else "Uniendo y comprimiendo…"
        st.markdown(f'<p class="process-note">{msg}</p>', unsafe_allow_html=True)

    go = False
    if step == 2 and files and not too_many and not st.session_state.get("processing"):
        label = "Comprimir" if len(files) == 1 else "Unir y comprimir"
        go = st.button(label, type="primary")

    if go:
        st.session_state.processing = True
        st.session_state.compress_error = None
        st.rerun()

    if st.session_state.get("processing") and files and not too_many:
        items = []
        bad = None
        for f in files[:MAX_FILES]:
            name = f.name or "archivo"
            if not supported_extension(name):
                bad = f"Formato no soportado: {name}"
                break
            items.append((f.getvalue(), name))

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

    if st.session_state.get("compress_error"):
        ui.alert(
            "No se pudo comprimir",
            description=st.session_state.compress_error,
            variant="destructive",
            key="err",
        )

    result = st.session_state.get("compress_result")
    if result is not None and (step == 3 or has_result):
        saved = result.original_size - result.final_size
        st.markdown('<div class="result-block">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            ui.metric_card("Original", format_size(result.original_size), key="m_orig")
        with c2:
            ui.metric_card("Resultado", format_size(result.final_size), key="m_out")
        with c3:
            ui.metric_card("Techo", format_size(TARGET_BYTES), key="m_cap")

        if result.already_ok:
            ui.alert(
                "Ya estaba por debajo de 1 MB",
                description="Se entrega con el nombre de versión comprimida.",
                key="ok_passthrough",
            )
        elif result.under_limit:
            extra = result.note or f"Ahorro: {format_size(max(saved, 0))}."
            ui.alert("Listo para descargar", description=extra, key="ok_done")
        else:
            ui.alert(
                "Quedó por encima de 1 MB",
                description=result.note or "Se entrega la versión más liviana posible.",
                variant="destructive",
                key="warn_over",
            )

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
        )
        if st.button("Empezar de nuevo"):
            st.session_state.compress_result = None
            st.session_state.compress_error = None
            st.session_state.processing = False
            st.session_state.file_id = None
            if "upload" in st.session_state:
                del st.session_state["upload"]
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.get("last_step") != step:
        st.session_state.last_step = step
        scroll_to_step()

st.markdown(
    """
    <div class="legal">
      Compresor de <strong>Atención Ciudadana</strong>. Los archivos se procesan
      de forma temporal, sin almacenamiento persistente. Hasta 5 archivos se pueden
      unir en un PDF. La calidad visual puede reducirse para respetar el límite de 1&nbsp;MB.
    </div>
    <p class="copy">© 2026 Atención Ciudadana de la Municipalidad de Santa Fe. Todos los derechos reservados.</p>
    <p class="renzo">Desarrollado y mantenido por Renzo.</p>
    """,
    unsafe_allow_html=True,
)
if LOGO.exists():
    st.image(str(LOGO), width=180)

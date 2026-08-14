from pathlib import Path

import html

import streamlit as st
import streamlit_shadcn_ui as ui

from compressor import (
    TARGET_BYTES,
    compress_file,
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
[data-testid="stHeaderActionElements"] {
  display: none !important;
  visibility: hidden;
}

.block-container {
  max-width: 1080px;
  padding-top: 56px;
  padding-bottom: 40px;
  animation: enter 480ms cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes enter {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: none; }
}

h1 {
  font-family: "Outfit", sans-serif !important;
  font-weight: 650 !important;
  font-size: clamp(2.4rem, 4.2vw, 3.35rem) !important;
  line-height: 1.12 !important;
  letter-spacing: -0.03em !important;
  color: #0C2644 !important;
  margin: 0 0 0.85rem 0 !important;
}

.kicker {
  margin: 0 0 0.5rem 0;
  color: #1A4A6E;
  font-size: 0.82rem;
  font-weight: 500;
  font-family: "Outfit", sans-serif;
}

.welcome {
  color: #2C3D4F;
  font-size: 1rem;
  line-height: 1.6;
  max-width: 34rem;
  font-family: "Outfit", sans-serif;
}

.welcome p {
  margin: 0;
}

.wizard {
  margin: 0 0 18px 0;
  animation: enter 380ms cubic-bezier(0.16, 1, 0.3, 1);
}

.wizard-dots {
  display: flex;
  gap: 6px;
  margin: 0 0 14px 0;
}

.wizard-dots span {
  display: block;
  width: 22px;
  height: 3px;
  border-radius: 2px;
  background: #D5DEE8;
}

.wizard-dots span.done,
.wizard-dots span.current {
  background: #1A4A6E;
}

.wizard-kicker {
  margin: 0 0 4px 0;
  color: #1A4A6E;
  font-size: 0.75rem;
  font-weight: 500;
  font-family: "Outfit", sans-serif;
}

.wizard-title {
  margin: 0 0 6px 0;
  color: #0C2644;
  font-size: 1.15rem;
  font-weight: 600;
  font-family: "Outfit", sans-serif;
  letter-spacing: -0.02em;
}

.wizard-help {
  margin: 0;
  color: #5A6B7A;
  font-size: 0.88rem;
  line-height: 1.45;
  font-family: "Outfit", sans-serif;
}

.file-ready {
  margin: 12px 0;
  padding: 12px 14px;
  background: #FFFFFF;
  border: 1px solid #C5D4E3;
  border-left: 3px solid #1A4A6E;
  border-radius: 8px;
  animation: enter 320ms cubic-bezier(0.16, 1, 0.3, 1);
  font-family: "Outfit", sans-serif;
}

.file-ready .name {
  color: #0C2644;
  font-size: 0.95rem;
  font-weight: 500;
}

.file-ready .meta {
  margin-top: 4px;
  color: #5A6B7A;
  font-size: 0.82rem;
}

.result-block {
  margin-top: 8px;
  animation: enter 380ms cubic-bezier(0.16, 1, 0.3, 1);
}

[data-testid="stIconMaterial"] {
  font-family: "Material Symbols Rounded", "Material Symbols Outlined" !important;
  font-weight: 400 !important;
  font-style: normal !important;
  letter-spacing: normal !important;
  text-transform: none !important;
}

[data-testid="stWidgetLabel"] p {
  font-family: "Outfit", sans-serif !important;
  color: #0C2644 !important;
  font-weight: 500 !important;
  font-size: 0.9rem !important;
}

[data-testid="stFileUploader"] section,
[data-testid="stFileUploaderDropzone"] {
  background: #FFFFFF !important;
  border: 1px solid #D5DEE8 !important;
  border-radius: 8px !important;
}

[data-testid="stFileUploaderDropzone"] {
  position: relative !important;
  min-height: 96px !important;
  cursor: pointer;
}

[data-testid="stFileUploaderDropzone"] > * {
  opacity: 0 !important;
}

[data-testid="stFileUploaderDropzone"]::after {
  content: "Arrastrá un archivo o hacé clic para elegir";
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 16px;
  color: #1A4A6E;
  font-family: "Outfit", sans-serif;
  font-size: 0.95rem;
  font-weight: 500;
  pointer-events: none;
}

[data-testid="stFileUploaderDropzone"]:hover {
  border-color: #1A4A6E !important;
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
  box-shadow: none !important;
  min-height: 2.6rem;
  transition: background 180ms ease, border-color 180ms ease, transform 140ms ease;
}

div.stButton > button:hover,
div.stDownloadButton > button:hover,
[data-testid="stBaseButton-primary"]:hover,
[data-testid="baseButton-primary"]:hover {
  background: #0C2644 !important;
  border-color: #0C2644 !important;
  color: #FFFFFF !important;
}

div.stButton > button:disabled,
[data-testid="stBaseButton-primary"]:disabled,
[data-testid="baseButton-primary"]:disabled {
  background: #1A4A6E !important;
  border-color: #1A4A6E !important;
  color: #FFFFFF !important;
  opacity: 0.45;
}

div.stDownloadButton > button {
  width: 100%;
}

[data-testid="stStatus"] {
  border: 1px solid #C5D4E3 !important;
  border-radius: 8px !important;
  background: #FFFFFF !important;
}

[data-testid="stImage"] {
  margin-top: 18px;
}

[data-testid="stImage"] img {
  max-height: 40px;
  width: auto;
}

.legal {
  margin-top: 56px;
  padding-top: 22px;
  border-top: 1px solid #E2E8F0;
  color: #7A8794;
  font-size: 0.75rem;
  line-height: 1.65;
  max-width: 42rem;
  font-family: "Outfit", sans-serif;
}

.copy, .renzo {
  font-family: "Outfit", sans-serif;
  font-size: 0.72rem;
}

.copy {
  margin-top: 14px;
  color: #9AA5B1;
}

.renzo {
  margin-top: 4px;
  color: #8A96A3;
}

@media (prefers-reduced-motion: reduce) {
  .block-container, .file-ready, .result-block, .wizard { animation: none; }
}
</style>
""",
    unsafe_allow_html=True,
)

WIZARD = {
    1: (
        "Paso 1 de 3",
        "Subí el archivo",
        "Arrastralo o hacé clic. Hasta 80 MB.",
    ),
    2: (
        "Paso 2 de 3",
        "Comprimí",
        "El archivo está cargado. Tocá Comprimir para dejarlo bajo 1 MB.",
    ),
    3: (
        "Paso 3 de 3",
        "Descargá",
        "Listo. Descargá el archivo para el trámite.",
    ),
}


def render_wizard(step: int) -> None:
    kicker, title, help_text = WIZARD[step]
    dots = "".join(
        f'<span class="{"done" if i < step else "current" if i == step else "todo"}"></span>'
        for i in range(1, 4)
    )
    st.markdown(
        f"""
        <div class="wizard">
          <div class="wizard-dots">{dots}</div>
          <p class="wizard-kicker">{kicker}</p>
          <p class="wizard-title">{title}</p>
          <p class="wizard-help">{help_text}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


left, right = st.columns((1.15, 0.85), gap="large")

with left:
    st.markdown('<p class="kicker">Atención Ciudadana</p>', unsafe_allow_html=True)
    st.title("Compresor de archivos")
    st.markdown(
        """
        <div class="welcome">
          <p>
            Los bots comprimen tu archivo a menos de 1&nbsp;MB para los trámites
            de Atención Ciudadana. El proceso corre en la red interna: el archivo
            no sale de los servidores.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right:
    pending = st.session_state.get("upload")
    file_id = f"{pending.name}-{pending.size}" if pending is not None else None
    if st.session_state.get("file_id") != file_id:
        st.session_state.file_id = file_id
        st.session_state.compress_result = None
        st.session_state.compress_error = None

    has_result = st.session_state.get("compress_result") is not None
    if pending is None:
        step = 1
    elif not has_result:
        step = 2
    else:
        step = 3

    render_wizard(step)

    uploaded = st.file_uploader(
        "Elegí un archivo",
        type=["pdf", "jpg", "jpeg", "png", "webp", "bmp", "tif", "tiff", "gif", "heic", "heif"],
        label_visibility="collapsed",
        key="upload",
    )

    if uploaded is not None and step == 2:
        st.markdown(
            f"""
            <div class="file-ready">
              <div class="name">{html.escape(uploaded.name)}</div>
              <div class="meta">{format_size(uploaded.size)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    go = False
    if step == 2:
        go = st.button("Comprimir", type="primary")

    if go and uploaded is not None:
        raw = uploaded.getvalue()
        name = uploaded.name or "archivo"
        if not supported_extension(name):
            st.session_state.compress_result = None
            st.session_state.compress_error = "Ese formato no se puede comprimir acá."
        else:
            try:
                with st.status("Comprimiendo…", expanded=False) as status:
                    st.session_state.compress_result = compress_file(raw, name)
                    st.session_state.compress_error = None
                    status.update(label="Listo", state="complete")
                st.rerun()
            except ValueError as exc:
                st.session_state.compress_result = None
                st.session_state.compress_error = str(exc)
            except Exception:
                st.session_state.compress_result = None
                st.session_state.compress_error = (
                    "No se pudo procesar el archivo. Probá con otro o con un PDF más corto."
                )

    if st.session_state.get("compress_error"):
        ui.alert(
            "No se pudo comprimir",
            description=st.session_state.compress_error,
            variant="destructive",
            key="err",
        )

    result = st.session_state.get("compress_result")
    if result is not None:
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
                description="No hizo falta modificar el archivo.",
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
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="legal">
      Compresor de <strong>Atención Ciudadana</strong>. Los archivos se procesan
      de forma temporal, sin almacenamiento persistente. La calidad visual puede
      reducirse para respetar el límite de 1&nbsp;MB.
    </div>
    <p class="copy">© 2026 Atención Ciudadana de la Municipalidad de Santa Fe. Todos los derechos reservados.</p>
    <p class="renzo">Desarrollado y mantenido por Renzo.</p>
    """,
    unsafe_allow_html=True,
)
if LOGO.exists():
    st.image(str(LOGO), width=200)

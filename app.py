from pathlib import Path

import html

import streamlit as st
import streamlit_shadcn_ui as ui

from compressor import (
    MAX_INPUT_BYTES,
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

html, body, [class*="st-"], .stApp, p, label, span, div {
  font-family: "Outfit", "Helvetica Neue", sans-serif;
}

.stApp {
  background: #F4F6F8;
  color: #0C1929;
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
  animation: enter 520ms cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes enter {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: none; }
}

h1 {
  font-family: "Outfit", sans-serif !important;
  font-weight: 650 !important;
  font-size: clamp(2.4rem, 4.2vw, 3.35rem) !important;
  line-height: 1.12 !important;
  letter-spacing: -0.03em !important;
  color: #0C2644 !important;
  margin: 0 0 1rem 0 !important;
}

.kicker {
  margin: 0 0 0.55rem 0;
  color: #1A4A6E;
  font-size: 0.82rem;
  font-weight: 500;
}

.welcome {
  color: #2C3D4F;
  font-size: 1rem;
  line-height: 1.65;
  max-width: 36rem;
}

.welcome p {
  margin: 0 0 0.9rem 0;
}

.welcome p:last-child {
  margin-bottom: 0;
}

.steps {
  list-style: none;
  margin: 1.6rem 0 0 0;
  padding: 0;
  max-width: 36rem;
}

.steps li {
  display: flex;
  gap: 14px;
  align-items: baseline;
  padding: 10px 0;
  border-top: 1px solid #E2E8F0;
  color: #2C3D4F;
  font-size: 0.95rem;
}

.steps li:last-child {
  border-bottom: 1px solid #E2E8F0;
}

.steps span {
  color: #1A4A6E;
  font-variant-numeric: tabular-nums;
  font-size: 0.78rem;
  font-weight: 600;
  min-width: 1.6rem;
}

.panel-label {
  margin: 0 0 10px 0;
  color: #1A4A6E;
  font-size: 0.82rem;
  font-weight: 500;
}

.file-ready {
  margin: 0 0 12px 0;
  padding: 12px 14px;
  background: #FFFFFF;
  border: 1px solid #C5D4E3;
  border-left: 3px solid #1A4A6E;
  border-radius: 8px;
  animation: enter 380ms cubic-bezier(0.16, 1, 0.3, 1);
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
  animation: enter 420ms cubic-bezier(0.16, 1, 0.3, 1);
}

[data-testid="stFileUploader"] {
  margin-top: 0;
}

[data-testid="stFileUploader"] > label {
  display: none;
}

[data-testid="stFileUploaderDropzone"] {
  min-height: 200px !important;
  background: #FFFFFF !important;
  border: 1px solid #D5DEE8 !important;
  border-radius: 8px !important;
  padding: 28px 20px !important;
  transition: border-color 200ms ease, background 200ms ease, transform 200ms ease;
}

[data-testid="stFileUploaderDropzone"]:hover {
  border-color: #1A4A6E !important;
  background: #F8FAFC !important;
}

[data-testid="stFileUploader"]:has([data-testid="stFileUploaderFile"]) [data-testid="stFileUploaderDropzone"],
[data-testid="stFileUploader"]:has([data-testid="stFileUploaderFileName"]) [data-testid="stFileUploaderDropzone"] {
  border-color: #1A4A6E !important;
  background: #F3F6FA !important;
}

[data-testid="stFileUploaderDropzone"] button {
  background: #1A4A6E !important;
  color: #FFFFFF !important;
  border: 1px solid #1A4A6E !important;
  border-radius: 6px !important;
  font-family: "Outfit", sans-serif !important;
  font-weight: 500 !important;
  padding: 0.55rem 1.15rem !important;
  box-shadow: none !important;
  transition: background 200ms ease, border-color 200ms ease, transform 160ms ease !important;
}

[data-testid="stFileUploaderDropzone"] button:hover {
  background: #0C2644 !important;
  border-color: #0C2644 !important;
  color: #FFFFFF !important;
}

[data-testid="stFileUploaderDropzone"] button:active {
  transform: scale(0.98) !important;
}

[data-testid="stFileUploaderDropzoneInstructions"] span,
[data-testid="stFileUploaderDropzoneInstructions"] small {
  color: #5A6B7A !important;
  font-size: 0.92rem !important;
}

.stButton > button {
  background: #1A4A6E;
  color: #FFFFFF;
  border: 1px solid #1A4A6E;
  border-radius: 6px;
  font-family: "Outfit", sans-serif;
  font-weight: 500;
  padding: 0.55rem 1.2rem;
  box-shadow: none;
  width: 100%;
  transition: background 200ms ease, border-color 200ms ease, transform 160ms ease;
}

.stButton > button:hover {
  background: #0C2644;
  border-color: #0C2644;
  color: #FFFFFF;
}

.stButton > button:active {
  transform: scale(0.98);
}

.stDownloadButton > button {
  background: #FFFFFF;
  color: #1A4A6E;
  border: 1px solid #C5D4E3;
  border-radius: 6px;
  font-weight: 500;
  box-shadow: none;
  transition: background 200ms ease, border-color 200ms ease, color 200ms ease;
}

.stDownloadButton > button:hover {
  background: #F3F6FA;
  border-color: #1A4A6E;
  color: #0C2644;
}

[data-testid="stStatus"] {
  border: 1px solid #C5D4E3 !important;
  border-radius: 8px !important;
  background: #FFFFFF !important;
  animation: enter 360ms cubic-bezier(0.16, 1, 0.3, 1);
}

[data-testid="stSpinner"] {
  color: #1A4A6E;
}

.stSpinner > div > div {
  border-top-color: #1A4A6E !important;
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
}

.legal strong {
  color: #5A6B7A;
  font-weight: 500;
}

.copy {
  margin-top: 14px;
  color: #9AA5B1;
  font-size: 0.72rem;
}

.renzo {
  margin-top: 4px;
  color: #8A96A3;
  font-size: 0.72rem;
}

@media (prefers-reduced-motion: reduce) {
  .block-container,
  .file-ready,
  .result-block,
  [data-testid="stStatus"] {
    animation: none;
  }
  [data-testid="stFileUploaderDropzone"],
  .stButton > button,
  .stDownloadButton > button,
  [data-testid="stFileUploaderDropzone"] button {
    transition: none !important;
  }
}
</style>
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
            Bienvenido al Compresor de archivos de Atención Ciudadana de la
            Municipalidad de Santa Fe. Nuestros bots toman tu archivo, lo
            comprimen y te lo dejan listo para que pese lo menos posible — por
            debajo de 1&nbsp;MB — y pueda ser procesado por los sistemas de
            Atención Ciudadana.
          </p>
          <p>
            Todo corre en la red interna: los archivos nunca abandonan los
            servidores de Atención Ciudadana. No se envían a internet ni a
            servicios externos, de modo que quedan seguros y protegidos.
          </p>
          <p>
            Subí un PDF, JPG, PNG u otro formato admitido. Cuando termine la
            compresión, descargá el resultado e incorporalo al trámite.
          </p>
        </div>
        <ol class="steps">
          <li><span>01</span> Subí el archivo</li>
          <li><span>02</span> Comprimí a menos de 1 MB</li>
          <li><span>03</span> Descargá e incorporá al trámite</li>
        </ol>
        """,
        unsafe_allow_html=True,
    )

with right:
    uploaded = st.file_uploader(
        "Subí un archivo",
        type=["pdf", "jpg", "jpeg", "png", "webp", "bmp", "tif", "tiff", "gif", "heic", "heif"],
        label_visibility="collapsed",
        help=f"PDF o imagen. Máximo {format_size(MAX_INPUT_BYTES)}.",
    )

    file_id = f"{uploaded.name}-{uploaded.size}" if uploaded is not None else None
    if st.session_state.get("file_id") != file_id:
        st.session_state.file_id = file_id
        st.session_state.compress_result = None
        st.session_state.compress_error = None

    if uploaded is None:
        st.markdown(
            '<p class="panel-label">Esperando un archivo</p>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class="file-ready">
              <div class="name">{html.escape(uploaded.name)}</div>
              <div class="meta">Listo para comprimir · {format_size(uploaded.size)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    go = st.button("Comprimir", type="primary", disabled=uploaded is None)

    if go and uploaded is not None:
        raw = uploaded.getvalue()
        name = uploaded.name or "archivo"
        if not supported_extension(name):
            st.session_state.compress_result = None
            st.session_state.compress_error = "Ese formato no se puede comprimir acá."
        else:
            try:
                with st.status("Comprimiendo el archivo…", expanded=True) as status:
                    st.write("Tomando el archivo")
                    st.write("Reduciendo el peso")
                    st.session_state.compress_result = compress_file(raw, name)
                    st.session_state.compress_error = None
                    status.update(label="Compresión terminada", state="complete")
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
            type="secondary",
        )
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="legal">
      Compresor de archivos de <strong>Atención Ciudadana</strong>.
      El uso de esta herramienta implica la aceptación de que los archivos se
      procesan de forma temporal, sin almacenamiento persistente, y que la
      calidad visual puede reducirse para respetar el límite de 1&nbsp;MB.
      Queda prohibida la reproducción o redistribución de esta aplicación
      sin autorización.
    </div>
    <p class="copy">© 2026 Atención Ciudadana de la Municipalidad de Santa Fe. Todos los derechos reservados.</p>
    <p class="renzo">Desarrollado y mantenido por Renzo.</p>
    """,
    unsafe_allow_html=True,
)
if LOGO.exists():
    st.image(str(LOGO), width=200)

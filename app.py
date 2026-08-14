from pathlib import Path

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
    page_title="Compresor de archivos — Municipalidad de Santa Fe",
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

[data-testid="stFileUploader"] {
  margin-top: 0;
}

[data-testid="stFileUploader"] > label {
  display: none;
}

[data-testid="stFileUploaderDropzone"] {
  min-height: 220px !important;
  background: #FFFFFF !important;
  border: 1px solid #D5DEE8 !important;
  border-radius: 8px !important;
  padding: 28px 20px !important;
}

[data-testid="stFileUploaderDropzone"]:hover {
  border-color: #1A4A6E !important;
  background: #F8FAFC !important;
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
}

[data-testid="stFileUploaderDropzone"] button:hover {
  background: #0C2644 !important;
  border-color: #0C2644 !important;
  color: #FFFFFF !important;
}

[data-testid="stFileUploaderDropzoneInstructions"] {
  color: #5A6B7A !important;
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
}

.stDownloadButton > button:hover {
  background: #F3F6FA;
  border-color: #1A4A6E;
  color: #0C2644;
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
</style>
""",
    unsafe_allow_html=True,
)

left, right = st.columns((1.15, 0.85), gap="large")

with left:
    st.title("Compresor de archivos")
    st.markdown(
        """
        <div class="welcome">
          <p>
            Bienvenido al Compresor de archivos de la Municipalidad de Santa Fe.
            Nuestros bots toman tu archivo, lo comprimen y te lo dejan listo para
            que pese lo menos posible — por debajo de 1&nbsp;MB — y pueda ser
            procesado por los sistemas municipales.
          </p>
          <p>
            Todo corre en la red interna: los archivos nunca abandonan los
            servidores municipales. No se envían a internet ni a servicios
            externos, de modo que quedan seguros y protegidos dentro de la
            infraestructura de la Municipalidad.
          </p>
          <p>
            Subí un PDF, JPG, PNG u otro formato admitido. Cuando termine la
            compresión, descargá el resultado e incorporalo al trámite o al
            sistema que corresponda.
          </p>
        </div>
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

    go = st.button("Comprimir", type="primary", disabled=uploaded is None)

    if go and uploaded is not None:
        raw = uploaded.getvalue()
        name = uploaded.name or "archivo"
        if not supported_extension(name):
            st.session_state.compress_result = None
            st.session_state.compress_error = "Ese formato no se puede comprimir acá."
        else:
            try:
                with st.spinner("Comprimiendo…"):
                    st.session_state.compress_result = compress_file(raw, name)
                    st.session_state.compress_error = None
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
            ui.alert("Listo", description=extra, key="ok_done")
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

st.markdown(
    """
    <div class="legal">
      Compresor de archivos de la <strong>Municipalidad de Santa Fe</strong>.
      El uso de esta herramienta implica la aceptación de que los archivos se
      procesan de forma temporal, sin almacenamiento persistente, y que la
      calidad visual puede reducirse para respetar el límite de 1&nbsp;MB.
      Queda prohibida la reproducción o redistribución de esta aplicación
      sin autorización.
    </div>
    <p class="copy">© 2026 Municipalidad de Santa Fe. Todos los derechos reservados.</p>
    <p class="renzo">Desarrollado y mantenido por Renzo.</p>
    """,
    unsafe_allow_html=True,
)
if LOGO.exists():
    st.image(str(LOGO), width=200)

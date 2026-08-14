<p align="center">
  <img src="assets/brand/msf-horizontal.png" alt="Municipalidad de Santa Fe" width="260">
</p>

<h1 align="center">Compresor de archivos</h1>

<p align="center">
  <strong>Atención Ciudadana · Municipalidad de Santa Fe</strong><br>
  Bajá PDF e imágenes a <strong>menos de 1&nbsp;MB</strong> para el trámite,<br>
  sin subir documentos a un compresor de internet.
</p>

<p align="center">
  <a href="https://compresorsac.streamlit.app"><strong>Abrir la app</strong></a>
  ·
  <a href="#cómo-se-usa">Cómo se usa</a>
  ·
  <a href="#privacidad">Privacidad</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/salida-%3C%201%20MB-2F6B5C?style=flat-square" alt="Salida menor a 1 MB">
  <img src="https://img.shields.io/badge/Python-3.12-0C2644?style=flat-square" alt="Python 3.12">
  <img src="https://img.shields.io/badge/Streamlit-1.61-1A4A6E?style=flat-square" alt="Streamlit 1.61">
</p>

---

## Para qué existe

El sistema de **Atención Ciudadana (SAC)** no admite archivos de más de **1 MB**. Quien va a iniciar un trámite —DNI, partidas, certificados, comprobantes, fotos de documentación— se encuentra con el archivo rechazado y, en la práctica, busca “compresor de PDF” o “bajar peso de imagen” en Google.

Eso es un problema. Los compresores públicos de la web suelen:

- pedir que **subas el documento a un servidor de terceros**, a menudo fuera del país
- no dejar claro **si lo guardan, por cuánto tiempo ni quién lo ve**
- mezclar trámites municipales con cuentas, publicidad y reuso de archivos

Un DNI, una partida de nacimiento o un certificado no deberían pasar por un sitio desconocido solo para “que pese menos”.

Esta app existe para ese hueco: **comprimir (y, si hace falta, unir) archivos con techo de 1 MB**, pensada para el trámite, con procesamiento temporal y **sin almacenamiento persistente**.

---

## Qué hace

| Situación | Resultado |
| --- | --- |
| **1 archivo** | Se comprime y se descarga. Una imagen sigue siendo imagen; un PDF sigue siendo PDF. |
| **2 a 5 archivos** | Se unen, en el orden de carga, en **un solo PDF** y ese PDF se comprime a menos de 1 MB. |

El nombre de salida queda así:

- un archivo: `{nombre}_comprimido.pdf` (o `.jpg` / `.webp`, según el caso)
- varios archivos: `{nombre}_combinado_comprimido.pdf`

Si el original ya está bajo 1 MB, no se vuelve a comprimir: se entrega igual, con el sufijo `_comprimido`, para que el trámite reciba un archivo con nombre claro.

La calidad puede bajarse (resolución, JPEG/WebP, recorte de páginas pesadas) **solo lo necesario** para respetar el techo. En documentos muy pesados o con muchas páginas, a veces no alcanza: se entrega la versión más liviana posible y se avisa.

---

## Cómo se usa

La interfaz tiene **tres pasos**.

1. **Subí los archivos**  
   Arrastrá o elegí hasta **5** archivos. PDF o imagen. Máximo **80 MB** cada uno.

2. **Comprimí** (un archivo) o **Uní y comprimí** (varios)  
   Podés sacar uno con la **×** o **Quitar todos** y volver a armar el lote.

3. **Descargá**  
   El archivo listo para adjuntar en el SAC. **Empezar de nuevo** limpia el lote.

No hace falta crear cuenta ni instalar nada en la PC de la persona que tramita: entra a la app, sube, descarga.

---

## Qué acepta

**PDF** e imágenes: JPG, JPEG, PNG, WEBP, BMP, TIF/TIFF, GIF. HEIC/HEIF si el entorno lo permite.

| Límite | Valor |
| --- | --- |
| Archivos por vez | 5 |
| Peso de cada archivo de entrada | 80 MB |
| Peso del archivo de salida | menos de 1 MB |
| Unión de varios archivos | un PDF (no es un ZIP) |

---

## Privacidad

- El archivo se procesa para comprimir o unir y **no se guarda** como expediente ni en una carpeta permanente de la app.
- No hay inicio de sesión ni base de usuarios.
- No se envía el documento a un compresor de terceros.

Sigue siendo un documento sensible: usá la app **oficial del área**, no clones ni “el mismo truco” en cualquier web.

---

## App en línea

**https://compresorsac.streamlit.app**

Repositorio: [github.com/CynarJulep/compresor](https://github.com/CynarJulep/compresor)

---

## Insertar en Google Sites

No uses “Insertar por URL” ni una dirección `http://` de una PC de escritorio: Google Sites es HTTPS y la bloquea.

En el sitio: **Insertar → Insertar código** (no por URL) y pegá:

```html
<iframe
  src="https://compresorsac.streamlit.app/?embed=true&embed_options=light_theme&embed_options=hide_loading_screen"
  title="Compresor de archivos"
  width="100%"
  height="100%"
  style="border:0;width:100%;height:100vh;min-height:100vh;display:block;"
  frameborder="0"
  scrolling="auto"
  allow="fullscreen; clipboard-read; clipboard-write"
  allowfullscreen
  loading="eager">
</iframe>
```

La app tiene que seguir publicada en modo público para que el iframe cargue.

---

## Correr en local (desarrollo)

Hace falta **Python 3.12**.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Queda en [http://127.0.0.1:8501](http://127.0.0.1:8501).

Para instalar dependencias y comprobar el motor:

```bash
pip install -r requirements.txt pytest
python -m pytest tests/ -q
```

En Windows, `INSTALAR_SERVIDOR.bat` deja la app como tarea al arranque (uso interno del área). No hace falta para desarrollar ni para usar la nube.

---

## Cómo está armado

| Archivo | Rol |
| --- | --- |
| `app.py` | Interfaz (wizard de 3 pasos) |
| `compressor.py` | Motor: techo de 1 MB, unión a PDF, nombres de salida |
| `tests/test_compressor.py` | Pruebas del motor |
| `assets/brand/` | Identidad visual de la Municipalidad |
| `requirements.txt` | Streamlit, Pillow, PyMuPDF |

El techo de salida es 1 MB (`TARGET_BYTES`); internamente se apunta un poco más abajo para no pasarse al guardar.

---

## Créditos

Compresor de **Atención Ciudadana**, Municipalidad de Santa Fe.

Desarrollado y mantenido por **Renzo**.

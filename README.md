# Compresor

App en Python para bajar PDF, JPG, PNG y formatos similares a **menos de 1 MB**.

Municipalidad de Santa Fe. Los archivos se procesan en el servidor de la app; no se almacenan.

## En esta PC

- Local: http://127.0.0.1:8501
- Red: http://10.3.2.117:8501

Doble clic en `INSTALAR_SERVIDOR.bat` para dejarla al arranque.

## Streamlit Community Cloud

App pública: [compresorsac.streamlit.app](https://compresorsac.streamlit.app)

Repositorio: [github.com/CynarJulep/compresor](https://github.com/CynarJulep/compresor)

### Insertar en Google Sites

No uses “Insertar por URL” ni la dirección de esta PC (`http://10.3.2.117:8501`): Google Sites es HTTPS y bloquea HTTP.

En el sitio: **Insertar → Insertar código** (no por URL) y pegá:

```html
<iframe
  src="https://compresorsac.streamlit.app/?embed=true"
  width="100%"
  height="780"
  style="border:none;"
  loading="lazy"
></iframe>
```

La app tiene que seguir en modo público.

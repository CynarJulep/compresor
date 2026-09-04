# Compresor — Docker (reemplazo de la tarea Windows)

```powershell
cd C:\Renzo\compresor\compresor
.\scripts\stop-windows-server.ps1   # libera :8501
docker compose up -d --build
.\scripts\install-docker-autostart.ps1
```

App: **http://127.0.0.1:8501**

```powershell
docker compose ps
docker compose logs -f
docker compose down
```

Persistencia: `./data`, `./logs`. `restart: unless-stopped`.

La app pública Streamlit Cloud (`compresorsac.streamlit.app`) no se modifica con este Compose.

# Google Fit Auto Steps

Este proyecto contiene un script en Python 3 para automatizar diariamente el registro de **20 000 pasos** en Google Fit, usando tu hora local, y notificando si algo falla.

---

## Contenido

- `script.py`: código principal del script.
- `credentials.json`: credenciales OAuth 2.0 de Google Cloud.
- `token.json`: token de usuario (generado en la primera ejecución).
- `venv/`: entorno virtual (no subirlo al repositorio).

---

## Requisitos

- **Python 3.7** o superior.

- Paquetes de Python (instalados en entorno virtual):

  ```bash
  pip install --upgrade \
    google-auth-oauthlib \
    google-auth-httplib2 \
    google-api-python-client \
    pytz
  ```

- **Opcional**: para crear un virtualenv en Debian/Ubuntu:

  ```bash
  sudo apt update
  sudo apt install python3-venv python3-pip
  ```

---

## Configuración inicial

1. Clona este repositorio:

   ```bash
   git clone https://github.com/cmos486/google_fit_auto_steps.git
   cd google_fit_auto_steps
   ```

2. Crea y activa un entorno virtual:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instala dependencias dentro del venv:

   ```bash
   pip install --upgrade \
     google-auth-oauthlib \
     google-auth-httplib2 \
     google-api-python-client \
     pytz
   ```

4. Copia tu `credentials.json` (OAuth 2.0 Client ID) a la raíz del proyecto.

5. Borra `token.json` si existe:

   ```bash
   rm -f token.json
   ```

6. Abre `script.py` y ajusta la zona horaria local si es necesario:

   ```python
   # Ejemplo para Europa/Madrid:
   LOCAL_TZ = pytz.timezone('Europe/Madrid')
   ```

---

## Primer ejecución

Con el entorno virtual activo, lanza:

```bash
python3 script.py
```

- Se abrirá tu navegador para autorizar lectura/escritura en Google Fit.
- Generará `token.json` con tus tokens.
- Verás en consola el total de pasos de hoy y la inserción (si faltan pasos).

---

## Uso diario / cron

Con el venv activado, puedes ejecutar manualmente:

```bash
source venv/bin/activate
python3 script.py
```

Para automatizar cada 30 min, añade al crontab (`crontab -e`):

```cron
*/30 * * * * cd /ruta/a/google_fit_auto_steps && \
  source venv/bin/activate && \
  python3 script.py >> /ruta/a/fit.log 2>&1
```

---

## Personalización

- Cambia la meta de pasos modificando `TARGET_STEPS` al inicio de `script.py`.
- Ajusta la zona (`LOCAL_TZ`) a tu ubicación.
- Para más notificaciones (Slack, Telegram…), edita el bloque `except` en `main()`.

---

## Licencia

MIT © Kilian Ubeda Cano


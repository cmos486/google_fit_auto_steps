# Google Fit Auto Steps

Este proyecto contiene un script en Python 3 para automatizar diariamente el registro de **20 000 pasos** en Google Fit, usando tu hora local y refrescando el token automáticamente.

---

## Crear proyecto en Google Cloud y configurar la API

Antes de configurar y ejecutar el script, crea un proyecto en Google Cloud y habilita la Fitness API:

1. Ve a [https://console.developers.google.com/](https://console.developers.google.com/) y crea un **nuevo proyecto** o selecciona uno existente.
2. En **API y servicios > Biblioteca**, busca **Fitness API** y haz clic en **Habilitar**.
3. Dirígete a **API y servicios > Credenciales** y selecciona **+ Crear credenciales > ID de cliente OAuth**:
   - Tipo de aplicación: **Escritorio**.
   - Nombre: p.ej. `GoogleFit Auto Steps`.
4. Descarga el JSON generado y renómbralo `credentials.json`.
5. En **Pantalla de consentimiento OAuth** configura:
   - Nombre de la aplicación y contacto.
   - Scopes autorizados:
     ```text
     https://www.googleapis.com/auth/fitness.activity.read
     https://www.googleapis.com/auth/fitness.activity.write
     ```
   Estos scopes permiten al script **leer** y **escribir** datos de actividad en tu cuenta de Google Fit.

---

## Contenido

- `script.py`: código principal del script.
- `credentials.json`: credenciales OAuth 2.0 (descargado desde Google Cloud).
- `token.json`: token de usuario (generado en la primera ejecución).
- `venv/`: entorno virtual (no subirlo al repositorio).

---

## Requisitos

- **Python 3.7** o superior.
- Virtualenv (recomendado):
  ```bash
  sudo apt update && sudo apt install python3-venv python3-pip
  ```
- Paquetes de Python (instalar dentro del venv):
  ```bash
  pip install --upgrade \
    google-auth-oauthlib \
    google-auth-httplib2 \
    google-api-python-client \
    google-auth \
    pytz
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
3. Copia tu archivo `credentials.json` (paso previo) a la raíz del proyecto.
4. Borra cualquier token previo:
   ```bash
   rm -f token.json
   ```
5. Instala dependencias en el venv:
   ```bash
   pip install --upgrade \
     google-auth-oauthlib \
     google-auth-httplib2 \
     google-api-python-client \
     google-auth \
     pytz
   ```
6. Ajusta la zona local en `script.py` si no es `Europe/Madrid`:
   ```python
   LOCAL_TZ = pytz.timezone('Tu/Región')
   ```

---

## Primer ejecución

Con el entorno virtual activo, ejecuta:

```bash
python3 script.py
```

- Se abrirá el navegador para autorizar lectura/escritura en Google Fit.
- Se generará `token.json` con tu token de acceso y refresh.
- Verás en consola el total de pasos de hoy y la inserción (si faltan pasos).

---

## Uso diario / Cron

### Ejecución manual

```bash
source venv/bin/activate
python3 script.py
```

### Automatización cada 6 horas

Edita el crontab (`crontab -e`) e inserta:

```cron
0 */6 * * * cd /root/google_fit_auto_steps && \
  /root/google_fit_auto_steps/venv/bin/python3 script.py \
  >> /root/google_fit_auto_steps/fit.log 2>&1
```

- Se ejecuta a las 00:00, 06:00, 12:00, 18:00 UTC.
- Ajusta rutas y usuarios según tu entorno.

---

## Personalización

- Cambia la meta modificando `TARGET_STEPS` en `script.py`.
- Para notificaciones avanzadas (Slack, Telegram…), edita el bloque `except` en `main()`.

---

## Licencia

MIT © Kilian Ubeda Cano

```
```

Google Fit Auto Steps

Este proyecto contiene un script en Python 3 para automatizar diariamente el registro de 20 000 pasos en Google Fit, así como su verificación y notificación en caso de fallo.

⸻

Contenido
	•	script.py: código principal del script.
	•	credentials.json: credenciales OAuth 2.0 de Google Cloud.
	•	token.json: token de usuario (generado tras el primer flujo de autorización).

⸻

Requisitos
	•	Python 3.7 o superior.
	•	Paquetes de Python:

pip install --upgrade \
  google-auth-oauthlib \
  google-auth-httplib2 \
  google-api-python-client


	•	Tener una cuenta de Google Cloud con:
	•	Proyecto habilitado para Fitness API.
	•	OAuth 2.0 Client ID (aplicación de escritorio) y su archivo credentials.json.

⸻

Configuración inicial
	1.	Clona este repositorio:

git clone https://github.com/tu-usuario/google-fit-auto-steps.git
cd google-fit-auto-steps


	2.	Copia tu archivo de credenciales en la raíz del proyecto como credentials.json.
	3.	Borra cualquier token previo (si existe):

rm -f token.json


	4.	Abre script.py y verifica:

SCOPES = [
    'https://www.googleapis.com/auth/fitness.activity.read',
    'https://www.googleapis.com/auth/fitness.activity.write'
]
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.json'
TARGET_STEPS = 20000



⸻

Primer ejecución

Al ejecutar por primera vez, el script abrirá el navegador para que autorices los permisos de lectura y escritura en Google Fit.

python3 script.py

	•	Tras conceder permisos, se generará token.json con el token de acceso.
	•	Verás en consola el número de pasos actuales del día y la inserción (si corresponde).

⸻

Uso regular

Ejecuta manualmente:

python3 script.py

La lógica es:
	1.	Agrega permisos de lectura y escritura.
	2.	Obtiene pasos registrados hoy.
	3.	Si ya hay ≥ 20 000 pasos, informa y no hace nada.
	4.	Si hay menos, registra la diferencia.
	5.	En caso de error, imprime en stderr y sale con código 1.

⸻

Automatización con cron

Para ejecutar cada 30 minutos, añade al crontab (crontab -e):

*/30 * * * * /usr/bin/python3 /ruta/al/proyecto/script.py >> /ruta/al/proyecto/fit.log 2>&1

	•	>> fit.log: guarda salida estándar.
	•	2>&1: guarda errores en el mismo log.

⸻

Depuración y logs
	•	Para activar traza HTTP, ajusta en script.py:

httplib2.debuglevel = 4
logging.basicConfig(level=logging.DEBUG)


	•	Los mensajes de estado y errores se imprimen en consola.

⸻

FAQs
	•	¿Dónde se guarda token.json?
	•	En el mismo directorio del script.
	•	¿Cómo cambio la meta de pasos?
	•	Modifica TARGET_STEPS en el inicio de script.py.
	•	¿Puedo notificar por otro canal?
	•	Sí: en el bloque except, sustituye la función de notificación.

⸻


import os
import sys
import datetime
import httplib2
import logging

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# ---------------- CONFIGURACIÓN ----------------
SCOPES = [
    'https://www.googleapis.com/auth/fitness.activity.read',
    'https://www.googleapis.com/auth/fitness.activity.write'
]
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.json'
TARGET_STEPS = 20000
# ------------------------------------------------

# Configuración de logging
logging.basicConfig(level=logging.INFO)
httplib2.debuglevel = 0


def get_credentials():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            CREDENTIALS_FILE,
            SCOPES,
            include_granted_scopes=True
        )
        creds = flow.run_local_server(port=0, prompt='consent')
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    return creds


def millis(dt: datetime.datetime) -> int:
    return int(dt.timestamp() * 1e3)


def get_today_steps(service) -> int:
    """Lee el total de pasos de hoy usando la API de agregación."""
    now = datetime.datetime.utcnow()
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    body = {
        "aggregateBy": [{"dataTypeName": "com.google.step_count.delta"}],
        "bucketByTime": {"durationMillis": millis(now) - millis(start)},
        "startTimeMillis": millis(start),
        "endTimeMillis": millis(now)
    }
    resp = service.users().dataset().aggregate(userId='me', body=body).execute()
    total = sum(
        val.get('intVal', 0)
        for bucket in resp.get('bucket', [])
        for ds in bucket.get('dataset', [])
        for point in ds.get('point', [])
        for val in point.get('value', [])
    )
    return total


def insert_steps(service, steps_to_add: int):
    now = datetime.datetime.utcnow()
    start_ns = int(now.replace(hour=0, minute=0, second=0, microsecond=0).timestamp() * 1e9)
    end_ns = int(now.timestamp() * 1e9)
    ds_name = "python_auto_steps"

    # Buscar o crear dataSource
    ds_list = service.users().dataSources().list(userId='me').execute()
    ds_id = next(
        (d['dataStreamId'] for d in ds_list.get('dataSource', [])
         if d.get('dataStreamName') == ds_name),
        None
    )
    if not ds_id:
        data_source = {
            "dataStreamName": ds_name,
            "type": "raw",
            "application": {"name": "auto-step-script"},
            "dataType": {
                "name": "com.google.step_count.delta",
                "field": [{"name": "steps", "format": "integer"}]
            },
        }
        ds_id = service.users().dataSources().create(
            userId='me', body=data_source
        ).execute()['dataStreamId']

    dataset_id = f"{start_ns}-{end_ns}"
    point = {
        "dataTypeName": "com.google.step_count.delta",
        "startTimeNanos": str(start_ns),
        "endTimeNanos": str(end_ns),
        "value": [{"intVal": steps_to_add}]
    }
    body = {
        "dataSourceId": ds_id,
        "minStartTimeNs": str(start_ns),
        "maxEndTimeNs": str(end_ns),
        "point": [point]
    }
    service.users().dataSources().datasets().patch(
        userId='me',
        dataSourceId=ds_id,
        datasetId=dataset_id,
        body=body
    ).execute()


def main():
    try:
        creds = get_credentials()
        service = build('fitness', 'v1', credentials=creds, cache_discovery=False)

        current = get_today_steps(service)
        logging.info(f"Pasos hoy hasta ahora: {current}")

        if current >= TARGET_STEPS:
            print(f"✅ Ya tienes {current} pasos (≥ {TARGET_STEPS}), no hago nada.")
        else:
            faltan = TARGET_STEPS - current
            print(f"🔄 Faltan {faltan} pasos para llegar a {TARGET_STEPS}, los inserto ahora.")
            insert_steps(service, faltan)
            print("✅ Inserción completada.")

    except Exception as e:
        err_msg = f"Error al actualizar Google Fit: {type(e).__name__}: {e}"
        logging.error(err_msg)
        # Impresión de error en consola y salida con código 1
        print(f"🚨 {err_msg}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

import requests
import boto3
from datetime import datetime

# Cliente de S3
s3 = boto3.client('s3')

# Nombre del bucket S3
BUCKET_NAME = 'ultimateultimate'

# Fuentes a descargar
SOURCES = {
    "eltiempo": "https://www.eltiempo.com/",
    "publimetro": "https://www.publimetro.co/"  # alternativa más simple que El Espectador
}

# Encabezados para evitar bloqueo por bots
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}

def upload(event=None, context=None):
    today = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d")  # Formato YYYY-MM-DD

    for name, url in SOURCES.items():
        try:
            print(f"Descargando {name} desde {url}")
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()

            html_content = response.text  # HTML como string

            filename = f"headlines/raw/{name}-{today}.html"

            s3.put_object(
                Bucket=BUCKET_NAME,
                Key=filename,
                Body=html_content.encode('utf-8'),
                ContentType='text/html; charset=utf-8'
            )

            print(f"{name} guardado correctamente como {filename}")
        except Exception as e:
            print(f"Error descargando {name}: {e}")

    return {
        "status": "ok",
        "date": today
    }

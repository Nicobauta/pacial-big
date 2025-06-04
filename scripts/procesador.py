import boto3
import csv
import io
from bs4 import BeautifulSoup
from datetime import datetime
import os

s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    raw_key = event['Records'][0]['s3']['object']['key']

    response = s3.get_object(Bucket=bucket, Key=raw_key)
    html = response['Body'].read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    nombre_archivo = os.path.basename(raw_key)
    partes = nombre_archivo.replace('.html', '').split('-')
    periodico = partes[0]
    fecha = '-'.join(partes[1:])
    fecha_dt = datetime.strptime(fecha, "%Y-%m-%d")
    year, month, day = fecha_dt.strftime("%Y"), fecha_dt.strftime("%m"), fecha_dt.strftime("%d")

    noticias = []

    if periodico == "eltiempo":
        for art in soup.find_all('article'):
            try:
                categoria = art.find('span', class_='category')
                categoria = categoria.get_text(strip=True) if categoria else 'Sin categoría'
                a = art.find('a')
                titular = a.get_text(strip=True)
                enlace = a['href']
                if not enlace.startswith("http"):
                    enlace = "https://www.eltiempo.com" + enlace
                noticias.append([categoria, titular, enlace])
            except Exception:
                pass
    elif periodico == "publimetro":
        for art in soup.find_all('article'):
            try:
                categoria = art.get('data-taxonomy', 'Sin categoría')
                a = art.find('a')
                titular = a.get_text(strip=True)
                enlace = a['href']
                if not enlace.startswith("http"):
                    enlace = "https://www.publimetro.co" + enlace
                noticias.append([categoria, titular, enlace])
            except Exception:
                pass

    #Crear contenido CSV
    csv_buffer = io.StringIO()
    writer = csv.writer(csv_buffer)
    writer.writerow(["categoria", "titular", "enlace"])  

    for cat, tit, url in noticias:
         writer.writerow([cat, tit, url])

    output_key = f"headlines/final/periodico={periodico}/year={year}/month={month}/day={day}/noticias.csv"
    s3.put_object(
        Bucket=bucket,
        Key=output_key,
        Body=csv_buffer.getvalue().encode('utf-8'),
        ContentType='text/csv'
    )

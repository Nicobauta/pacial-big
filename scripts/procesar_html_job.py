import boto3
from bs4 import BeautifulSoup
from datetime import datetime
import os

s3 = boto3.client('s3')
BUCKET = 'ultimateultimate' 

#Obtener la lista de archivos en la carpeta raw
response = s3.list_objects_v2(Bucket=BUCKET, Prefix="headlines/raw/")

#Verificar si hay archivos
for obj in response.get('Contents', []):
    raw_key = obj['Key']

    #Solo procesar archivos .html
    if not raw_key.endswith(".html"):
        continue

    print(f"📥 Procesando archivo: {raw_key}")
    try:
        #Descargar HTML
        response = s3.get_object(Bucket=BUCKET, Key=raw_key)
        html = response['Body'].read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')

        #Obtener nombre, periódico y fecha
        nombre_archivo = os.path.basename(raw_key).replace('.html', '')
        partes = nombre_archivo.split('-')
        periodico = partes[0]
        fecha = '-'.join(partes[1:])
        fecha_dt = datetime.strptime(fecha, "%Y-%m-%d")
        year, month, day = fecha_dt.strftime("%Y"), fecha_dt.strftime("%m"), fecha_dt.strftime("%d")

        noticias = []

        #Parsing para El Tiempo
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
                    continue

        #Parsing para Publimetro
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
                    continue

        #Crear contenido CSV
        csv_content = "categoria,titular,enlace\n"
        for cat, tit, url in noticias:
            csv_content += f"\"{cat}\",\"{tit}\",\"{url}\"\n"

        #Guardar CSV en particiones Glue
        output_key = f"headlines/final/periodico={periodico}/year={year}/month={month}/day={day}/noticias.csv"
        s3.put_object(
            Bucket=BUCKET,
            Key=output_key,
            Body=csv_content.encode('utf-8'),
            ContentType='text/csv'
        )
        print(f"✅ CSV guardado en: {output_key}")

    except Exception as e:
        print(f"❌ Error al procesar {raw_key}: {e}")

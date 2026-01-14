
# Proyecto Big Data – Pipeline de Procesamiento con Python y AWS

Este proyecto implementa un **pipeline de procesamiento de datos orientado a Big Data**, utilizando **Python** y servicios de **AWS**, enfocado en la **descarga, procesamiento y transformación de contenido HTML**, así como la **orquestación de jobs y crawlers de AWS Glue**.

El proyecto incluye **pruebas automatizadas** y **integración continua con GitHub Actions**, garantizando la correcta ejecución del flujo de datos.

---

## Objetivo del proyecto

- Descargar contenido HTML
- Procesar y transformar la información
- Ejecutar jobs de AWS Glue
- Activar crawlers para catalogación de datos
- Validar el pipeline mediante pruebas automáticas

---

## Tecnologías utilizadas

- **Python 3**
- **AWS Glue**
- **AWS Crawlers**
- **GitHub Actions**
- **Pytest / pruebas automatizadas**

---

## Estructura del proyecto

```
.
├── .github/
│ └── workflows/
│ └── python-tests.yml
│
├── scripts/
│ ├── app.py
│ ├── descargar_html_job.py
│ ├── procesar_html_job.py
│ ├── procesador.py
│ ├── procesamiento.py
│ ├── glue_trigger.py
│ └── trigger_crawler_job.py
│
├── test_all.py
├── requirements.txt
└── README.md

```


---

## Flujo del sistema

1. Descarga de archivos HTML
2. Procesamiento y transformación de datos
3. Ejecución de jobs de AWS Glue
4. Activación de crawlers para catalogación
5. Validación del pipeline mediante pruebas

---

## Pruebas automatizadas

El archivo `test_all.py` contiene pruebas que validan:

- Importación correcta de los módulos
- Existencia y funcionamiento de funciones clave

Las pruebas se ejecutan automáticamente mediante **GitHub Actions** en cada push al repositorio.

---

## Ejecución del proyecto

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar pruebas
pytest test_all.py

# Ejecutar el script principal
python scripts/app.py

import boto3

glue = boto3.client('glue', region_name='us-east-1')
crawler_name = 'crawler-headlines-final'

try:
    glue.start_crawler(Name=crawler_name)
    print(f" Crawler '{crawler_name}' iniciado con éxito.")
except glue.exceptions.CrawlerRunningException:
    print(" Crawler ya se está ejecutando.")
except Exception as e:
    print(f" Error al iniciar el crawler: {str(e)}")

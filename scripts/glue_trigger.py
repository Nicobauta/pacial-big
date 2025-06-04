import boto3

def lambda_handler(event, context):
    glue = boto3.client('glue', region_name='us-east-1')
    crawler_name = 'crawler-headlines-final'  # mismo nombre que creaste en Glue

    try:
        glue.start_crawler(Name=crawler_name)
        print(f" Crawler '{crawler_name}' iniciado con éxito.")
        return {
            'statusCode': 200,
            'body': f"Crawler '{crawler_name}' iniciado correctamente"
        }
    except glue.exceptions.CrawlerRunningException:
        print(f" Crawler '{crawler_name}' ya se está ejecutando.")
        return {
            'statusCode': 200,
            'body': f"Crawler '{crawler_name}' ya está corriendo"
        }
    except Exception as e:
        print(f" Error al iniciar el crawler: {str(e)}")
        return {
            'statusCode': 500,
            'body': f"Error: {str(e)}"
        }

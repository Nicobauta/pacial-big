import pytest
import pandas as pd
from pathlib import Path

# === Tests para app.py ===
from app import lambda_handler

def test_lambda_handler_evento_vacio():
    event = {}
    context = {}
    result = lambda_handler(event, context)
    assert isinstance(result, dict)

# === Tests para glue_trigger.py ===
from glue_trigger import iniciar_trabajo_glue

def test_iniciar_trabajo_glue_mock(mocker):
    mock_client = mocker.Mock()
    mock_client.start_job_run.return_value = {"JobRunId": "1234"}

    resultado = iniciar_trabajo_glue(mock_client, "mi_trabajo")
    assert resultado == {"JobRunId": "1234"}

# === Tests para procesador.py ===
from procesador import Procesador

def test_procesar_archivo_csv(tmp_path):
    archivo = tmp_path / "datos.csv"
    archivo.write_text("col1,col2\n1,2\n3,4")

    p = Procesador()
    df = p.procesar_csv(str(archivo))

    assert not df.empty
    assert df.shape == (2, 2)

# === Tests para procesamiento.py ===
from procesamiento import limpiar_datos

def test_limpiar_datos():
    datos = pd.DataFrame({
        "col1": [1, 2, None],
        "col2": ["a", None, "c"]
    })

    resultado = limpiar_datos(datos)
    assert not resultado.isnull().values.any()
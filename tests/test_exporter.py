
import json
import csv
from pathlib import Path

from src.devices_in_wifi.exporter import guardar_csv, guardar_json



def test_guardar_csv_archivo(tmp_path: Path) -> None:
    dispositivos = [
        {
            "ip": "192.168.1.1",
            "mac": "aa:bb:cc:dd:ee:ff",
            "tipo": "Router",
            "fabricante": "TP-Link",
            "nombre": "TP-Link Router"
        }
    ]

    salida = tmp_path / "dispositivos.csv"

    guardar_csv(dispositivos, str(salida))

    assert salida.exists()



def test_guardar_csv_contenido(tmp_path: Path) -> None:
    dispositivos = [
        {
            "ip": "192.168.1.1",
            "mac": "aa:bb:cc:dd:ee:ff",
            "tipo": "Router",
            "fabricante": "TP-Link",
            "nombre": "TP-Link Router"
        }
    ]

    salida = tmp_path / "dispositivos.csv"

    guardar_csv(dispositivos, str(salida))

    with salida.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        filas = list(reader)

    assert len(filas) == 1
    assert filas[0]["ip"] == "192.168.1.1"
    assert filas[0]["fabricante"] == "TP-Link"



def test_guardar_json_archivo(tmp_path: Path) -> None:
    dispositivos = [
        {
            "ip": "192.168.1.1",
            "mac": "aa:bb:cc:dd:ee:ff",
            "tipo": "Router",
            "fabricante": "TP-Link",
            "nombre": "TP-Link Router"
        }
    ]

    salida = tmp_path / "dispositivos.json"

    guardar_json(dispositivos, str(salida))

    assert salida.exists()



def test_guardar_json_contenido(tmp_path: Path) -> None:
    dispositivos = [
        {
            "ip": "192.168.1.1",
            "mac": "aa:bb:cc:dd:ee:ff",
            "tipo": "Router",
            "fabricante": "TP-Link",
            "nombre": "TP-Link Router"
        }
    ]

    salida = tmp_path / "dispositivos.json"

    guardar_json(dispositivos, str(salida))

    with salida.open("r", encoding="utf-8") as f:
        datos = json.load(f)

    assert len(datos) == 1
    assert datos[0]["nombre"] == "TP-Link Router"

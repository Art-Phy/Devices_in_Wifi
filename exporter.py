
import csv
import json
from pathlib import Path
from typing import List, Dict


def guardar_csv(dispositivos: List[Dict[str, str]], ruta_salida: str) -> None:
    """
    Guarda la lista de dispositivos en un archivo CSV.
    """
    salida = Path(ruta_salida)
    salida.parent.mkdir(parents=True, exist_ok=True)

    with salida.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["ip", "mac", "tipo", "fabricante", "nombre"]
        )
        writer.writeheader()
        for d in dispositivos:
            writer.writerow(d)

    print(f"Resultados guardados en: {salida}")



def guardar_json(dispositivos: List[Dict[str, str]], ruta_salida: str) -> None:
    """
    Guarda la lista de dispositivos en un archivo JSON.
    """
    salida = Path(ruta_salida)
    salida.parent.mkdir(parents=True, exist_ok=True)

    with salida.open("w", encoding="utf-8") as f:
        json.dump(dispositivos, f, indent=2, ensure_ascii=False)

    print(f"Resultados guardados en JSON: {salida}")

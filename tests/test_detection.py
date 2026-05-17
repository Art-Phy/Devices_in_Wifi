
from devices_in_wifi.detection import (
    construir_nombre,
    detectar_fabricante,
    detectar_tipo_dispositivo,
)


def test_detectar_tipo_router() -> None:
    assert detectar_tipo_dispositivo("router-home") == "Router"



def test_detectar_tipo_smarthome() -> None:
    assert detectar_tipo_dispositivo("iphone-art") == "Smartphone"



def test_detectar_tipo_unknown() -> None:
    assert detectar_tipo_dispositivo("Nombre desconocido") == "Unknown"



def test_detectar_fabricante_known() -> None:
    assert detectar_fabricante("c8:b4:22:c6:bd:40") == "Askey"



def test_detectar_fabricante_unknown() -> None:
    assert detectar_fabricante("aa:bb:cc:dd:ee:ff") == "Desconocido"



def test_nombre_mostrable_real_hostname() -> None:
    assert (
        construir_nombre(
            "iphone-art",
            "Smartphone",
            "Apple"
        )
        == "iphone-art"
    )



def test_nombre_mostrable_vendor_and_type() -> None:
    assert (
        construir_nombre(
            "Nombre desconocido",
            "Router",
            "TP-Link"
        )
        == "TP-Link Router"
    )



def test_nombre_mostrable_total_fallback() -> None:
    assert (
        construir_nombre(
            "Nombre desconocido",
            "Unknown",
            "Desconocido"
        )
        == "Nombre desconocido"
    )

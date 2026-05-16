
from src.devices_in_wifi.scanner import detectar_red_local, imprimir_dispositivos



def test_imprimir_dispositivos_sin_resultados(capsys) -> None:
    imprimir_dispositivos([])

    salida = capsys.readouterr()

    assert "No se encontraron dispositivos." in salida.out



def test_imprimir_dispositivos_con_resultado(capsys) -> None:
    dispositivos = [
        {
            "ip": "192.168.1.1",
            "mac": "aa:bb:cc:dd:ee:ff",
            "tipo": "Router",
            "fabricante": "TP-Link",
            "nombre": "TP-Link Router"
        }
    ]

    imprimir_dispositivos(dispositivos)

    salida = capsys.readouterr()

    assert "Dispositivos encontrados" in salida.out
    assert "192.168.1.1" in salida.out
    assert "TP-Link Router" in salida.out



def test_detectar_red_local_fallback(monkeypatch) -> None:
    class FakeSocket:
        def __enter__(self):
            raise OSError
        
        def __exit__(self, exc_type, exc_value, traceback):
            return False
        
    monkeypatch.setattr(
        "src.devices_in_wifi.scanner.socket.socket",
        lambda *args, **kwargs: FakeSocket(),
    )

    assert detectar_red_local() == "192.168.1.0/24"

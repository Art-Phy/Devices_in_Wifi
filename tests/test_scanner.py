
from src.devices_in_wifi.scanner import detectar_red_local, imprimir_dispositivos, escanear_red



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



def test_escanear_red_sin_dns(monkeypatch) -> None:
    class FakeResponse:
        def __init__(self, ip: str, mac: str):
            self.psrc = ip
            self.hwsrc = mac

    fake_answered = [
        (None, FakeResponse("192.168.1.1", "30:68:93:aa:bb:cc")),
        (None, FakeResponse("192.168.1.10", "c8:b4:22:11:22:33")),
    ]

    monkeypatch.setattr(
        "src.devices_in_wifi.scanner.srp",
        lambda *args, **kwargs: (fake_answered, None),
    )

    dispositivos = escanear_red(
        "192.168.1.0/24",
        resolve_names=False
    )

    assert len(dispositivos) == 2
    assert dispositivos[0]["fabricante"] == "TP-Link"
    assert dispositivos[0]["tipo"] == "Router"
    assert dispositivos[1]["fabricante"] == "Askey"

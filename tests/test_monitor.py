
from devices_in_wifi.monitor import monitorizar_red



def test_monitorizar_red_ejecuta_escaneo_y_muestra_resultado(monkeypatch, capsys) -> None:
    dispositivos = [
        {
            "ip": "192.168.1.1",
            "mac": "aa:bb:cc:dd:ee:ff",
            "tipo": "Router",
            "fabricante": "TP-Link",
            "nombre": "TP-Link Router",
        }
    ]

    llamadas = {
        "scan": 0,
        "display": 0,
    }


    def fake_scan():
        llamadas["scan"] += 1
        return dispositivos


    def fake_display(resultados):
        llamadas["display"] += 1
        assert resultados == dispositivos


    def fake_sleep(interval):
        assert interval == 10
        raise KeyboardInterrupt


    monkeypatch.setattr(
        "devices_in_wifi.monitor.time.sleep",
        fake_sleep,
    )

    monitorizar_red(
        scan_function=fake_scan,
        display_function=fake_display,
        interval=10,
    )

    salida = capsys.readouterr()

    assert llamadas["scan"] == 1
    assert llamadas["display"] == 1
    assert "Monitorizando la red cada 10 segundos" in salida.out
    assert "Monitorización detenida por el usuario" in salida.out



def test_monitorizar_red_muestra_proximo_escaneo(monkeypatch, capsys) -> None:

    def fake_scan():
        return []


    def fake_display(_dispositivos):
        return None


    def fake_sleep(_interval):
        raise KeyboardInterrupt


    monkeypatch.setattr(
        "devices_in_wifi.monitor.time.sleep",
        fake_sleep,
    )

    monitorizar_red(
        scan_function=fake_scan,
        display_function=fake_display,
        interval=30,
    )

    salida = capsys.readouterr()

    assert "Próximo escaneo en 30 segundos" in salida.out

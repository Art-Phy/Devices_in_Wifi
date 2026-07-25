
from __future__ import annotations

import time
from typing import Callable, Dict, List

Device = Dict[str, str]
ScanFunction = Callable[[], List[Device]]
DisplayFunction = Callable[[List[Device]], None]



def monitorizar_red(scan_function: ScanFunction, display_function: DisplayFunction, interval: int) -> None:
    """Ejecuta escaneos de red continuamente hasta que el usuario pulse Ctrl+C
    
    Args:
        scan_function: función sin argumentos que devuelve los dispositivos.
        display_function: función encargada de mostrar los resultados.
        interval: segundos de espera entre escaneos.
    """
    print(
        f"Monitorizando la red cada {interval} sengundos. "
        "Pulsa Ctrl+C para detener."
    )

    try:
        while True:
            dispositivos = scan_function()
            display_function(dispositivos)

            print(f"\nPróximo escaneo en {interval} segundos...")
            time.sleep(interval)

    except KeyboardInterrupt:
        print("\nMonitorización detenida por el usuario")

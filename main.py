
# -*- coding: utf-8 -*-

"""
=============================
     DEVICES IN WIFI
=============================

Escaneador de dispositivos en una red Wi-Fi basado en ARP.
"""

from __future__ import annotations

import argparse
import ipaddress
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent / "src"))

from devices_in_wifi.exporter import guardar_csv, guardar_json
from devices_in_wifi.scanner import detectar_red_local, escanear_red, imprimir_dispositivos
from devices_in_wifi.monitor import monitorizar_red



def parse_args() -> argparse.Namespace:
    """
    Analiza los argumentos de la línea de comandos.
    """
    
    parser = argparse.ArgumentParser(
        description="Escaneador de dispositivos en red Wi-Fi (ARP scan)"
    )

    parser.add_argument(
        "-r",
        "--red",
        default=None,
        help="Red/CIDR a escanear (ej: 192.168.1.0/24)",
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=float,
        default=3.0,
        help="Timeout ARP en segundos (default: %(default)s)",
    )
    parser.add_argument(
        "-i",
        "--iface",
        default=None,
        help="Interfaz a usar (opcional)",
    )
    parser.add_argument(
        "-s",
        "--save",
        default=None,
        help="Ruta CSV donde guardar resultados (opcional)",
    )
    parser.add_argument(
        "--json",
        dest="json_output",
        default=None,
        help="Ruta JSON donde guardar resultados (opcional)",
    )
    parser.add_argument(
        "--no-name",
        dest="no_name",
        action="store_true",
        help="No intentar resolver nombres por DNS inversa (más rápido)",
    )
    parser.add_argument(
        "--name-timeout",
        type=float,
        default=1.0,
        help="Timeout para cada gethostbyaddr (default: %(default)s)",
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        default=20,
        help="Máx. hilos para resolución de nombres (default: %(default)s)",
    )
    parser.add_argument(
        "--watch",
        action="store_true",
        help="Monitorizar la red de forma continua",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=30,
        help="Segundos entre escaneos en modo watch (default: %(default)s)",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.red is None:
        args.red = detectar_red_local()
        
    try:
        ipaddress.ip_network(args.red, strict=False)
    except ValueError:
        print(f"Error: la red '{args.red}' no es un CIDR válido (ej: 192.168.1.0/24)")
        sys.exit(1)

    if args.timeout <= 0:
        print("Error: --timeout debe ser mayor que 0")
        sys.exit(1)

    if args.name_timeout <= 0:
        print("Error: --name-timeout debe ser mayor que 0")
        sys.exit(1)

    if args.max_workers <= 0:
        print("Error: --max-workers debe ser mayor que 0")
        sys.exit(1)

    print(f"Escaneando red: {args.red}  (timeout={args.timeout}s)")




    def ejecutar_escaneo():
        return escanear_red(
            args.red,
            timeout=args.timeout,
            iface=args.iface,
            resolve_names=not args.no_name,
            name_timeout=args.name_timeout,
            max_workers=args.max_workers
        )

    try:
        if args.watch:
            monitorizar_red(
                scan_function=ejecutar_escaneo,
                display_function=imprimir_dispositivos,
                interval=args.interval,
            )
            return

        dispositivos = ejecutar_escaneo()
    
    except PermissionError:
        print("Error: se requieren permisos de superusuario para escanear la red")
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado durante el escaneo: {e}")
        sys.exit(1)

    imprimir_dispositivos(dispositivos)

    if args.save:
        guardar_csv(dispositivos, args.save)

    if args.json_output:
        guardar_json(dispositivos, args.json_output)


if __name__ == "__main__":
    main()

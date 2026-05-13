
# -*- coding: utf-8 -*-
"""
=============================
     DEVICES IN WIFI (v1.1.0)
=============================

Escaneador de dispositivos en una red Wi-Fi (basado en ARP) con resolución
de nombres DNS inversa en paralelo usando ThreadPoolExecutor.

Autor: Art-Phy (mejorado)
IMPORTANTE:
  - Requiere permisos de superusuario (sudo) para enviar/recibir paquetes raw.
  - Usa scapy (pip install scapy). En macOS/Ubuntu puede requerir libpcap.
"""

from __future__ import annotations
import ipaddress
import argparse
import ipaddress
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent / "src"))

from src.devices_in_wifi.exporter import guardar_csv, guardar_json
from src.devices_in_wifi.scanner import detectar_red_local, escanear_red, imprimir_dispositivos



def parse_args() -> argparse.Namespace:
    """
    Analiza los argumentos de la línea de comandos.
    """
    parser = argparse.ArgumentParser(description="Escaneador de dispositivos en red Wi-Fi (ARP scan)")
    parser.add_argument("-r", "--red", default=None, help="Red/CIDR a escanear (ej: 192.168.1.0/24)")
    parser.add_argument("-t", "--timeout", type=float, default=3.0, help="Timeout ARP en segundos (default: %(default)s)")
    parser.add_argument("-i", "--iface", default=None, help="Interfaz a usar (opcional)")
    parser.add_argument("-s", "--save", default=None, help="Ruta CSV donde guardar resultados (opcional)")
    parser.add_argument("--json", dest="json_output", default=None, help="Ruta JSON donde guardar resultados (opcional)")
    parser.add_argument("--no-name", dest="no_name", action="store_true", help="No intentar resolver nombres por DNS inversa (más rápido)")
    parser.add_argument("--name-timeout", type=float, default=1.0, help="Timeout para cada gethostbyaddr (default: %(default)s)")
    parser.add_argument("--max-workers", type=int, default=20, help="Máx. hilos para resolución de nombres (default: %(default)s)")
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

    try:
        dispositivos = escanear_red(
            args.red,
            timeout=args.timeout,
            iface=args.iface,
            resolve_names=not args.no_name,
            name_timeout=args.name_timeout,
            max_workers=args.max_workers
        )
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
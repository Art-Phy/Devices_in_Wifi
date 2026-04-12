
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
import sys
import socket
import argparse
from detection import detectar_tipo_dispositivo, detectar_fabricante, construir_nombre
from exporter import guardar_csv, guardar_json
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import ipaddress

# scapy import
from scapy.all import ARP, Ether, srp, conf  # type: ignore


def obtener_nombre(ip: str, timeout: float = 1.0) -> str:
    """
    Intenta obtener el nombre del host mediante DNS inversa.
    Si falla o tarda demasiado, devuelve "Nombre desconocido".

    Args:
        ip: dirección IPv4 en forma de string.
        timeout: tiempo máximo (segundos) para la operación DNS inversa.

    Returns:
        nombre (str) del host o "Nombre desconocido".
    """
    try:
        prev = socket.getdefaulttimeout()
        socket.setdefaulttimeout(timeout)
        nombre = socket.gethostbyaddr(ip)[0]
        socket.setdefaulttimeout(prev)
        return nombre
    except (socket.herror, socket.gaierror, socket.timeout, OSError):
        return "Nombre desconocido"



def _resolver_nombres_paralelo(ips: List[str], timeout: float = 1.0, max_workers: int = 20) -> Dict[str, str]:
    """
    Resuelve una lista de IPs a nombres en paralelo.

    Args:
        ips: lista de direcciones IP (strings).
        timeout: timeout por cada consulta gethostbyaddr.
        max_workers: número máximo de hilos simultáneos.

    Returns:
        diccionario mapping ip -> nombre
    """
    resultados: Dict[str, str] = {}
    if not ips:
        return resultados

    # Ajustar número de workers a la cantidad de ips y al límite pedido
    workers = min(max_workers, len(ips))

    with ThreadPoolExecutor(max_workers=workers) as executor:
        # lanzamos tareas
        future_to_ip = {executor.submit(obtener_nombre, ip, timeout): ip for ip in ips}
        for future in as_completed(future_to_ip):
            ip = future_to_ip[future]
            try:
                nombre = future.result()
            except Exception:
                nombre = "Nombre desconocido"
            resultados[ip] = nombre

    return resultados



def detectar_red_locar() -> str:
    """
    Intenta detectar la red local del equipo y devuelve un CIDR /24.
    Ejemplo: '192.168.1.0/24'

    Returns:
        Red local en formato CIDR    
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            ip_local = s.getsockname()[0]

        red = ipaddress.ip_network(f"{ip_local}/24", strict=False)
        return str(red)
    except OSError:
        return "192.168.1.0/24"



def escanear_red(red: str, timeout: float = 3.0, iface: Optional[str] = None,
                 resolve_names: bool = True, name_timeout: float = 1.0,
                 max_workers: int = 20) -> List[Dict[str, str]]:
    """
    Escanea la red indicada (CIDR) y devuelve una lista de diccionarios con
    'ip', 'mac' y 'nombre'.

    Args:
        red: red en formato CIDR (ej. "192.168.1.0/24").
        timeout: tiempo de espera para las respuestas ARP (segundos).
        iface: interfaz a usar (opcional).
        resolve_names: si True, realiza resolución DNS inversa (paralela).
        name_timeout: timeout individual para cada gethostbyaddr.
        max_workers: máximo de hilos para resolver nombres en paralelo.

    Returns:
        lista de dicts: [{'ip': '192.168.1.2', 'mac': 'aa:bb:cc:dd:ee:ff', 'nombre': 'mi-dispositivo'}, ...]
    """
    if iface:
        conf.iface = iface

    paquete = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=red)
    answered = srp(paquete, timeout=timeout, verbose=0)[0]

    dispositivos: List[Dict[str, str]] = []
    ips = []
    ip_to_mac: Dict[str, str] = {}

    for _, recibido in answered:
        ip = recibido.psrc
        mac = recibido.hwsrc
        ips.append(ip)
        ip_to_mac[ip] = mac

    # Si no queremos resolver nombres, asignamos "Nombre desconocido"
    if not resolve_names:
        for ip in ips:
            mac = ip_to_mac.get(ip, "")
            nombre = "Nombre desconocido"
            fabricante = detectar_fabricante(mac)
            tipo = detectar_tipo_dispositivo(nombre)

            # Heurística extra basada en fabricante cuando no hay hostname
            if tipo == "Unknown":
                if fabricante in ["TP-Link", "Askey", "Cisco", "Netgear", "Ubiquiti", "Huawei"]:
                    tipo = "Router"
                elif fabricante in ["Apple", "Samsung", "Xiaomi", "Google"]:
                    tipo = "Smartphone"
                elif fabricante in ["Philips", "Nest", "Amazon"]:
                    tipo = "IoT Device"
                elif fabricante == "iRobot":
                    tipo = "IoT Device"
                elif fabricante == "Midea":
                    tipo = "IoT Device"

            nombre_mostrable = construir_nombre(nombre, tipo, fabricante)

            dispositivos.append({
                "ip": ip,
                "mac": mac,
                "nombre": nombre_mostrable,
                "tipo": tipo,
                "fabricante": fabricante
            })
        return dispositivos
    

    # Resolución paralela de nombres
    start = time.time()
    ip_to_name = _resolver_nombres_paralelo(ips, timeout=name_timeout, max_workers=max_workers)
    elapsed = time.time() - start

    # Construir lista final
    for ip in ips:
        mac = ip_to_mac.get(ip, "")
        nombre_real = ip_to_name.get(ip, "Nombre desconocido")
        fabricante = detectar_fabricante(mac)
        tipo = detectar_tipo_dispositivo(nombre_real)

        # Heurística extra basada en fabricante cuando no hay hostname
        if tipo == "Unknown":
            if fabricante in ["TP-Link", "Askey", "Cisco", "Netgear", "Ubiquiti", "Huawei"]:
                tipo = "Router"
            elif fabricante in ["Apple", "Samsung", "Xiaomi", "Google"]:
                tipo = "Smartphone"
            elif fabricante in ["Philips", "Nest", "Amazon"]:
                tipo = "IoT Device"
            elif fabricante == "iRobot":
                tipo = "IoT Device"
            elif fabricante == "Midea":
                tipo = "IoT Device"

        nombre_mostrable = construir_nombre(nombre_real, tipo, fabricante)

        dispositivos.append({
            "ip": ip,
            "mac": mac,
            "nombre": nombre_mostrable,
            "tipo": tipo,
            "fabricante": fabricante
        })

    # Información de rendimiento (opcional)
    print(f"(Resolución de {len(ips)} nombres en {elapsed:.2f}s usando hasta {min(max_workers, len(ips))} hilos)")

    return dispositivos


def imprimir_dispositivos(dispositivos: List[Dict[str, str]]) -> None:
    """
    Muestra por pantalla los dispositivos encontrados en un formato legible.
    """
    if not dispositivos:
        print("No se encontraron dispositivos.")
        return

    print("\nDispositivos encontrados:")
    print(f"{'IP':15} {'MAC':20} {'TIPO':18} {'FABRICANTE':20} {'NOMBRE'}")
    print("-" * 120)
    for d in dispositivos:
        print(f"{d['ip']:15} {d['mac']:20} {d['tipo']:18} {d['fabricante']:20} {d['nombre']}")


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
        args.red = detectar_red_locar()
        
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
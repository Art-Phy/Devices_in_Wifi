
from __future__ import annotations

import ipaddress
import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional

from scapy.all import ARP, Ether, conf, srp # type: ignore

from devices_in_wifi.detection import (
    construir_nombre,
    detectar_fabricante,
    detectar_tipo_dispositivo,
)


def obtener_nombre(ip: str, timeout: float = 1.0) -> str:
    """
    Intenta obtener el nombre del host mediante DNS inversa.
    Si falla o tarda demasiado devuelve "Nombre desconocido"
    """
    try:
        prev = socket.getdefaulttimeout()
        socket.setdefaulttimeout(timeout)
        nombre = socket.gethostbyaddr(ip)[0]
        socket.setdefaulttimeout(prev)
        return nombre
    except (socket.error, socket.gaierror, socket.timeout, OSError):
        return "Nombre desconocido"
    


def resolver_nombres_paralelo(ips: List[str], timeout: float = 1.0, max_workers: int = 20) -> Dict[str, str]:
    """
    Resuelve una lista de IPs a nombres en paralelo.
    """
    resultados: Dict[str, str] = {}
    if not ips:
        return resultados
    
    workers = min(max_workers, len(ips))

    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_ip = {executor.submit(obtener_nombre, ip, timeout): ip for ip in ips}
        for future in as_completed(future_to_ip):
            ip = future_to_ip[future]
            try:
                nombre = future.result()
            except Exception:
                nombre = "Nombre desconocido"
            resultados[ip] = nombre

    return resultados



def detectar_red_local() -> str:
    """
    Intenta detectar la red local del equipo y devuelve un CIDR /24.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            ip_local = s.getsockname()[0]

        red = ipaddress.ip_network(f"{ip_local}/24", strict=False)
        return str(red)
    except OSError:
        return "192.168.1.0/24"
    


def inferir_tipo_por_fabricante(tipo: str, fabricante: str) -> str:
    """
    Aplica una heurística adicional basada en fabricante cuando no hay hostname útil.
    """
    if tipo != "Unknown":
        return tipo
    
    
    if fabricante in ["TP-Link", "Askey", "Cisco", "Netgear", "Ubiquiti", "Huawei"]:
        return "Router"
    if fabricante in ["Apple", "Samsung", "Xiaomi", "Google"]:
        return "Smartphone"
    if fabricante in ["Philips", "Nest", "Amazon", "iRobot", "Midea"]:
        return "IoT Device"

    return "Unknown"



def escanear_red(red: str, timeout: float = 3.0, iface: Optional[str] = None, resolve_names: bool = True, name_timeout: float = 1.0, max_workers: int = 20) -> List[Dict[str, str]]:
    """
    Escanea la red indicada y devuelve una lista de dispositivos detectados.
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

    if not resolve_names:
        for ip in ips:
            mac = ip_to_mac.get(ip, "")
            nombre_real = "Nombre desconocido"
            fabricante = detectar_fabricante(mac)
            tipo = detectar_tipo_dispositivo(nombre_real)
            tipo = inferir_tipo_por_fabricante(tipo, fabricante)
            nombre_mostrable = construir_nombre(nombre_real, tipo, fabricante)

            dispositivos.append(
                {
                    "ip": ip,
                    "mac": mac,
                    "nombre": nombre_mostrable,
                    "tipo": tipo,
                    "fabricante": fabricante,
                }
            )
        return dispositivos
    
    start = time.time()
    ip_to_name = resolver_nombres_paralelo(ips, timeout=name_timeout, max_workers=max_workers)
    elapsed = time.time() - start

    for ip in ips:
        mac = ip_to_mac.get(ip, "")
        nombre_real = ip_to_name.get(ip, "Nombre desconocido")
        fabricante = detectar_fabricante(mac)
        tipo = detectar_tipo_dispositivo(nombre_real)
        tipo = inferir_tipo_por_fabricante(tipo, fabricante)
        nombre_mostrable = construir_nombre(nombre_real, tipo, fabricante)

        dispositivos.append(
            {
                "ip": ip,
                "mac": mac,
                "nombre": nombre_mostrable,
                "tipo": tipo,
                "fabricante": fabricante,
            }
        )

    print(
        f"(Resolución de {len(ips)} nombres en {elapsed:.2f}s usando hasta {min(max_workers, len(ips))} hilos)"
    )

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

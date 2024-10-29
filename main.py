### Escaneador de usuarios en red Wifi ###

from scapy.all import ARP, Ether, srp
import socket

def obtener_nombre(ip):
    try:
        # se realiza una búsqueda inversa de DNS para obtener el nombre del dispositivo
        nombre = socket.gethostbyaddr(ip)[0]
    except socket.herror:
        nombre = "Nombre desconocido" # si no tiene nombre
    return nombre

def escanear_red(red):
    paquete = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=red)
    result = srp(paquete, timeout=3, verbose=0)[0]

    dispositivos = []
    for sent, received in result:
        ip = received.psrc
        mac = received.hwsrc
        nombre = obtener_nombre(ip)
        dispositivos.append({'ip': ip, 'mac': mac, 'nombre': nombre})

    return dispositivos

# definimos nuestro rango de red
red = "192.168.1.0/24"

# escanea la red
dispositivos = escanear_red(red)

# se muestran los dispositivos conectados
print(" Dispositivos conectados: ")
for dispositivo in dispositivos:
    print(f"IP: {dispositivo['ip']}, MAC: {dispositivo['mac']}, Nombre: {dispositivo['nombre']}")

# ejecútalo en tu terminal, te hacen falta permisos de superusuario

def detectar_tipo_dispositivo(nombre: str) -> str:
    """
    Intenta clasificar el tipo de dispositivo a partor del hostname.

    Args:
        nombre: hostname resuelto por DNS inversa.
    
    Returns:
        Tipo de dispositivo estimado.
    """
    hostname = nombre.lower()

    if hostname == "nombre desconocido":
        return "Unknown"
    
    if any(x in hostname for x in ["router", "gateaway", "livebox", "movistar", "vodafone", "digi"]):
        return "Router"
    
    if any(x in hostname for x in ["iphone", "android", "xiaomi", "redmi", "mobile", "telefon", "phone"]):
        return "Smartphone"

    if any(x in hostname for x in ["tv", "bravia", "smarttv", "lg"]):
        return "Smart TV"

    if any(x in hostname for x in ["printer", "epson", "brother", "hp", "canon"]):
        return "Printer"

    if any(x in hostname for x in ["pc", "desktop", "laptop", "macbook", "thinkpad", "acer"]):
        return "Laptop/Desktop"
    
    if any (x in hostname for x in ["echo", "nest", "cam", "camera", "sensor", "plug"]):

        return "Unknown"



def detectar_fabricante(mac: str) -> str:
    """
    Intenta identificar el fabricante a partir del prefijo OUI de la MAC.

    Args:
        mac: dirección MAC del dispositivo.
    
    Returns:
        Nombre estimado del fabricante
    """
    oui = mac.upper().replace("-", ":")[0:8]

    fabricantes = {
    "B8:27:EB": "Raspberry Pi Foundation",
    "DC:A6:32": "Raspberry Pi Foundation",
    "E4:5F:01": "Raspberry Pi Foundation",
    "FC:FB:FB": "Apple",
    "F0:18:98": "Apple",
    "3C:52:82": "Apple",
    "28:CF:E9": "Apple",
    "C8:69:CD": "Apple",
    "48:8F:5A": "Huawei",
    "F4:F2:6D": "Samsung",
    "90:9F:33": "LG",
    "00:1A:79": "Cisco",
    "00:1B:63": "Apple",
    "00:1E:C2": "ASUSTek",
    "00:09:5B": "Netgear",
    "A4:2B:B0": "TP-Link",
    "30:68:93": "TP-Link",
    "FC:EC:DA": "Ubiquiti",
    "C0:56:27": "Belkin",
    "18:B4:30": "Nest",
    "44:65:0D": "Amazon",
    "00:17:88": "Philips",
    "EC:B5:FA": "Philips",
    "EC:FA:BC": "Xiaomi",
    "B8:7B:D4": "Google",
    "3C:20:93": "Midea",
    "4C:B9:EA": "iRobot",
    "C8:B4:22": "Askey"
}

    return fabricantes.get(oui, "Desconocido")


def construir_nombre(nombre: str, tipo: str, fabricante: str) -> str:
    """
    Devuelve un nombre legible para mostrar por pantalla.
    Si hay hostname real lo usa, si no lo hay contruye un fallback con fabricante y tipo.
    """
    if nombre != "Nombre desconocido":
        return nombre
    
    if fabricante != "Desconocido" and tipo != "Unkown":
        return f"{fabricante} {tipo}"
    
    if fabricante != "Desconocido":
        return f"{fabricante} device"
    
    if tipo != "Unknown":
        return tipo
    
    return "Nombre desconocido"

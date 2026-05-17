### Devices in WiFi 📡

<p align="left">
  <img src="https://img.shields.io/badge/python-3.10+-blue.svg" />
  <img src="https://img.shields.io/badge/CLI-Network%20Scanner-orange" />
  <img src="https://img.shields.io/badge/Scapy-Network%20Tools-red" />
  <img src="https://img.shields.io/badge/Tests-pytest-green" />
  <img src="https://img.shields.io/badge/Status-v1.5.0%20Stable-success" />
  <img src="https://img.shields.io/badge/License-MIT-lightgrey" />
</p>

Herramienta **CLI desarrollada en Python** que permite escanear una red local y detectar los dispositivos conectados a ella, mostrando información como dirección **IP**, **MAC** y nombre de host opcional.

---

### ✨ Funcionalidades

#### Core

- Escaneo ARP de la red local.
- Detección de dispositivos activos.
- Obtención de dirección **IP** y **MAC**.
- Resolución opcional de **hostname** mediante reverse DNS.
- Detección automática de red local si no se especifica rango.

---

#### 🧠 Enriquecimiento de datos

- Detección heurística del **tipo de dispositivo**:
  - Router
  - Smartphone
  - Smart TV
  - IoT Device
  - Printer
  - Laptop/Desktop

- Identificación del fabricante a partir de la **MAC (OUI)**
- Generación de *nombres amigables* cuando no hay DNS disponible:
  - `Askey Router`
  - `Apple Smartphone`
  - `Philips IoT Device`

---

#### CLI Features

- Selección manual del rango de red (`-r`)
- Selección de interfaz de red (`-i`)
- Desactivación de reverse DNS (`--no-name`)
- Timeout configurable (`--timeout`)
- Timeout DNS configurable (`--name-timeout`)
- Control de concurrencia (`--max-workers`)
- Validación robusta de argumentos
- Manejo de errores amigable

---

#### 💾 Export

- Exportación a **CSV**
- Exportación a **JSON**
- Datos exportados incluyen:
  - IP
  - MAC
  - Tipo
  - Fabricante
  - Nombre

---

#### Opciones CLI
```
-r, --red      -> Red/CIDR a escanear
-i, --iface    -> Interfaz de red
-s, --save     -> Guardar resultados en CSV
--json         -> Guardar resultados en JSON
--no-name      -> No resolver nombres de host
--timeout      -> Timeout ARP
--max-workers  -> Número de workers concurrentes
--name-timeout -> Timeout para resolución DNS
```

#### 📊 Ejemplo de salida
```bash
Escaneando red: 192.168.1.0/24  (timeout=3.0s)

Dispositivos encontrados:

IP              MAC                  TIPO               FABRICANTE           NOMBRE
------------------------------------------------------------------------------------------------------------------------
192.168.1.1     c8:b4:22:c6:bd:40    Router             Askey                Askey Router
192.168.1.34    ec:b5:fa:18:f0:dd    IoT Device         Philips              Philips IoT Device
192.168.1.36    b8:7b:d4:df:8f:ae    Smartphone         Google               Google Smartphone
192.168.1.37    c8:69:cd:5b:a0:43    Smartphone         Apple                Apple Smartphone
192.168.1.45    30:68:93:9d:a1:ef    Router             TP-Link              TP-Link Router
```
El tiempo de resolución de nombres depende del número de dispositivos encontrados
y de los parámetros `--max-workers` y `--name-timeout`.

---

#### 🛠️ Stack tecnológico

- **Lenguaje:** Python
- **Networking:** Scapy
- **CLI:** argparse
- **Resolución DNS:** socket
- **Concurrencia:** concurrent.futures
- **Exportación:** CSV/JSON
- **Testing:** pytest
- **Control de versiones:** Git + GitFlow

---

#### Clonar el repositorio

```bash
git clone https://github.com/Art-Phy/Devices_in_Wifi.git
cd Devices_in_Wifi

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```
---

#### 🧠 Decisiones técnicas destacables
- Escaneo ARP con Scapy.
- Resolución DNS paralela para mejorar rendimiento.
- Uso de **ThreadPoolExecutor** para paralelizar consultas DNS.
- Validación de entrada con **ipaddress**
- Identificación por fabricante mediante **OUI**
- Arquitectura modular con separación de responsabilidades.
- Testing automatizado con **pytest**
- Refactor progresivo orientado a mantenimiento.
- Versionado semántico con releases claras.
- Flujo GitFlow (`main`, `develop`, `feature/*`).

---
#### 🧪 Testing
```
pytest
```
- detección heurística
- fabricante OUI
- naming fallback
- exportación CSV
- exportación JSON
- impresión de resultados
- autodetección de red
- escaneo mockeado
- parsing CLI

---

#### 🔭 Posibles extensiones futuras (no implementadas)
- Interfaz web ligera para visualizar dispositivos detectados.
- Monitorización continua de la red.
- Alertas cuando aparece un nuevo dispositivo.
- Fingerprinting más avanzado.
- Base de datos OUI completa y externa.
- Exportación a HTML.

---

### 📁 Project Structure
```
Devices_in_Wifi
│
├── src/
│   └── devices_in_wifi/
│       ├── __init__.py
│       ├── detection.py
│       ├── exporter.py
│       └── scanner.py
│
├── tests/
│   ├── conftest.py
│   ├── test_detection.py
│   ├── test_exporter.py
│   ├── test_scanner.py
│   └── test_main.py
│
├── main.py
├── README.md
├── CHANGELOG.md
├── requirements.txt
├── LICENSE.md
└── .gitignore
```
---

> [!TIP]
> ###### Si consideras útil el repositorio, apóyalo hanciendo "★ Star" 
### Devices in WiFi 📡

<p align="left">
  <img src="https://img.shields.io/badge/python-3.10+-blue.svg" />
  <img src="https://img.shields.io/badge/CLI-Network%20Scanner-orange" />
  <img src="https://img.shields.io/badge/Scapy-Network%20Tools-red" />
  <img src="https://img.shields.io/badge/Status-Portfolio%20Project-success" />
  <img src="https://img.shields.io/badge/License-MIT-lightgrey" />
</p>

Herramienta **CLI desarrollada en Python** que permite escanear una red local y detectar los dispositivos conectados a ella, mostrando información como dirección **IP**, **MAC** y nombre de host opcional.

El proyecto está enfocado en demostrar habilidades en **programación de red con Python**, desarrollo de herramientas CLI, procesamiento concurrente y buenas prácticas de desarrollo.

---

### ✨ Funcionalidades

#### Core

- Escaneo ARP de la red local.
- Detección de dispositivos activos.
- Obtención de dirección **IP** y **MAC**.
- Resolución opcional de **hostname** mediante reverse DNS.

---

#### 🧠 Enriquecimiento de datos

- Detección heurística del **tipo de dispositivo**:
  - Router
  - Smartphone
  - Smart TV
  - IoT Device
  - etc.

- Identificación del **fabricante** a partir de la MAC (OUI).
- Generación de **nombres amigables** cuando no hay DNS disponible:
  - `TP-Link Router`
  - `Apple Smartphone`
  - `Philips IoT Device`

---

#### CLI Features

- Detección automática de la red local si no se especifica `-r`.
- Selección manual del rango de red.
- Selección de interfaz de red.
- Control de concurrencia (`--max-workers`).
- Timeout configurable (`--name-timeout`).
- Desactivación de resolución DNS (`--no-name`).
- Validación de argumentos de entrada.
- Manejo de errores claro y controlado.

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
--max-workers  -> Número de workers concurrentes
--name-timeout -> Timeout para resolución DNS
```

#### 📊 Ejemplo de salida
```bash
192.168.1.1 00:11:22:33:44:55 router
192.168.1.10 AA:BB:CC:DD:EE:FF laptop
192.168.1.15 12:34:56:78:90:AB smart-tv
192.168.1.20 7C:D1:C3:91:44:F2 Nombre desconocido
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
```
---

#### 🧠 Decisiones técnicas destacables
- Uso de Scapy para escaneos ARP a bajo nivel. 
- Resolución de nombres mediante reverse **DNS lookup**.
- Uso de **ThreadPoolExecutor** para paralelizar consultas DNS.
- Validación de entrada con **ipaddress**
- Uso de OUI para identificación de fabricante.
- Manejo de errores para mejorar la experiencia CLI.
- Diseño simple y autocontenido orientado a herramientas reales.
- Arquitectura modular preparada para futuras mejoras.
- Versionado semántico con releases claras.
- Flujo GitFlow (`main`, `develop`, `feature/*`).

---

#### 🔭 Posibles extensiones futuras (no implementadas)
- Interfaz web ligera para visualizar dispositivos detectados.
- Monitorización continua de la red.
- Alertas cuando aparece un nuevo dispositivo.
- Identificación más precisa por fingerprinting.
- Base de datos OUI completa y externa.
- Test automatizados con pytest.

---

### 📁 Project Structure
```
Devices_in_Wifi
│
├── main.py         # Punto de entrada CLI
├── scanner.py      # Escaneo de red y resolución DNS
├── detection.py    # Clasificación de dispositivos
├── exporter.py     # Exportación de datos
├── README.md
├── CHANGELOG.md
├── requirements.txt
└── .gitignore
```
---

> [!TIP]
> ###### Si consideras útil el repositorio, apóyalo hanciendo "★ Star" 
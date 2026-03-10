### Devices in WiFi 📡

<p align="left">
  <img src="https://img.shields.io/badge/python-3.10+-blue.svg" />
  <img src="https://img.shields.io/badge/CLI-Network%20Scanner-orange" />
  <img src="https://img.shields.io/badge/Scapy-Network%20Tools-red" />
  <img src="https://img.shields.io/badge/Status-Portfolio%20Project-success" />
  <img src="https://img.shields.io/badge/License-MIT-lightgrey" />
</p>

Herramienta **CLI desarrollada en Python** que permite escanear una red local y detectar los dispositivos conectados a ella, mostrando información como dirección **IP**, **MAC** y nombre de host opcional.

El objetivo del proyecto es demostrar conocimientos de **programación en Python aplicada a redes**, desarrollo de **herramientas de línea de comandos**, procesamiento concurrente y buenas prácticas de desarrollo y control de versiones.

---

### ✨ Funcionalidades

#### Core

- Escaneo ARP de la red local.
- Detección de dispositivos activos.
- Obtención de dirección **IP** y **MAC**.
- Resolución opcional de **hostname** mediante reverse DNS.

#### CLI Features

- Selección manual del rango de red.
- Selección de interfaz de red.
- Control del número de workers concurrentes.
- Desactivación opcional de resolución de nombres.
- Timeout configurable para resolución DNS.

#### Export

- Exportación de resultados a **CSV**.
- Salida clara y legible en consola.

---

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
- **Exportación:** CSV
- **Testing:** pytest
- **Control de versiones:** Git + GitFlow

---

#### Clonar el repositorio

```bash
git clone https://github.com/Art-Phy/Devices_in_Wifi.git
cd Devices_in_Wifi
```

#### 🧠 Decisiones técnicas destacables
- Uso de Scapy para realizar escaneos ARP en la red local.
- Resolución de nombres mediante reverse **DNS lookup**.
- Uso de concurrencia con ThreadPoolExecutor para acelerar la resolución de hostnames.
- Interfaz CLI flexible mediante argparse.
- Arquitectura modular preparada para futuras mejoras.
- Versionado semántico con releases claras.
- Flujo GitFlow aplicado estrictamente (`main`, `develop`, `feature/*`).

#### 🔭 Posibles extensiones futuras (no implementadas)
- Detección de fabricante mediante OUI lookup.
- Identificación de tipo de dispositivo.
- Exportación adicional a JSON.
- Interfaz web ligera para visualizar dispositivos detectados.
- Monitorización continua de la red.
- Alertas cuando aparece un nuevo dispositivo.

---

### 📁 Project Structure
- Devices_in_Wifi
│
├── - main.py # CLI entrypoint del escáner
├── - README.md # Documentación del proyecto
├── - CHANGELOG.md # Historial de cambios y versiones
├── - requirements.txt # Dependencias del proyecto
├── - LICENSE
└── - .gitignore


El proyecto está diseñado como una **herramienta CLI simple y autocontenida**, donde `main.py` contiene la lógica principal del escaneo de red, resolución de nombres y exportación de resultados.

---

> [!TIP]
> ###### Si consideras útil el repositorio, apóyalo hanciendo "★ Star" 
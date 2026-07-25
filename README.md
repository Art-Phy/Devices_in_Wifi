## Devices in WiFi

<p align="left">
  <img src="https://img.shields.io/badge/python-3.10+-blue.svg" />
  <img src="https://img.shields.io/badge/CLI-Network%20Scanner-orange" />
  <img src="https://img.shields.io/badge/Scapy-Network%20Tools-red" />
  <img src="https://img.shields.io/badge/Testing-pytest-green" />
  <img src="https://img.shields.io/badge/Status-v1.6.0%20Stable-success" />
  <img src="https://img.shields.io/badge/License-MIT-lightgrey" />
</p>

Herramienta **CLI desarrollada en Python** para escanear una red local, detectar los dispositivos conectados y mostrar información enriquecida como **IP**, **MAC**, **tipo de dispositivo**, **fabricante** y nombre amigable.

También incluye un modo de **monitorización continua**, que permite repetir el escaneo automáticamente con un intervalo configurable.

---

### Funcionalidades

#### Escaneo de red

- Escaneo ARP de la red local.
- Detección de dispositivos activos.
- Obtención de dirección **IP** y **MAC**.
- Resolución opcional de nombres mediante DNS inversa.
- Detección automática de la red local si no se especifica un rango.
- Selección manual de red en formato CIDR.
- Selección opcional de interfaz de red.

#### Identificación de dispositivos

- Clasificación heurística del tipo de dispositivo:
  - Router
  - Smartphone
  - Smart TV
  - IoT Device
  - Printer
  - Laptop/Desktop
  - Unknown

- Detección del fabricante mediante el prefijo **MAC/OUI**.
- Generación de nombres amigables cuando no existe hostname DNS:
  - `Askey Router`
  - `Apple Smartphone`
  - `Philips IoT Device`

#### Monitorización continua

- Escaneo periódico de la red mediante `--watch`.
- Intervalo configurable entre escaneos.
- Finalización limpia mediante `Ctrl+C`.
- Mensajes informativos entre cada ejecución.
- Preparado para incorporar futuras alertas de nuevos dispositivos.

#### Experiencia CLI

- Validación del rango de red.
- Validación de timeouts y número de workers.
- Validación del intervalo de monitorización.
- Control de concurrencia para la resolución DNS.
- Mensajes de error claros.
- Comprobación previa de permisos de administrador.
- Salida controlada sin tracebacks innecesarios.

#### Exportación

- Exportación a **CSV**.
- Exportación a **JSON**.

Los datos exportados incluyen:

- IP
- MAC
- Tipo de dispositivo
- Fabricante
- Nombre

---

### Instalación

Clonar el repositorio:

```bash
git clone https://github.com/Art-Phy/Devices_in_Wifi.git
cd Devices_in_Wifi
```

Crear y activar un entorno virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instalar las dependencias:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

### Uso

#### Escaneo básico

```bash
sudo .venv/bin/python main.py
```

Si no se especifica una red, la herramienta intenta detectar automáticamente la red local.

#### Especificar una red manualmente

```bash
sudo .venv/bin/python main.py -r 192.168.1.0/24
```

#### Escaneo sin resolución DNS inversa

```bash
sudo .venv/bin/python main.py --no-name
```

#### Exportar resultados a CSV

```bash
sudo .venv/bin/python main.py -s dispositivos.csv
```

#### Exportar resultados a JSON

```bash
sudo .venv/bin/python main.py --json dispositivos.json
```

#### Exportar a CSV y JSON

```bash
sudo .venv/bin/python main.py \
  -s dispositivos.csv \
  --json dispositivos.json
```

---

### Monitorización continua

Para escanear la red periódicamente:

```bash
sudo .venv/bin/python main.py --watch
```

El intervalo predeterminado es de 30 segundos.

Para establecer un intervalo personalizado:

```bash
sudo .venv/bin/python main.py --watch --interval 10
```

La monitorización puede detenerse mediante:

```text
Ctrl+C
```

---

### Opciones CLI

| Opción | Descripción |
|--------|-------------|
| `-r`, `--red` | Red o rango CIDR que se desea escanear |
| `-t`, `--timeout` | Timeout del escaneo ARP |
| `-i`, `--iface` | Interfaz de red que se desea utilizar |
| `-s`, `--save` | Ruta para exportar los resultados a CSV |
| `--json` | Ruta para exportar los resultados a JSON |
| `--no-name` | Omite la resolución de nombres mediante DNS inversa |
| `--name-timeout` | Timeout individual para cada consulta DNS |
| `--max-workers` | Número máximo de workers para resolver nombres |
| `--watch` | Activa la monitorización continua |
| `--interval` | Segundos entre escaneos en modo monitorización |

La ayuda completa puede consultarse mediante:

```bash
python main.py --help
```

---

### Ejemplo de salida

```text
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

Ejemplo del modo monitorización:

```text
Monitorizando la red cada 10 segundos. Pulsa Ctrl+C para detener.

Dispositivos encontrados:
...

Próximo escaneo en 10 segundos...
```

---

### Stack tecnológico

- **Lenguaje:** Python
- **Networking:** Scapy
- **CLI:** argparse
- **Resolución DNS:** socket
- **Concurrencia:** ThreadPoolExecutor
- **Exportación:** CSV y JSON
- **Testing:** pytest
- **Control de versiones:** Git + GitFlow

---

### Testing

Ejecutar todos los tests:

```bash
pytest
```

La suite actual incluye **21 tests** que cubren:

- Detección heurística del tipo de dispositivo.
- Identificación del fabricante por OUI.
- Construcción de nombres amigables.
- Exportación a CSV.
- Exportación a JSON.
- Autodetección de red local.
- Formato de salida en consola.
- Escaneo de red mediante mocks.
- Parsing de argumentos CLI.
- Comprobación de permisos.
- Monitorización continua.
- Detención mediante `KeyboardInterrupt`.
- Respeto del intervalo configurado.

---

### Decisiones técnicas

- Uso de **Scapy** para realizar escaneos ARP.
- Resolución DNS inversa paralela mediante `ThreadPoolExecutor`.
- Clasificación heurística ligera y mantenible.
- Identificación de fabricantes mediante prefijos OUI.
- Nombres amigables como fallback cuando no existe hostname.
- Detección automática de la red local.
- Separación de responsabilidades en módulos independientes.
- Monitorización desacoplada mediante funciones inyectables.
- Uso de mocks para probar el escaneo sin acceder a una red real.
- Comprobación previa de privilegios para evitar errores poco claros.
- Versionado semántico y flujo GitFlow.

---

### Estructura del proyecto

```text
Devices_in_Wifi/
├── src/
│   └── devices_in_wifi/
│       ├── __init__.py
│       ├── detection.py
│       ├── exporter.py
│       ├── monitor.py
│       └── scanner.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_detection.py
│   ├── test_exporter.py
│   ├── test_main.py
│   ├── test_monitor.py
│   └── test_scanner.py
├── main.py
├── README.md
├── CHANGELOG.md
├── requirements.txt
├── LICENSE.md
└── .gitignore
```

---

###  Posibles extensiones futuras

- Alertas cuando aparece un nuevo dispositivo.
- Base de datos OUI completa y externa.
- Interfaz web ligera para visualizar dispositivos detectados.
- Fingerprinting más avanzado.
- Exportación a HTML.

---

>[!TIP]
>##### Si el proyecto te resulta útil, una ⭐ en GitHub siempre alegra más que encontrar un dispositivo desconocido conectado a la red.
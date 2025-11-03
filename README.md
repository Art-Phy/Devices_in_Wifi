### Bienvenid@s a Tu Wifi_Scanner.

##### ✨ Muestra la dirección IP, MAC y nombre del dispositivo (si lo tiene). Es necesario correrlo como superusuario.

#### 📋 Qué he usado

- 👨‍💻 Visual Studio Code
- 📘 Libro "Curso Intensivo de Python" de Eric Matthes  
- 📘 Libro "Git & GitHub desde cero" de Brais Moure
- 🌐 [Documentación de Git](https://git-scm.com)
- 🌐 [Documentación de GitHub](https://docs.github.com/es)
- 🌐 [Documentación Markdown](https://markdown.es)

---

#### 🧭 Guía rápida de uso (comandos)

> ⚠️ Este script requiere permisos de superusuario (sudo) para funcionar correctamente.

- **Escaneo básico (por defecto)**  
  Escanea la red `192.168.1.0/24` y muestra los dispositivos conectados.  
  👉 `sudo python wifi_scanner.py`

- **Escanear una red específica**  
  Permite indicar una red manualmente (por ejemplo `10.0.0.0/24`).  
  👉 `sudo python wifi_scanner.py -r 10.0.0.0/24`

- **Guardar resultados en un archivo CSV**  
  Guarda los resultados en un archivo (por ejemplo `dispositivos.csv`).  
  👉 `sudo python wifi_scanner.py -s dispositivos.csv`

- **Escaneo sin resolución de nombres (más rápido)**  
  Evita las consultas DNS inversas.  
  👉 `sudo python wifi_scanner.py --no-name`

- **Configurar número de hilos y timeout**  
  Aumenta la velocidad de resolución DNS inversa si la red es grande.  
  👉 `sudo python wifi_scanner.py --max-workers 40 --name-timeout 1.5`

- **Escanear con interfaz específica (opcional)**  
  Si tienes varias interfaces de red, indica cuál usar (ejemplo: `en0`, `wlan0`, `eth0`).  
  👉 `sudo python wifi_scanner.py -i en0`

- **Mostrar ayuda completa**  
  Muestra todas las opciones y descripciones de los argumentos.  
  👉 `python wifi_scanner.py -h`

---

> [!TIP]
> ###### Si consideras útil el repositorio, apóyalo haciendo "★ Star" ¡Gracias! 🚀


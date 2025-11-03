## 📜 CHANGELOG

### [v1.1.0] - 2025-11-03

#### 🚀 Mejoras
- Añadido escaneo de red con resolución **DNS inversa en paralelo** usando `ThreadPoolExecutor`.
- Ahora el usuario puede especificar manualmente la red mediante el argumento `-r` (ej. `-r 10.0.0.0/24`).
- Implementada opción `--no-name` para **omitir resolución de nombres** y acelerar el escaneo.
- Soporte para guardar los resultados en un archivo CSV mediante el argumento `-s`.
- Añadidos argumentos avanzados:
  - `--max-workers` → controla el número de hilos usados en la resolución.
  - `--name-timeout` → ajusta el tiempo máximo para cada búsqueda DNS inversa.
- Mejorado el formato de salida en terminal (alineación de columnas y formato legible).
- Documentación y comentarios en el código completamente revisados.

#### 🧰 Correcciones
- Manejo robusto de excepciones en `gethostbyaddr` para evitar bloqueos.
- Ajuste en el uso de `socket.setdefaulttimeout()` para restaurar correctamente el valor anterior.
- Validación de rutas al guardar CSV.

#### 🧩 Otros cambios
- Se añadió `argparse` para control completo desde terminal.
- Se añadieron **type hints** y docstrings detallados para mejorar la legibilidad y mantenibilidad del código.
- Limpieza general del código (PEP8 + nombres más descriptivos).

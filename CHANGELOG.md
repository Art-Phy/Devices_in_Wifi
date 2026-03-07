
All notable changes to this project will be documented in this file.

The format is inspired by **Keep a Changelog** and the project follows **Semantic Versioning**.

---

### [Unreleased]

#### Changed

- Rewritten project **README** with portfolio-style documentation.
- Improved repository presentation and documentation structure.

---

### [1.1.0] - 2025-11-03

#### Added

- Network scanning with **parallel reverse DNS resolution** using `ThreadPoolExecutor`.
- Ability to manually specify the network range using `-r` (e.g. `-r 10.0.0.0/24`).
- Option `--no-name` to **skip hostname resolution** and speed up scanning.
- Option to export detected devices to **CSV** using `-s`.
- Advanced CLI arguments:
  - `--max-workers` → controls number of threads used for hostname resolution.
  - `--name-timeout` → sets timeout for each reverse DNS lookup.
- Improved terminal output formatting with aligned columns.
- Added **argparse CLI interface**.
- Added **type hints and detailed docstrings** to improve maintainability.

#### Fixed

- Robust exception handling in `socket.gethostbyaddr` to prevent blocking.
- Correct restoration of `socket.setdefaulttimeout()` value.
- Validation when saving CSV files.

#### Changed

- General code cleanup.
- Improved naming and readability following **PEP8 conventions**.
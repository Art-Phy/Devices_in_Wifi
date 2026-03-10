
All notable changes to this project will be documented in this file.

The format is inspired by **Keep a Changelog** and the project follows **Semantic Versioning**.

---

### [1.2.0] - 10.03.2025

#### Changed

- Rewritten project **README** with portfolio-style documentation.
- Added **Project Structure** section to improve repository readability.
- Added **Example Output** section showing CLI usage results.
- Standardized **CHANGELOG** format following Keep a Changelog style.

#### Fixed

- Updated `scapy` dependency to a valid PyPI version.
- Added UTF-8 encoding declaration to prevent non-ASCII errors.

#### Maintenance

- Improved `.gitignore` for Python projects.
- Cleaned repository structure and documentation consistency.

---

### [1.1.0] - 03.11.2025

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

All notable changes to this project will be documented in this file.

The format is inspired by **Keep a Changelog** and the project follows **Semantic Versioning**.

---

### [1.6.0] - 25.07.2026

#### Added

- Continuous network monitoring through the new `--watch` CLI option.
- Configurable delay between scans using `--interval`.
- New `monitor.py` module dedicated to continuous monitoring logic.
- Graceful monitoring shutdown using `Ctrl+C`.
- Administrator permission check before starting an ARP scan.
- Friendly instructions showing how to rerun the command with `sudo`.
- Automated tests for continuous monitoring behavior.
- Automated test for administrator permission validation.

#### Changed

- Refactored CLI argument definitions for improved readability and maintainability.
- Improved help messages for monitoring-related arguments.
- Centralized scan execution so normal and watch modes reuse the same logic.
- Improved monitoring output with information about the next scheduled scan.
- Updated project documentation with continuous monitoring usage and examples.
- Updated the testing badge to reflect 21 passing tests.

#### Fixed

- Validation now rejects monitoring intervals equal to or lower than zero.
- Improved behavior when the application is executed without the privileges required by Scapy.
- Corrected monitoring output messages and related test expectations.

---

### [1.5.0] - 17.05.2026

#### Added

- Automated test suite with **pytest**.
- Unit tests for device classification heuristics.
- Unit tests for MAC vendor detection logic.
- Unit tests for fallback naming behavior.
- Unit tests for CSV export.
- Unit tests for JSON export.
- Unit tests for scanner output formatting.
- Mocked tests for network scanning behavior.
- CLI argument parsing tests.
- `tests/conftest.py` to support clean package imports.

#### Changed

- Refactored project structure to follow the **src layout** pattern:
  - `src/devices_in_wifi/`
  - `tests/`
- Cleaned package imports across the project.
- Improved project maintainability through clearer package organization.
- Updated README documentation with testing, architecture and current feature set.

#### Fixed

- Resolved import path inconsistencies between runtime execution and test environment.
- Improved project portability and package consistency.

---

### [1.4.0] - 19.04.2026

#### Added

- Heuristic device type detection based on resolved hostname.
- MAC vendor detection using OUI prefixes.
- Friendly fallback device naming when reverse DNS is not available.
- Automatic local network detection when no CIDR range is provided.
- JSON export support for detected devices.

#### Changed

- Improved CLI argument validation for network range and numeric parameters.
- Improved scan-time error handling with clearer user-facing messages.
- Refactored the project into dedicated modules:
  - `scanner.py` for network scanning and DNS resolution
  - `detection.py` for classification heuristics
  - `exporter.py` for CSV and JSON export

#### Fixed

- Improved output consistency by including detected device type and vendor in exported results.
- Improved usability when hostnames are not available in the local network.

---

### [1.3.0] - 04.04.2026

#### Added

- Automatic local network detection when no custom CIDR range is provided.
- JSON export support through a dedicated CLI argument.

#### Changed

- Improved CLI argument validation for network range and numeric parameters.
- Improved error handling during scan execution with clearer user-facing messages.

#### Fixed

- More robust execution flow for invalid input values and scan-time failures.

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
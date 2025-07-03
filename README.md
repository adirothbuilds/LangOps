# LangOps

[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![SDK](https://img.shields.io/badge/SDK-LangOps-green)](https://github.com/adirothbuilds/LangOps)

LangOps is a modular SDK for building AI-powered DevOps tools.
It provides a flexible framework for parsing logs, interacting with LLMs, and analyzing failure patterns across CI/CD pipelines.
Designed with extensibility in mind, it supports plug-and-play parsers, model-agnostic LLM clients, and clean abstractions for building intelligent automation agents.

---

## 🚀 Features

- **LLM Integration:** Built-in support for OpenAI's GPT models with synchronous and asynchronous completions.
- **Abstract Base Classes:** Consistent design for log parsing and language model integration.
- **Error Extraction:** Advanced utilities for filtering and extracting error logs.
- **Parser Registry:** Decorator-based system for managing parsers.
- **File Utilities:** Tools for handling and filtering log files.
- **100% Test Coverage:** Comprehensive unit tests for all components.

---

## 🛠️ Quick Start

1. **Install dependencies:**

   ```sh
   poetry install
   ```

2. **Run tests:**

   ```sh
   make test
   ```

3. **Run coverage:**

   ```sh
   make coverage
   ```

---

## 📂 Project Structure

- `LangOps/` — Core library modules
  - `llm/` — Language model integrations
  - `parser/` — Log parsing and error extraction
  - `alert/` — Alerting mechanisms
  - `prompt/` — Flexible prompt handling for LLMs
- `tests/` — Unit tests for all modules
- `docs/` — Documentation for the project

---

## 📖 Documentation

Detailed documentation for each module is available in the `docs/` directory:

- [LLM Module](docs/LangOps/llm/README.md): Language model integrations.
- [Parser Module](docs/LangOps/parser/README.md): Log parsing and error extraction.
- [Alert Module](docs/LangOps/alert/README.md): Alerting mechanisms.
- [Prompt Module](docs/LangOps/prompt/README.md): Flexible prompt handling for LLMs.

---

## 🌟 Contributing

We welcome contributions to LangOps! Here's how you can get started:

1. **Fork the repository** and clone it locally.
2. **Create a new branch** for your feature or bug fix:

   ```sh
   git checkout -b feature/my-new-feature
   ```

3. **Make your changes** and ensure all tests pass:

   ```sh
   make test
   ```

4. **Submit a pull request** with a clear description of your changes.

### Contributor Guidelines

- Follow the [Code of Conduct](CODE_OF_CONDUCT.md).
- Write clear commit messages and document your code.
- Ensure your changes are covered by tests.

---

## 🔮 Future Features

LangOps is designed to expand its capabilities further. Planned features include:

- **LangOps.Agent:**
  - Intelligent agents for automated log analysis and decision-making.
  - Integration with CI/CD pipelines for proactive error detection.

- **LangOps.Tool:**
  - A suite of tools for log visualization and debugging.
  - Enhanced filtering and search capabilities for large datasets.

- **LangOps.Alert:**
  - Real-time alerting system for critical errors.
  - Configurable thresholds and notification channels.

These features aim to make LangOps a comprehensive solution for failure analysis and log management.

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

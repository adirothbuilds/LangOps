# LangOps – AI-Driven Automation for DevOps Logs

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=adirothbuilds_AgentOps&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=adirothbuilds_AgentOps) [![Coverage](https://sonarcloud.io/api/project_badges/measure?project=adirothbuilds_AgentOps&metric=coverage)](https://sonarcloud.io/summary/new_code?id=adirothbuilds_AgentOps) [![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=adirothbuilds_AgentOps&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=adirothbuilds_AgentOps) [![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=adirothbuilds_AgentOps&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=adirothbuilds_AgentOps) [![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![LangOps SDK](https://img.shields.io/badge/SDK-LangOps-green)](https://github.com/adirothbuilds/LangOps)

---

LangOps is a **modular SDK** for building intelligent, AI-enhanced DevOps tooling.  
It helps you **parse logs, extract errors, craft prompts, and interact with LLMs** — all in a clean, extensible architecture.

Whether you're debugging CI/CD failures or building auto-triage agents, LangOps gives you the building blocks to automate it *your way*.

---

## ✨ Features

- 🔌 **Plug-and-Play Parsers** – Define, register, and reuse parsers with one decorator.
- 🧠 **LLM Integration** – Sync + Async support for OpenAI GPT, extensible to other providers.
- 🗃 **Prompt Engineering Toolkit** – Prompt classes with context injection and structure.
- 🪵 **Log Utilities** – Tools for filtering, trimming, and extracting relevant log sections.
- 🧪 **Full Test Coverage** – Unit-tested design with `pytest`, `coverage`, and linting.
- 🧱 **Clean Abstractions** – Every layer is modular and extensible.

---

## ⚡ Quick Start

```bash
git clone https://github.com/adirothbuilds/LangOps.git
cd LangOps
make install-dev
make test
```

💡 Want to publish or build locally?

```bash
make build   # Build the SDK
make publish # Publish to PyPI
```

---

## 📦 Project Structure

```
langops/
├── parser/   # Log parsers and error extractors
├── llm/      # Model integrations (OpenAI, etc.)
├── prompt/   # Prompt handling and injection
├── alert/    # Alert system hooks (future)
├── core/     # Shared logic and utilities
tests/        # Unit tests for every module
docs/         # Markdown docs per module
demo/         # Examples and data
```

---

## 📚 Module Documentation

Each module has a dedicated README:

- [`parser/`](docs/agentops/parser/README.md): Log filtering, extraction, and categorization
- [`llm/`](docs/agentops/llm/README.md): GPT-powered inference with sync/async support
- [`prompt/`](docs/agentops/prompt/README.md): Prompt building and formatting utilities
- [`alert/`](docs/agentops/alert/README.md): Alert templates and future notification features

---

## 🤝 Contributing

LangOps is open-source and community-first.  
If you're passionate about DevOps, LLMs, or smart automation — we’d love your help.

Start here:

```bash
git checkout -b feature/my-contribution
```

Then:

- Follow the [Code of Conduct](CODE_OF_CONDUCT.md)
- Write meaningful commit messages
- Cover your code with tests
- Open a PR when ready 🙌

Community contact:
- 📬 Email: [adi.build.balance@gmail.com](mailto:adi.build.balance@gmail.com)
- 🧵 Discussions: [GitHub Discussions](https://github.com/adirothbuilds/LangOps/discussions/10)
- 🐞 Issues: [Issue Tracker](https://github.com/adirothbuilds/LangOps/issues)

---

## 🔮 Coming Soon

LangOps is evolving rapidly. Upcoming additions:

- `LangOps.Agent` – Autonomous agents that can analyze and respond to pipeline failures.
- `LangOps.Tool` – Standalone CLI tools for log triage and visualization.
- `LangOps.Alert` – Real-time error alerts via custom channels (email, Slack, etc.)

---

## 📄 License

MIT — use it freely, improve it openly, and build responsibly.  
See [`LICENSE`](LICENSE) for details.
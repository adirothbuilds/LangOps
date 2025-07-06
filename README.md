# LangOps – Modular AI SDK for DevOps Log Intelligence

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=adirothbuilds_AgentOps&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=adirothbuilds_AgentOps) [![Coverage](https://sonarcloud.io/api/project_badges/measure?project=adirothbuilds_AgentOps&metric=coverage)](https://sonarcloud.io/summary/new_code?id=adirothbuilds_AgentOps) [![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=adirothbuilds_AgentOps&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=adirothbuilds_AgentOps) [![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=adirothbuilds_AgentOps&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=adirothbuilds_AgentOps) [![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![LangOps SDK](https://img.shields.io/badge/SDK-LangOps-green)](https://github.com/adirothbuilds/LangOps)

---

LangOps is a **modular SDK** designed for DevOps and SRE professionals for building intelligent log-analysis pipelines and AI-powered DevOps agents. It is open-source and community-driven, making it easy to contribute and extend.

## Why LangOps?

As a DevOps engineer, you often face challenges like debugging CI/CD failures, analyzing massive logs, and crafting effective prompts for language models. LangOps streamlines this process through:

- **Plug-and-Play Architecture**: Easily integrate parsers, LLMs, and prompt builders into your workflows.
- **AI-Powered Insights**: Use GPT models to analyze logs and explain failure causes.
- **Extensibility**: Register custom modules to tailor the SDK to your needs.

Whether you're building auto-triage agents or streamlining log analysis, LangOps empowers you to automate smarter.

---

## ✨ Features

- 🔍 Extract meaningful errors from massive CI logs with a single parser.
- 🤖 Analyze logs with GPT-powered language models and explain failure causes.
- 🧰 Register your own parsers and prompt builders in a plug-and-play way.
- 🧪 Run comprehensive unit tests with full `pytest` + `coverage` integration.

---

## ⚡ Quick Start

Install LangOps directly from PyPI:

```bash
pip install langops
# Optional: install [dev] extras if contributing
```

Then import and start using it:

```python
from langops.parser import ErrorParser 
from langops.prompt import JenkinsErrorPrompt
from langops.llm import OpenAILLM


# Example usage
parser = ErrorParser()
errors = parser.from_file("path/to/logfile.log")

prompter = JenkinsErrorPrompt(build_id="build_id", timestamp="timestamp")
prompt.add_user_prompt(errors)
messages = prompt.render_prompts()

client = OpenAILLM(api_key="your-openai-api-key")
response = client.complete(messages)
print("LLM response:\n")
print(response.text)
print("\nLLM metadata:\n")
print(response.metadata)
```

📚 For advanced usage examples, check the [`demo/`](demo) folder.

---

## 📦 Project Structure

```bash
langops/
├── parser/   # Log parsers and error extractors
├── llm/      # Model integrations (OpenAI, etc.)
├── prompt/   # Prompt handling and injection
├── alert/    # Alert system hooks (in progress)
├── core/     # Shared logic and utilities
tests/        # Unit tests for every module
docs/         # Markdown docs per module
demo/         # Examples and data
```

---

## 📚 Module Documentation

Each module has a dedicated README:

- [`core/`](docs/core/index.md): Foundational classes and utilities for AI-driven workflows
- [`parser/`](docs/langops/parser/index.md): Tools for parsing and filtering logs, including specialized parsers for Jenkins logs and error logs.
- [`llm/`](docs/langops/llm/index.md): Async-ready GPT client with structured response interface
- [`prompt/`](docs/langops/prompt/index.md): Prompt building and formatting utilities
- [`alert/`](docs/langops/alert/index.md): Alert templates and future notification features

---

## 🤝 Contributing

LangOps is open-source and community-first.  
If you're passionate about DevOps, LLMs, or smart automation — we’d love your help.

Start here:

```bash
git clone https://github.com/adirothbuilds/LangOps.git
cd LangOps
git switch -c your-new-branch
make install-dev
```

Then:

- Follow the [Code of Conduct](CODE_OF_CONDUCT.md)
- Write meaningful commit messages
- Cover your code with tests
- Open a PR when ready 🙌

✨ Tip: Run `make lint && make test` before every PR to verify your changes.

Community contact:

- 📬 Email: [adi.build.balance@gmail.com](mailto:adi.build.balance@gmail.com)
- 🧵 Discussions: [GitHub Discussions](https://github.com/adirothbuilds/LangOps/discussions/10)
- 🐞 Issues: [Issue Tracker](https://github.com/adirothbuilds/LangOps/issues)

---

## 🔮 Coming Soon

LangOps is evolving rapidly. Upcoming additions:

- `LangOps.Agent` – Smart agents for pipeline triage, issue explanation, and auto-resolution.
- `LangOps.Tool` – CLI utilities for fast log inspection and AI-powered summaries.
- `LangOps.Alert` – Real-time error alerts via custom channels (email, Slack, etc.)

📌 Want to build your own plugin or agent? Open an idea in [GitHub Discussions](https://github.com/adirothbuilds/LangOps/discussions) and let’s talk!

---

## 📄 License

MIT — use it freely, improve it openly, and build responsibly.  
See [`LICENSE`](LICENSE) for details.

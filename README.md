# LangOps – Modular AI SDK for DevOps Log Intelligence

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=adirothbuilds_AgentOps&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=adirothbuilds_AgentOps) [![Coverage](https://sonarcloud.io/api/project_badges/measure?project=adirothbuilds_AgentOps&metric=coverage)](https://sonarcloud.io/summary/new_code?id=adirothbuilds_AgentOps) [![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=adirothbuilds_AgentOps&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=adirothbuilds_AgentOps) [![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=adirothbuilds_AgentOps&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=adirothbuilds_AgentOps) [![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Test Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen)](https://github.com/adirothbuilds/LangOps) [![LangOps SDK](https://img.shields.io/badge/SDK-LangOps-green)](https://github.com/adirothbuilds/LangOps)

---

LangOps is a **production-ready, modular SDK** designed for DevOps and SRE professionals for building intelligent log-analysis pipelines and AI-powered DevOps agents. With **100% test coverage** and a robust architecture, it's built for reliability and extensibility in enterprise environments.

## Why LangOps?

As a DevOps engineer, you often face challenges like debugging CI/CD failures, analyzing massive logs, and crafting effective prompts for language models. LangOps streamlines this process through:

- **🏗️ Production-Ready Architecture**: Built with 100% test coverage and enterprise-grade reliability
- **🔌 Plug-and-Play Components**: Registry-based system for easy integration of parsers, LLMs, and prompt builders
- **🤖 AI-Powered Insights**: Advanced GPT integration to analyze logs and explain failure causes
- **🎯 Comprehensive Log Parsing**: Support for Jenkins, GitHub Actions, GitLab CI, and custom pipeline formats
- **📊 Intelligent Pattern Matching**: Context-aware error extraction with severity classification
- **🔧 Extensible Design**: Register custom modules and patterns to tailor the SDK to your needs

Whether you're building auto-triage agents, streamlining log analysis, or creating intelligent DevOps workflows, LangOps empowers you to automate smarter with confidence.

---

## ✨ Features

- 🔍 **Advanced Log Parsing**: Extract meaningful errors from massive CI logs with intelligent pattern matching
- 🤖 **AI-Powered Analysis**: Analyze logs with GPT models and generate actionable insights
- 🧰 **Modular Architecture**: Registry-based plugin system for parsers, LLMs, and prompt builders
- 🎯 **Multi-Platform Support**: Built-in patterns for Jenkins, GitHub Actions, GitLab CI, and more
- 📊 **Context-Aware Extraction**: Smart metadata extraction with timestamp, severity, and stage detection
- 🧪 **100% Test Coverage**: Comprehensive test suite with 170+ tests ensuring reliability
- 🔧 **Type-Safe Design**: Full TypeScript-style annotations for better development experience
- 📈 **Performance Optimized**: Efficient parsing with configurable severity filtering and deduplication

---

## ⚡ Quick Start

Install LangOps directly from PyPI:

```bash
pip install langops
# Optional: install [dev] extras if contributing
```

### Basic Usage

```python
from langops.parser import ErrorParser, PipelineParser
from langops.prompt import JenkinsErrorPrompt
from langops.llm import OpenAILLM

# Parse errors from logs
parser = ErrorParser()
errors = parser.from_file("path/to/logfile.log")

# Advanced pipeline parsing with stage detection
pipeline_parser = PipelineParser(source="jenkins")
result = pipeline_parser.parse(log_content, 
                              min_severity="WARNING",
                              deduplicate=True)

# Generate AI-powered insights
prompter = JenkinsErrorPrompt(build_id="build_123", timestamp="2024-01-01T12:00:00Z")
prompter.add_user_prompt(errors)
messages = prompter.render_prompts()

# Get LLM analysis
client = OpenAILLM(api_key="your-openai-api-key")
response = client.complete(messages)
print("AI Analysis:")
print(response.text)
print("\nMetadata:")
print(response.metadata)
```

### Advanced Pipeline Parsing

```python
from langops.parser import PipelineParser
from langops.parser.types import SeverityLevel

# Create parser with custom configuration
parser = PipelineParser(source="github_actions")

# Parse with advanced options
result = parser.parse(
    log_content,
    min_severity=SeverityLevel.WARNING,
    deduplicate=True,
    extract_metadata=True
)

# Access structured results
print(f"Found {len(result.log_entries)} log entries")
print(f"Stages detected: {[stage.name for stage in result.stages]}")
print(f"Error summary: {result.summary}")
```

📚 For more advanced usage examples, check the [`demo/`](demo) folder.

---

## 📦 Project Structure

```bash
langops/
├── core/         # Foundation classes (BaseParser, BaseLLM, etc.)
├── parser/       # Log parsers and intelligent extractors
│   ├── utils/    # Pattern resolvers, extractors, stage cleaners
│   ├── patterns/ # CI/CD platform-specific patterns
│   └── types/    # Type definitions and data models
├── llm/          # LLM integrations (OpenAI, async support)
├── prompt/       # Prompt building and formatting utilities
├── alert/        # Alert system and notification hooks
└── __init__.py   # Clean SDK interface

tests/            # Comprehensive test suite (100% coverage)
├── langops/      # Mirror structure with full test coverage
│   ├── parser/   # 170+ tests covering all parsing logic
│   ├── llm/      # LLM integration tests
│   └── ...       # Complete test coverage

demo/             # Real-world examples and sample data
docs/             # Module documentation and guides
```

### 🏗️ Architecture Highlights

- **Registry-Based Design**: Plug-and-play component registration
- **Abstract Base Classes**: Consistent interfaces across all modules
- **Type-Safe Implementation**: Full type annotations for better DX
- **Comprehensive Error Handling**: Robust error management and logging
- **Performance Optimized**: Efficient parsing with configurable options

---

## 🧪 Quality & Testing

LangOps maintains **exceptional code quality** with comprehensive testing:

- **✅ 100% Test Coverage**: All 714 lines of source code are fully tested
- **🔬 170+ Test Cases**: Comprehensive test suite covering all scenarios
- **🎯 Edge Case Testing**: Thorough testing of error conditions and boundary cases
- **🚀 Continuous Integration**: Automated testing and quality checks
- **📊 Code Quality**: Clean, maintainable code with proper documentation

### Running Tests

```bash
# Run the full test suite
make test

# Generate coverage report
make coverage

# Run linting and type checking
make lint

# Run all quality checks
make lint && make test
```

### Coverage Details

| Module | Coverage | Lines | Tests |
|--------|----------|-------|-------|
| `core/` | 100% | 134 | 15+ |
| `parser/` | 100% | 365 | 80+ |
| `llm/` | 100% | 86 | 25+ |
| `prompt/` | 100% | 35 | 10+ |
| `alert/` | 100% | 37 | 7+ |
| **Total** | **100%** | **714** | **170+** |

---

---

## 📚 Module Documentation

### Core Parsers

LangOps provides several specialized parsers for different use cases:

#### 🔍 PipelineParser

Advanced parser for CI/CD pipeline logs with intelligent stage detection:

- **Multi-platform support**: Jenkins, GitHub Actions, GitLab CI
- **Stage detection**: Automatic pipeline stage identification and cleaning
- **Severity classification**: Context-aware error severity assessment
- **Metadata extraction**: Timestamps, build IDs, and contextual information
- **Configurable filtering**: Minimum severity levels and deduplication

#### 🚨 ErrorParser

Focused error extraction from any log format:

- **Pattern-based matching**: Efficient error line identification
- **Context extraction**: Surrounding log lines for better understanding
- **Structured output**: Clean, LLM-ready error summaries

#### 🔧 JenkinsParser

Specialized parser for Jenkins-specific log formats:

- **Build stage analysis**: Detailed Jenkins pipeline stage parsing
- **Plugin-aware**: Handles various Jenkins plugin output formats
- **Performance metrics**: Build timing and resource usage extraction

### Documentation Links

Each module has comprehensive documentation:

- [`core/`](docs/langops/core/index.md): Foundational classes and utilities for AI-driven workflows
- [`parser/`](docs/langops/parser/index.md): Advanced log parsing with intelligent pattern matching
- [`llm/`](docs/langops/llm/index.md): Async-ready LLM integrations with structured responses
- [`prompt/`](docs/langops/prompt/index.md): Prompt building and formatting utilities
- [`alert/`](docs/langops/alert/index.md): Alert templates and notification system

---

## 📖 Documentation

LangOps comes with comprehensive documentation including API references, tutorials, and examples.

### 🐳 Docker Documentation

The easiest way to access the documentation is through Docker:

```bash
# Build the documentation container
docker build -f Dockerfile.langops.docs -t langops-docs .

# Run the documentation server
docker run -p 8000:8000 langops-docs

# Open your browser to http://localhost:8000/langops/
```

This will start a MkDocs server with the complete documentation, including:

- API reference with auto-generated docs
- Getting started guides
- Usage examples
- Advanced configuration

### 📝 Local Documentation

For local development, you can also run the documentation directly:

```bash
# Install documentation dependencies
pip install -r requirements.docs.txt

# Serve the documentation locally
mkdocs serve

# Open your browser to http://localhost:8000/
```

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

# LangOps – Modular AI SDK for DevOps Log Intelligence

<div class="hero">
  <h1>🚀 LangOps</h1>
  <p>Production-ready AI SDK for DevOps Log Intelligence</p>
  <div class="hero-buttons">
    <a href="getting-started/installation/" class="hero-button">Get Started</a>
    <a href="getting-started/quick-start/" class="hero-button">Quick Start</a>
    <a href="https://github.com/adirothbuilds/langops" class="hero-button">GitHub</a>
  </div>
</div>

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=adirothbuilds_AgentOps&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=adirothbuilds_AgentOps) [![Coverage](https://sonarcloud.io/api/project_badges/measure?project=adirothbuilds_AgentOps&metric=coverage)](https://sonarcloud.io/summary/new_code?id=adirothbuilds_AgentOps) [![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=adirothbuilds_AgentOps&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=adirothbuilds_AgentOps) [![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=adirothbuilds_AgentOps&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=adirothbuilds_AgentOps) [![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Test Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen)](https://github.com/adirothbuilds/LangOps) [![LangOps SDK](https://img.shields.io/badge/SDK-LangOps-green)](https://github.com/adirothbuilds/LangOps)

LangOps is a **production-ready, modular SDK** designed for DevOps and SRE professionals for building intelligent log-analysis pipelines and AI-powered DevOps agents. With <span class="coverage-badge">100% test coverage</span> and a robust architecture, it's built for reliability and extensibility in enterprise environments.

## 🌟 Key Features

<div class="feature-grid">
  <div class="feature-card">
    <div class="feature-icon">🏗️</div>
    <div class="feature-title">Production-Ready</div>
    <div class="feature-description">Built with 100% test coverage and enterprise-grade reliability. Battle-tested architecture for mission-critical environments.</div>
  </div>
  
  <div class="feature-card">
    <div class="feature-icon">🔌</div>
    <div class="feature-title">Modular Design</div>
    <div class="feature-description">Registry-based system for easy integration of parsers, LLMs, and prompt builders. Extend with custom components.</div>
  </div>
  
  <div class="feature-card">
    <div class="feature-icon">🤖</div>
    <div class="feature-title">AI-Powered</div>
    <div class="feature-description">Advanced GPT integration to analyze logs, explain failure causes, and provide actionable insights.</div>
  </div>
  
  <div class="feature-card">
    <div class="feature-icon">📊</div>
    <div class="feature-title">Comprehensive Parsing</div>
    <div class="feature-description">Support for Jenkins, GitHub Actions, GitLab CI, Azure DevOps, and custom pipeline formats.</div>
  </div>
  
  <div class="feature-card">
    <div class="feature-icon">🎯</div>
    <div class="feature-title">Smart Pattern Matching</div>
    <div class="feature-description">Context-aware error extraction with severity classification and stage-level analysis.</div>
  </div>
  
  <div class="feature-card">
    <div class="feature-icon">🔧</div>
    <div class="feature-title">Extensible</div>
    <div class="feature-description">Register custom modules and patterns to tailor the SDK to your specific needs and workflows.</div>
  </div>
</div>

## 🚀 Why LangOps?

As a DevOps engineer, you often face challenges like:

- **Debugging CI/CD failures** across multiple platforms
- **Analyzing massive log volumes** manually
- **Crafting effective prompts** for language models
- **Building reliable automation** for log analysis

LangOps streamlines this process through intelligent automation and AI-powered insights, empowering you to automate smarter with confidence.

## ⚡ Quick Start

Install LangOps directly from PyPI:

```bash
pip install langops
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
llm = OpenAILLM(model="gpt-4")
analysis = llm.generate(messages)
print(analysis)
```

## 📋 Supported Platforms

| Platform | Parser | Patterns | Status |
|----------|---------|----------|--------|
| **Jenkins** | ✅ | ✅ | Full Support |
| **GitHub Actions** | ✅ | ✅ | Full Support |
| **GitLab CI** | ✅ | ✅ | Full Support |
| **Azure DevOps** | ✅ | ✅ | Full Support |
| **Custom Logs** | ✅ | ✅ | Extensible |

## 🏆 Quality Metrics

- **Test Coverage**: 100%
- **Tests**: 170+ comprehensive test cases
- **Architecture**: Modular, registry-based design
- **Type Safety**: Full type annotations
- **Documentation**: Comprehensive guides and API docs

## 📚 Documentation

- **[Getting Started](getting-started/installation/)** - Installation and setup
- **[Quick Start Guide](getting-started/quick-start/)** - Basic usage examples
- **[Core Modules](docs/langops/core/index.md)** - SDK architecture overview
- **[Parser Deep Dive](docs/langops/parser/index.md)** - Advanced parsing features
- **[API Reference](docs/langops/parser/index.md)** - Complete API documentation
- **[Contributing](contributing/development.md)** - Development guidelines

## 🔗 Example Use Cases

### 1. **Auto-Triage CI/CD Failures**
```python
# Parse build logs and classify errors
parser = PipelineParser(source="jenkins")
result = parser.parse(build_log)

# Generate AI analysis
prompter = JenkinsErrorPrompt(build_id=build_id)
prompter.add_user_prompt(result.errors)
analysis = llm.generate(prompter.render_prompts())
```

### 2. **Smart Log Analysis**
```python
# Extract and categorize errors
parser = ErrorParser()
errors = parser.from_file("application.log")

# Filter by severity
critical_errors = [e for e in errors if e.severity == "CRITICAL"]
```

### 3. **Intelligent DevOps Workflows**
```python
# Build comprehensive analysis pipeline
pipeline_parser = PipelineParser(source="github")
result = pipeline_parser.parse(log_content, extract_stages=True)

# Analyze each stage
for stage in result.stages:
    if stage.has_errors():
        stage_analysis = analyze_stage_errors(stage)
```

## 🤝 Community & Support

- **GitHub**: [adirothbuilds/langops](https://github.com/adirothbuilds/langops)
- **Issues**: [Report bugs or request features](https://github.com/adirothbuilds/langops/issues)
- **Discussions**: [Community discussions](https://github.com/adirothbuilds/langops/discussions)
- **PyPI**: [langops package](https://pypi.org/project/langops/)

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Ready to supercharge your DevOps workflows with AI?** [Get started now](getting-started/installation/) or explore the [documentation](docs/langops/core/index.md) to learn more!
client = OpenAILLM(api_key="your-openai-api-key")
response = client.complete(messages)
print("AI Analysis:")
print(response.text)
```

## Features

- 🔍 **Advanced Log Parsing**: Extract meaningful errors from massive CI logs with intelligent pattern matching
- 🤖 **AI-Powered Analysis**: Analyze logs with GPT models and generate actionable insights
- 🧰 **Modular Architecture**: Registry-based plugin system for parsers, LLMs, and prompt builders
- 🎯 **Multi-Platform Support**: Built-in patterns for Jenkins, GitHub Actions, GitLab CI, and more
- 📊 **Context-Aware Extraction**: Smart metadata extraction with timestamp, severity, and stage detection
- 🧪 **100% Test Coverage**: Comprehensive test suite with 170+ tests ensuring reliability
- 🔧 **Type-Safe Design**: Full TypeScript-style annotations for better development experience
- 📈 **Performance Optimized**: Efficient parsing with configurable severity filtering and deduplication

## Documentation

Explore the comprehensive documentation:

- [Core Modules](docs/langops/core/index.md) - Foundational classes and utilities
- [Parser System](docs/langops/parser/index.md) - Advanced log parsing with intelligent pattern matching
- [LLM Integration](docs/langops/llm/index.md) - AI-powered log analysis
- [Prompt Building](docs/langops/prompt/index.md) - Prompt templates and formatting
- [Alert System](docs/langops/alert/index.md) - Notification and alert management

## Contributing

LangOps is open-source and community-first. We welcome contributions from developers passionate about DevOps, AI, and automation.

## License

MIT License - see [LICENSE](https://github.com/adirothbuilds/langops/blob/main/LICENSE) for details.

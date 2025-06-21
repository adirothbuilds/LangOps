# AgentOps

AgentOps is an AI-powered failure analysis agent for CI/CD pipelines. It provides a framework for parsing, filtering, and analyzing logs, with extensible parser registration and error extraction capabilities.

## Features

- Abstract base parser class for log and data parsing
- Error log extraction and filtering
- Parser registry for easy extension
- Utilities for file handling and log filtering
- 100% test coverage with pytest

## Quick Start

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

## Project Structure

- `agentops/` — Core library modules
- `tests/` — Unit tests
- `docs/` — Documentation

## License

MIT

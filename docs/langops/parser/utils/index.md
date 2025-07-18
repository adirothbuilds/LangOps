# Parser Utils

## Overview

The `langops.parser.utils` module provides essential utility functions for processing pipeline logs, including timestamp extraction, context identification, pattern resolution, and stage name cleaning.

## Modules

### [extractors.py](extractors.md)

Utilities for extracting timestamps, context IDs, and metadata from log entries.

### [resolver.py](resolver.md)

Pattern resolution utilities for loading and resolving platform-specific patterns.

### [stage_cleaner.py](stage_cleaner.md)

Stage name cleaning utilities for different CI/CD platforms.

## Key Features

- **Timestamp Extraction**: Multi-format timestamp parsing and normalization
- **Context ID Extraction**: Intelligent identification of trace IDs, job IDs, and error contexts
- **Pattern Resolution**: Dynamic loading of platform-specific patterns
- **Stage Name Cleaning**: Platform-aware stage name sanitization
- **Metadata Extraction**: Comprehensive metadata parsing from log data

## Usage

```python
from langops.parser.utils.extractors import extract_timestamp, extract_context_id, extract_metadata
from langops.parser.utils.resolver import PatternResolver
from langops.parser.utils.stage_cleaner import STAGE_NAME_CLEANERS

# Extract timestamp from log line
timestamp = extract_timestamp("2024-01-01T12:00:00Z [INFO] Starting build")

# Extract context ID from log lines
context_id = extract_context_id(log_lines, line_number=10)

# Resolve patterns for a platform
resolver = PatternResolver()
patterns = resolver.resolve_patterns(jenkins_patterns_dict)

# Clean stage name
cleaner = STAGE_NAME_CLEANERS["jenkins"]
clean_name = cleaner("Stage: Build and Test [stable]")
```

## Architecture

The utils module follows a functional design pattern with:

- **Pure Functions**: Most utilities are stateless and predictable
- **Type Safety**: Full type annotations for better development experience
- **Extensibility**: Easy to add new extractors and cleaners
- **Performance**: Optimized regex patterns and efficient algorithms

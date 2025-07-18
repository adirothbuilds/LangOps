# Parser Module Documentation

## Overview

The `parser` module provides comprehensive tools for parsing and analyzing CI/CD pipeline logs, including specialized parsers for different platforms, intelligent pattern matching, and structured data extraction.

## Core Parsers

- [ErrorParser](error_parser.md): Filters and returns only error logs with context
- [JenkinsParser](jenkins_parser.md): Filters Jenkins logs by severity level
- [PipelineParser](pipeline_parser.md): Advanced parser for CI/CD pipeline logs with stage detection
- [ParserRegistry](registry.md): Registry for managing parser classes

## Parser Utilities

- [Utils](utils/index.md): Essential utilities for log processing
  - [Extractors](utils/extractors.md): Timestamp, context ID, and metadata extraction
  - [Resolver](utils/resolver.md): Pattern resolution and loading utilities
  - [Stage Cleaner](utils/stage_cleaner.md): Platform-aware stage name cleaning

## Pattern Matching

- [Patterns](patterns/index.md): Comprehensive pattern matching system
  - [Common Patterns](patterns/common.md): Shared patterns across languages and platforms
  - [Jenkins Patterns](patterns/jenkins.md): Jenkins-specific error patterns and stage detection
  - [GitHub Actions Patterns](patterns/github_actions.md): GitHub Actions workflow patterns
  - [GitLab CI Patterns](patterns/gitlab_ci.md): GitLab CI pipeline patterns
  - [Azure DevOps Patterns](patterns/azure_devops.md): Azure DevOps pipeline patterns

## Type Definitions

- [Types](types/pipeline_types.md): Core data structures and type definitions
- [Constants](constants/pipeline_constants.md): Essential constants and severity ordering

## Legacy Patterns

- [Jenkins Patterns](jenkins_patterns.md): Legacy regex patterns for Jenkins (deprecated)

---

## Architecture

The parser module is built with a modular architecture:

- **Registry-Based Design**: Plug-and-play parser registration
- **Pattern Resolution**: Dynamic loading of platform-specific patterns
- **Type-Safe Operations**: Full type annotations and validation
- **Performance Optimized**: Efficient parsing with configurable options

## Usage

Refer to the individual documentation files linked above for detailed API information and usage examples.

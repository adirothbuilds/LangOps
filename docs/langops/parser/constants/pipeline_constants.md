# Pipeline Constants

## Overview

The `pipeline_constants.py` module defines essential constants used throughout the LangOps pipeline parsing system. These constants provide standardized values for severity levels, ordering, and other pipeline-related configurations.

## Constants

### `SEVERITY_ORDER`

A list defining the hierarchical order of severity levels from lowest to highest priority.

```python
SEVERITY_ORDER = [
    SeverityLevel.INFO,
    SeverityLevel.WARNING,
    SeverityLevel.ERROR,
    SeverityLevel.CRITICAL,
]
```

**Purpose:**

- Provides a consistent ordering for severity levels
- Used for filtering logs by minimum severity
- Enables severity-based sorting and comparison operations

**Usage:**

```python
from langops.parser.constants.pipeline_constants import SEVERITY_ORDER
from langops.parser.types.pipeline_types import SeverityLevel

# Check if a severity level meets minimum requirements
def meets_minimum_severity(severity: SeverityLevel, minimum: SeverityLevel) -> bool:
    """Check if severity meets minimum threshold."""
    return SEVERITY_ORDER.index(severity) >= SEVERITY_ORDER.index(minimum)

# Usage
severity = SeverityLevel.ERROR
minimum = SeverityLevel.WARNING
if meets_minimum_severity(severity, minimum):
    print("Severity meets minimum threshold")
```

## Usage Examples

### Severity Filtering

```python
from langops.parser.constants.pipeline_constants import SEVERITY_ORDER
from langops.parser.types.pipeline_types import LogEntry, SeverityLevel

def filter_logs_by_severity(logs: List[LogEntry], min_severity: SeverityLevel) -> List[LogEntry]:
    """Filter logs by minimum severity level."""
    min_index = SEVERITY_ORDER.index(min_severity)
    
    return [
        log for log in logs
        if SEVERITY_ORDER.index(log.severity) >= min_index
    ]

# Filter to show only errors and critical issues
logs = [...]  # List of LogEntry objects
filtered = filter_logs_by_severity(logs, SeverityLevel.ERROR)
```

### Severity Comparison

```python
from langops.parser.constants.pipeline_constants import SEVERITY_ORDER
from langops.parser.types.pipeline_types import SeverityLevel

def compare_severities(severity1: SeverityLevel, severity2: SeverityLevel) -> int:
    """Compare two severity levels. Returns -1, 0, or 1."""
    index1 = SEVERITY_ORDER.index(severity1)
    index2 = SEVERITY_ORDER.index(severity2)
    
    if index1 < index2:
        return -1
    elif index1 > index2:
        return 1
    else:
        return 0

# Compare severities
result = compare_severities(SeverityLevel.ERROR, SeverityLevel.WARNING)
print(result)  # 1 (ERROR is higher than WARNING)
```

### Severity Statistics

```python
from langops.parser.constants.pipeline_constants import SEVERITY_ORDER
from langops.parser.types.pipeline_types import LogEntry, SeverityLevel

def get_severity_statistics(logs: List[LogEntry]) -> Dict[str, int]:
    """Get statistics for each severity level."""
    stats = {level.value: 0 for level in SEVERITY_ORDER}
    
    for log in logs:
        stats[log.severity.value] += 1
    
    return stats

# Get statistics
logs = [...]  # List of LogEntry objects
stats = get_severity_statistics(logs)
print(stats)  # {'info': 10, 'warning': 5, 'error': 2, 'critical': 1}
```

## Integration with Parsers

### Pipeline Parser Usage

```python
from langops.parser.constants.pipeline_constants import SEVERITY_ORDER
from langops.parser.types.pipeline_types import SeverityLevel

class PipelineParser:
    def __init__(self, min_severity: SeverityLevel = SeverityLevel.INFO):
        self.min_severity = min_severity
        self.min_severity_index = SEVERITY_ORDER.index(min_severity)
    
    def should_include_log(self, log_severity: SeverityLevel) -> bool:
        """Check if log should be included based on severity."""
        return SEVERITY_ORDER.index(log_severity) >= self.min_severity_index
    
    def parse(self, data: str) -> List[LogEntry]:
        """Parse logs and filter by severity."""
        all_logs = self._parse_all_logs(data)
        return [log for log in all_logs if self.should_include_log(log.severity)]
```

### Severity-Based Routing

```python
from langops.parser.constants.pipeline_constants import SEVERITY_ORDER
from langops.parser.types.pipeline_types import SeverityLevel

def route_by_severity(log_entry: LogEntry) -> str:
    """Route log entries based on severity level."""
    severity_index = SEVERITY_ORDER.index(log_entry.severity)
    
    if severity_index <= 1:  # INFO and WARNING
        return "info_channel"
    elif severity_index == 2:  # ERROR
        return "error_channel"
    else:  # CRITICAL
        return "critical_channel"

# Route logs
log = LogEntry(severity=SeverityLevel.ERROR, ...)
channel = route_by_severity(log)
print(channel)  # "error_channel"
```

## Configuration Management

### Custom Severity Orders

```python
from langops.parser.constants.pipeline_constants import SEVERITY_ORDER
from langops.parser.types.pipeline_types import SeverityLevel

# Create custom severity order for specific use cases
CUSTOM_SEVERITY_ORDER = [
    SeverityLevel.CRITICAL,  # Highest priority first
    SeverityLevel.ERROR,
    SeverityLevel.WARNING,
    SeverityLevel.INFO,
]

def get_priority_score(severity: SeverityLevel, order: List[SeverityLevel] = SEVERITY_ORDER) -> int:
    """Get priority score for a severity level."""
    return order.index(severity)

# Use custom order
score = get_priority_score(SeverityLevel.CRITICAL, CUSTOM_SEVERITY_ORDER)
print(score)  # 0 (highest priority)
```

### Severity Thresholds

```python
from langops.parser.constants.pipeline_constants import SEVERITY_ORDER
from langops.parser.types.pipeline_types import SeverityLevel

class SeverityThreshold:
    """Utility class for severity threshold management."""
    
    def __init__(self, threshold: SeverityLevel):
        self.threshold = threshold
        self.threshold_index = SEVERITY_ORDER.index(threshold)
    
    def is_above_threshold(self, severity: SeverityLevel) -> bool:
        """Check if severity is above threshold."""
        return SEVERITY_ORDER.index(severity) >= self.threshold_index
    
    def get_above_threshold(self, logs: List[LogEntry]) -> List[LogEntry]:
        """Get logs above threshold."""
        return [log for log in logs if self.is_above_threshold(log.severity)]

# Use threshold
threshold = SeverityThreshold(SeverityLevel.WARNING)
important_logs = threshold.get_above_threshold(all_logs)
```

## Validation and Utilities

### Severity Validation

```python
from langops.parser.constants.pipeline_constants import SEVERITY_ORDER
from langops.parser.types.pipeline_types import SeverityLevel

def validate_severity(severity: SeverityLevel) -> bool:
    """Validate that severity is a known level."""
    return severity in SEVERITY_ORDER

def validate_severity_order(order: List[SeverityLevel]) -> bool:
    """Validate that a severity order contains all required levels."""
    return set(order) == set(SEVERITY_ORDER)

# Validate severity
is_valid = validate_severity(SeverityLevel.ERROR)
print(is_valid)  # True
```

### Severity Utilities

```python
from langops.parser.constants.pipeline_constants import SEVERITY_ORDER
from langops.parser.types.pipeline_types import SeverityLevel

def get_max_severity(severities: List[SeverityLevel]) -> SeverityLevel:
    """Get the maximum severity from a list."""
    if not severities:
        return SeverityLevel.INFO
    
    return max(severities, key=lambda s: SEVERITY_ORDER.index(s))

def get_min_severity(severities: List[SeverityLevel]) -> SeverityLevel:
    """Get the minimum severity from a list."""
    if not severities:
        return SeverityLevel.INFO
    
    return min(severities, key=lambda s: SEVERITY_ORDER.index(s))

# Get max severity
severities = [SeverityLevel.INFO, SeverityLevel.ERROR, SeverityLevel.WARNING]
max_severity = get_max_severity(severities)
print(max_severity)  # SeverityLevel.ERROR
```

## Performance Considerations

### Index Caching

```python
from langops.parser.constants.pipeline_constants import SEVERITY_ORDER
from langops.parser.types.pipeline_types import SeverityLevel

class SeverityIndexCache:
    """Cache for severity indices to improve performance."""
    
    def __init__(self):
        self._cache = {level: i for i, level in enumerate(SEVERITY_ORDER)}
    
    def get_index(self, severity: SeverityLevel) -> int:
        """Get cached index for severity."""
        return self._cache[severity]
    
    def compare(self, severity1: SeverityLevel, severity2: SeverityLevel) -> int:
        """Compare severities using cached indices."""
        index1 = self.get_index(severity1)
        index2 = self.get_index(severity2)
        return index1 - index2

# Use cache for better performance
cache = SeverityIndexCache()
comparison = cache.compare(SeverityLevel.ERROR, SeverityLevel.WARNING)
```

### Batch Operations

```python
from langops.parser.constants.pipeline_constants import SEVERITY_ORDER
from langops.parser.types.pipeline_types import LogEntry, SeverityLevel

def batch_filter_by_severity(logs: List[LogEntry], min_severity: SeverityLevel) -> List[LogEntry]:
    """Efficiently filter large batches of logs."""
    min_index = SEVERITY_ORDER.index(min_severity)
    
    # Pre-compute indices for better performance
    severity_indices = {log.severity: SEVERITY_ORDER.index(log.severity) for log in logs}
    
    return [
        log for log in logs
        if severity_indices[log.severity] >= min_index
    ]
```

## Extension Points

### Custom Constants

```python
from langops.parser.constants.pipeline_constants import SEVERITY_ORDER
from langops.parser.types.pipeline_types import SeverityLevel

# Add custom constants for specific use cases
ALERT_THRESHOLD = SeverityLevel.ERROR
NOTIFICATION_THRESHOLD = SeverityLevel.WARNING
LOGGING_THRESHOLD = SeverityLevel.INFO

# Custom severity groups
LOW_PRIORITY = [SeverityLevel.INFO, SeverityLevel.WARNING]
HIGH_PRIORITY = [SeverityLevel.ERROR, SeverityLevel.CRITICAL]

def is_high_priority(severity: SeverityLevel) -> bool:
    """Check if severity is high priority."""
    return severity in HIGH_PRIORITY
```

### Dynamic Configuration

```python
from langops.parser.constants.pipeline_constants import SEVERITY_ORDER
from langops.parser.types.pipeline_types import SeverityLevel

class DynamicSeverityConfig:
    """Dynamic configuration for severity handling."""
    
    def __init__(self, config: Dict[str, Any]):
        self.thresholds = {
            'alert': SeverityLevel(config.get('alert_threshold', 'error')),
            'notification': SeverityLevel(config.get('notification_threshold', 'warning')),
            'logging': SeverityLevel(config.get('logging_threshold', 'info'))
        }
    
    def should_alert(self, severity: SeverityLevel) -> bool:
        """Check if severity should trigger alert."""
        return SEVERITY_ORDER.index(severity) >= SEVERITY_ORDER.index(self.thresholds['alert'])
```

## Testing

The pipeline constants module is thoroughly tested with:

- **Constant Validation**: Tests for constant values and types
- **Ordering**: Tests for severity ordering and comparisons
- **Integration**: Tests with parsers and other components
- **Performance**: Tests for efficient constant usage

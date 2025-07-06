# Constants

## Overview

`constants.py` defines shared constants used across the LangOps SDK.

## API Documentation

### Attributes

#### `SEVERITY_ORDER`

**Description**: Ordered list of severity levels.

**Type**: `List[SeverityLevel]`

**Values**:

- [`SeverityLevel.INFO`](types.md#severitylevel)
- [`SeverityLevel.WARNING`](types.md#severitylevel)
- [`SeverityLevel.ERROR`](types.md#severitylevel)
- [`SeverityLevel.CRITICAL`](types.md#severitylevel)

---

## Usage

Use `SEVERITY_ORDER` to prioritize or filter logs based on severity.

```python
from langops.core.constants import SEVERITY_ORDER

for level in SEVERITY_ORDER:
    print(level)
```

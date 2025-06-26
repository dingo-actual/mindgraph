# Python Style Quick Reference

## Full Guide

- The full Python style guide is available in claude_handbook/reference/style_guide.md
- **ALWAYS** refer to the full guide for specific rules and exceptions.

## Formatting

- **Line length:** 88 chars max
- **Indentation:** 4 spaces (never tabs)
- **Blank lines:** 2 between module-level items, 1 between methods

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Modules/Variables/Functions | lowercase_underscore | `data_processor`, `process_data()` |
| Classes | CapWords | `DataProcessor` |
| Constants | UPPERCASE_UNDERSCORE | `MAX_SIZE` |
| Protected | `_leading_underscore` | `_internal` |
| Type Variables | CapWords | `T`, `Vector` |

## Imports

```python
# Order: stdlib → third-party → local
import os

import numpy as np

from myproject.core import Engine
```

## Type Annotations

```python
def process(data: List[float], normalize: bool = True) -> float:
    ...
```

## Strings

- Default: double quotes `"string"`
- F-strings preferred: `f"{name} scored {score:.1f}"`
- Docstrings: triple double quotes `"""`

## Key Rules

- **No walrus operator** `:=`
- **No mutable defaults:** Use `None` then check
- **Explicit returns:** Return `None` explicitly
- **Spaces:** Around operators, after commas, none in brackets
- **Comprehensions:** Multi-line for complex cases
- **Exceptions:** Catch specific types, not bare except

## File Structure

```python
#!/usr/bin/env python3
"""Module docstring."""
# Imports (sorted by group)
# Constants
# Classes/Functions
if __name__ == "__main__":
    main()
```
# Python Style Guide

## 1. General Formatting

### Line Length
- Maximum line length: 88 characters (following Black's default, more practical than 79)
- Exceptions:
  - Long URLs in comments
  - Long string literals with no natural break points
  - Import statements that would be less readable when split

### Indentation
- Use 4 spaces per indentation level
- Never use tabs
- Continuation lines should align wrapped elements:
  ```python
  # Aligned with opening delimiter
  result = some_function(argument_one, argument_two,
                        argument_three, argument_four)
  
  # Hanging indent (add 4 spaces)
  result = some_function(
      argument_one, argument_two,
      argument_three, argument_four
  )
  ```

### Blank Lines
- Two blank lines between module-level functions and classes
- One blank line between methods within a class
- One blank line between logical sections within functions (sparingly)
- No blank line after function/class definition before docstring

## 2. Imports

### Organization
```python
# Standard library imports
import os
import sys
from collections import defaultdict
from typing import Optional, List, Dict

# Related third-party imports
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Local application/library imports
from myproject.core import Engine
from myproject.utils import helper_function
```

### Import Rules

- One import per line for `import` statements
- Multiple imports allowed for `from` imports: `from typing import Dict, List, Optional`
- Use absolute imports for packages
- Avoid wildcard imports (`from module import *`)
- Sort imports alphabetically within each group
- Place all imports at the top of the file after module docstring

## 3. Naming Conventions

### Basic Rules
| Type | Convention | Example |
|------|------------|---------|
| Modules | lowercase_with_underscores | `data_processor.py` |
| Classes | CapWords | `DataProcessor` |
| Functions | lowercase_with_underscores | `process_data()` |
| Variables | lowercase_with_underscores | `processed_data` |
| Constants | UPPERCASE_WITH_UNDERSCORES | `MAX_BUFFER_SIZE` |
| Type Variables | CapWords (usually single letter) | `T`, `KT`, `VT` |

### Specific Guidelines

- Protected members: single leading underscore `_internal_method()`
- Private members: double leading underscore `__private_method()`
- Avoid single character names except for:
  - Exceptions: `e`
  - Mathematical conventions: `x`, `y`, `n`
- Never use `l`, `O`, or `I` as single character names
- When overlapping built-in names, use a trailing underscore: `class_`

- Counters and iterates should have a short name describing what they count or iterate:

```python
for ix, item in enumerate(items):
    print(f"Item {ix}: {item}")
```

- File pointers should be named `fp`:

```python
with open("data.csv", "r") as fp:
    for line in fp:
        ...
```

## 4. Type Annotations

### Function Annotations

```python
def calculate_mean(values: List[float]) -> float:
    """Calculate arithmetic mean of values."""
    return sum(values) / len(values)

def process_data(
    data: pd.DataFrame,
    columns: Optional[List[str]] = None,
    normalize: bool = True
) -> pd.DataFrame:
    """Process dataframe with optional normalization."""
    ...
```

### Variable Annotations

```python
# When type isn't obvious from assignment
items: List[int] = []
mapping: Dict[str, Any] = {}

# For complex types
ProcessedResult = Tuple[pd.DataFrame, Dict[str, float]]
results: ProcessedResult = process_complex_data()
```

### Type Alias Convention

```python
# Use CapWords for type aliases
Vector = List[float]
Matrix = List[List[float]]
PathLike = Union[str, Path]
```

## 5. String Formatting

### String Quotes

- Use double quotes `"` for strings by default
- Use single quotes `'` when string contains double quotes
- Use triple double quotes `"""` for docstrings
- Use triple quotes for multi-line strings

### F-strings (Preferred)

```python
name = "Alice"
score = 95.5
message = f"{name} scored {score:.1f}%"
```

### Format Method (When f-strings aren't available)

```python
template = "{name} scored {score:.1f}%"
message = template.format(name="Alice", score=95.5)
```

## 6. Comments and Docstrings

### Inline Comments

```python
x = x + 1  # Increment x
```

- Use sparingly
- Separate from code by at least two spaces
- Start with `# ` (space after hash)

### Block Comments

```python
# This is a block comment that explains the following
# section of code. Each line starts with # and a space.
# 
# Additional paragraphs are separated by a line with just #.
```

### Docstrings

```python
#!/usr/bin/env python3
"""
A short description of the module, including its name.

More detailed description of the module, explaining its purpose,
functionality, usage, and contents.

    Important Classes:
        ImportantClass1(ParentClass): Description of the class.
        ImportantClass2(AnotherParentClass): Description of the class.
        ...

    Important Functions:
        important_function1(param1: type, param2: type) -> return_type: Description of the function.
        important_function2(param1: type, param2: type) -> return_type: Description of the function.
        ...

    Important Variables:
        important_variable1 (type): Description of the variable.
        important_variable2 (type): Description of the variable.
        ...
```

````python
class MyClass:
    """Short summary on one line.

    Longer description if needed. This section can span multiple
    lines and provides more detail about the class.

    Class Attributes:
        cls_attr1 (type): Description of cls_attr1.
        cls_attr2 (type): Description of cls_attr2.
        ...

    Instance Attributes:
        inst_attr1 (type): Description of inst_attr3.
        inst_attr2 (type): Description of inst_attr2.
        ...

    Example Usage:
        ```python
            >>> obj = MyClass()
            >>> obj.method1()
            ...
        ```
    """
````

```python
def complex_function(
    param1: int,
    param2: str,
    param3: Optional[float] = None
) -> Dict[str, Any]:
    """Short summary on one line.
    
    Longer description if needed. This section can span multiple
    lines and provides more detail about the function.
    
    Args:
        param1 (type): Description of param1.
        param2 (type): Description of param2.
        param3 (type): Description of param3. Defaults to None.
    
    Returns:
        (type) Description of return value.
    
    Raises:
        ValueError: Description of when this is raised.
        TypeError: Description of when this is raised.

    Example Usage:
        ```python
            >>> result = complex_function(1, "test", 3.14)
            >>> print(result)
            ...
        ```
    """
```

## 7. Whitespace

### Around Operators

```python
# Correct
x = 1
y = 2
result = x * y + 1

# Exception: Higher precedence operations
hypot = x*x + y*y
c = (a+b) * (a-b)
```

### Function Calls

```python
# No spaces around = for keyword arguments
function(x, y, z=3, name="test")

# Space after comma
items = [1, 2, 3, 4]
```

### Indexing/Slicing

```python
# No spaces inside brackets
array[index]
array[start:stop]
array[start:stop:step]
```

## 8. Class Formatting

```python
class DataProcessor:
    """Process data with configurable options."""
    
    DEFAULT_BATCH_SIZE: int = 32
    
    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize processor with configuration."""
        self.config = config
        self._cache: Dict[str, Any] = {}
    
    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        """Process input dataframe."""
        return self._apply_transforms(data)
    
    def _apply_transforms(self, data: pd.DataFrame) -> pd.DataFrame:
        """Apply configured transformations."""
        ...
```

## 9. Control Flow

### If Statements

```python
# Simple conditions
if condition:
    do_something()

# Multiple conditions (prefer parentheses over backslash)
if (condition_one and condition_two and
    condition_three and condition_four):
    do_something()

# Avoid single-line if statements
# Bad: if condition: do_something()
```

### List/Dict/Set Comprehensions

```python
# Simple comprehensions are fine on one line
squares = [x**2 for x in range(10)]

# Complex comprehensions should be multi-line
result = [
    transform(item)
    for item in sequence
    if condition(item)
]

# Very complex logic should use regular loops
```

## 10. Function Definitions

### Default Arguments

```python
# Good: Immutable defaults
def function(items: Optional[List[int]] = None) -> None:
    if items is None:
        items = []

# Bad: Mutable defaults
def function(items: List[int] = []) -> None:  # Don't do this
    ...
```

### Return Statements

```python
# Explicit None return for functions that don't return values
def modify_in_place(data: List[int]) -> None:
    data.sort()
    return None  # Explicit is better

# Consistent return points
def check_value(x: int) -> bool:
    if x < 0:
        return False
    if x > 100:
        return False
    return True
```

## 11. Exception Handling

```python
# Specific exception catching
try:
    value = dictionary[key]
except KeyError:
    value = default_value

# Multiple exceptions
try:
    process_data()
except (ValueError, TypeError) as e:
    logger.error(f"Processing failed: {e}")
    raise

# Cleanup with finally
try:
    f = open(filename)
    process_file(f)
finally:
    f.close()
```

## 12. Modern Python Features

### Walrus Operator (Python 3.8+)

- **DO NOT USE** the walrus operator.

### Match Statements (Python 3.10+)
```python
match command:
    case ["move", direction]:
        handle_move(direction)
    case ["attack", target]:
        handle_attack(target)
    case _:
        handle_unknown()
```

## 13. File Organization

### Module Structure
```python
#!/usr/bin/env python3
"""Module docstring.

Longer description of module functionality.
"""

# Future imports (if needed)
from __future__ import annotations

# Standard library imports
import os
import sys

# Third-party imports
import numpy as np

# Local imports
from mypackage import utilities

# Module-level constants
DEFAULT_TIMEOUT = 30
SUPPORTED_FORMATS = ["json", "csv", "parquet"]

# Module-level type definitions
ConfigDict = Dict[str, Any]

# Classes and functions
class MainClass:
    ...

# Main entry point
def main():
    ...

# Script execution
if __name__ == "__main__":
    main()
```

# References Guide

## Purpose

This guide provides practical steps for creating effective reference documentation following the Diátaxis framework. Reference material is technical description of the machinery and how to operate it. Reference documentation is always information-oriented. This document helps documentation writers craft references that provide authoritative, complete technical information users can trust while working.

## Prerequisites

- Understanding of the Diátaxis framework's four documentation types
- Technical knowledge of the system being documented
- Access to complete technical specifications
- Ability to describe without explaining or instructing

## Understanding Reference Fundamentals

### Step 1: Recognize What Makes Reference Documentation

Reference differs fundamentally from other documentation types. While tutorials teach, how-to guides solve problems, and explanations deepen understanding, reference documentation describes. It provides propositional knowledge—facts about what is, not instructions about what to do.

**Example: Reference vs How-to Documentation**
```markdown
# API Reference: User.create() (✓)
Creates a new user object in the database.

**Signature:** `User.create(data: UserData) -> User`

# How-to: Create a User Account (✗)
To create a new user account, follow these steps...
```

The reference states facts; the how-to provides instructions.

### Step 2: Embrace Neutral Description

Reference documentation demands austere neutrality. Resist every urge to explain why something works, justify design decisions, or provide usage recommendations. These belong in other documentation types. Focus solely on describing what exists and how it behaves.

**Example: Neutral vs Explanatory Description**
```python
# Poor: Explanatory
# This method uses SHA-256 because it provides 
# excellent security while maintaining performance...

# Better: Neutral
def hash_password(password: str) -> str:
    """
    Returns SHA-256 hash of the input string.
    
    Time complexity: O(n) where n is string length
    Space complexity: O(1)
    """
```

## Creating Reference Structure

### Step 3: Mirror Product Architecture

Structure reference documentation to match the system it describes. Users navigate both simultaneously—the documentation map should correspond to the territory of the code. This alignment reduces cognitive load and enables intuitive discovery.

**Example: Matching Documentation to Code Structure**
```markdown
# Documentation Structure
/reference
  /api
    /authentication
      /oauth.md
      /jwt.md
    /users
      /crud.md
      /permissions.md
  /cli
    /commands.md
    /options.md
```

### Step 4: Adopt Rigorous Patterns

Consistency enables quick consultation. Users learn your patterns once, then apply them everywhere. Establish templates for each reference type and enforce them ruthlessly. Predictability trumps creativity in reference documentation.

**Example: Consistent Function Documentation Pattern**
```markdown
## function_name()

**Signature**
`function_name(param1: Type1, param2: Type2 = default) -> ReturnType`

**Parameters**
- `param1` (Type1): Description of parameter
- `param2` (Type2, optional): Description. Default: `default`

**Returns**
- `ReturnType`: Description of return value

**Raises**
- `ErrorType`: Condition that triggers this error

**Complexity**
- Time: O(n log n)
- Space: O(n)

**Example**
```python
result = function_name("value", param2=42)
# Returns: ProcessedResult(...)
```
```

## Writing Reference Content

### Step 5: Document Everything Systematically

Reference documentation must be complete. Every parameter, return value, error condition, and edge case requires documentation. Users consult references when they need certainty—omissions break trust and force users to experiment or read source code.

**Example: Complete Parameter Documentation**
```markdown
**Parameters**
- `timeout` (float): Maximum seconds to wait for response.
  - Range: 0.001 to 300.0
  - Default: 30.0
  - Raises `ValueError` if negative
  - Raises `TimeoutError` if exceeded
  - Set to `None` for no timeout
  - Precision limited to milliseconds
```

### Step 6: State Facts Without Commentary

Write sentences that state facts about the machinery. Avoid subjective words like "simple," "powerful," or "convenient." Let users form their own judgments based on the facts you present.

**Example: Factual Statements**
```markdown
# Avoid Commentary (✗)
This powerful method easily transforms data...

# State Facts (✓)
Transforms input data according to the specified rules.

Available transformations:
- `uppercase`: Converts to uppercase (UTF-8 aware)
- `trim`: Removes leading/trailing whitespace
- `normalize`: Applies Unicode normalization form C
```

### Step 7: Include Minimal Examples

Examples in reference documentation illustrate facts, not teach concepts. Keep them brief—typically 1-3 lines—focusing on syntax and behavior rather than real-world applications. Complex examples belong in tutorials or how-to guides.

**Example: Reference Examples**
```python
# String.split() Examples
"a,b,c".split(",")      # Returns: ["a", "b", "c"]
"hello".split("")       # Raises: ValueError
"a b".split(maxsplit=1) # Returns: ["a", "b"]
```

## Ensuring Reference Quality

### Step 8: Verify Technical Accuracy

Reference documentation serves as the source of truth. A single inaccuracy undermines user confidence in the entire documentation set. Implement systematic verification processes, ideally automated, to ensure ongoing accuracy.

**Example: Accuracy Checklist**
```markdown
For each documented element, verify:
- [ ] Signature matches implementation
- [ ] All parameters listed with correct types
- [ ] Default values accurate
- [ ] Complexity analysis verified by profiling
- [ ] Error conditions tested
- [ ] Version availability confirmed
- [ ] Examples execute without error
```

### Step 9: Maintain Completeness

Users consult reference documentation to answer specific questions. Missing information forces them to abandon documentation for source code or experimentation. Regular audits ensure completeness as systems evolve.

**Example: Completeness Audit**
```python
# Automated completeness check
def audit_api_docs():
    undocumented = []
    for func in get_public_api_functions():
        if not has_reference_doc(func):
            undocumented.append(func)
        elif missing_params(func):
            undocumented.append(f"{func}: incomplete")
    return undocumented
```

### Step 10: Optimize for Scanning

Users consult references while working—they need answers quickly. Optimize layout for rapid visual scanning. Use consistent formatting, clear headings, and visual hierarchy to guide eyes to relevant information.

**Example: Scannable Layout**
```markdown
## Configuration Options

### `cache_size`
**Type:** `integer`  
**Default:** `1000`  
**Range:** `1-1000000`  
**Description:** Maximum cached items

### `cache_ttl`
**Type:** `duration`  
**Default:** `1h`  
**Format:** `<number><unit>` where unit is s|m|h|d  
**Description:** Time before cache expiry
```

## Testing and Validation

### Step 11: Automate Accuracy Verification

Unlike tutorials that require human testing, much reference documentation can be validated automatically. Extract examples and verify they produce documented results. Compare documented signatures against actual code.

**Example: Automated Verification**
```python
# doctest for automatic validation
def parse_config(path: str) -> dict:
    """
    Parse configuration from JSON file.
    
    >>> parse_config("config.json")
    {'version': '1.0', 'debug': False}
    
    >>> parse_config("missing.json")
    Traceback (most recent call last):
    FileNotFoundError: missing.json
    """
```

### Step 12: Review for Unintended Instruction

Reference documentation easily accumulates instructional content over time. Regular reviews should identify and relocate such content to appropriate how-to guides, maintaining reference purity.

**Example: Removing Instructional Content**
```markdown
# Before (Mixed Content)
## Database.connect()
Establishes database connection. You should always 
use connection pooling in production for better 
performance. First, configure your pool size based 
on expected load...

# After (Pure Reference)
## Database.connect()
Establishes database connection.

**Returns:** `Connection` object
**Raises:** `ConnectionError` if unable to connect

See: [How to configure connection pooling](../how-to/pooling.md)
```

## Common Anti-Patterns to Avoid

### The Explanation Contamination

Writers naturally want to share their understanding. In reference documentation, this impulse must be suppressed entirely. Save explanations for dedicated explanation documents.

**Anti-pattern Example:**
```markdown
# Don't explain in references:
"The cache uses LRU eviction because studies show
it provides optimal hit rates for most workloads..."
```

### The Tutorial Creep

Step-by-step instructions don't belong in references, even when describing complex APIs. Maintain strict boundaries between documentation types.

**Anti-pattern Example:**
```markdown
# Avoid tutorial content:
"First, initialize the client. Then, authenticate
using your credentials. Finally, make your request..."
```

### The Incomplete Specification

Partial documentation is dangerous documentation. Users rely on references for complete information when making technical decisions.

**Anti-pattern Example:**
```markdown
# Never leave specs incomplete:
"Accepts various options" (✗)
"Accepts options: a, b, c" (✓ - if complete)
```

## Performance Considerations

Reference documentation must load quickly and render efficiently. Users consult references frequently while working, often keeping multiple pages open.

**Example: Performance Optimization**
```markdown
# Optimize large references:
- Split by logical sections (one class per page)
- Include table of contents with jump links
- Lazy-load code examples
- Use static generation where possible
- Implement effective search indexing
- Cache rendered documentation
```

## Maintenance Strategy

Reference documentation requires immediate updates when code changes. Unlike tutorials that teach concepts, references describe current reality—any lag creates dangerous inconsistencies.

**Maintenance Checklist:**
- Daily: Update for merged API changes
- Weekly: Run automated accuracy tests
- Monthly: Audit for completeness
- Quarterly: Review for pattern consistency
- On release: Version-specific snapshots

## Quick Reference Card

| Element | Reference Approach |
|---------|-------------------|
| **Purpose** | Describe technical machinery |
| **Voice** | Neutral, third person |
| **Explanation** | None - link to explanation docs |
| **Instructions** | None - link to how-to guides |
| **Testing** | Automated accuracy verification |
| **Success Metric** | Users find accurate facts quickly |
| **Maintenance** | Immediate updates with code changes |

## Conclusion

Writing effective reference documentation requires disciplined restraint. The urge to explain, instruct, or persuade must be constantly suppressed in favor of neutral, complete description. Reference material succeeds when users can quickly find accurate, trustworthy facts about the system.

Success comes from embracing the austere nature of reference documentation. When done well, references become the bedrock of user confidence—the authoritative source users trust implicitly while working. This trust, built through completeness, accuracy, and consistency, enables users to work efficiently with your system, consulting your references as they would consult a map of familiar territory.
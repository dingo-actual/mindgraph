# Python Production Standards - Quick Reference

## Core Principles
- **Fail fast**: Validate at boundaries - imports → initialization → operation
- **Explicit over implicit**: Make assumptions visible through types and signatures
- **Immutable by default**: Mutability requires justification
- **Protocols over inheritance**: Define interfaces by capabilities, not hierarchy

## Error Handling
- Build exception hierarchies mirroring your domain model
- Include error codes and structured context in custom exceptions
- Use context managers for all resource management
- Handle errors at the appropriate abstraction level
- Never catch bare Exception except at system boundaries

## Type Safety (Pydantic v2 + Protocols)
- Parse don't validate: Use Pydantic at system boundaries
- Define protocols for structural typing and extensibility
- Create type guards for union type narrowing
- Use `TypedDict` for structured data, not raw dicts
- Annotate with protocols (Sequence, Mapping) not concrete types (list, dict)

## Data Structures
- Prefer immutable: tuple > list, frozenset > set, frozen dataclasses
- Create custom containers to enforce domain invariants
- Use `__slots__` for classes with many instances
- Choose collections by access patterns: deque for queues, heapq for priority
- Make illegal states unrepresentable through type design

## Algorithms & Control Flow
- Use generators for memory-efficient pipelines
- Apply `@cache`/`@lru_cache` systematically to recursive algorithms
- Implement state machines as classes with explicit transitions
- Early return for edge cases and errors
- Use match statements for exhaustive case analysis
- Pass context objects explicitly, never use global state

## Performance Patterns
- Lazy evaluation: cached_property, lazy imports, deferred initialization
- Memory awareness: arrays for numeric data, __slots__ for objects
- Algorithm complexity: match data structures to access patterns
- Profile before optimizing, but design for efficiency
- Batch operations and chunk large datasets

## Tool Configuration

### Ruff (pyproject.toml)
- Enable: E (errors), F (flakes), UP (upgrade), B (bugbear), SIM (simplify), I (imports)
- Line length: 100, target Python 3.11+
- Format: double quotes, space indentation
- Ignore E501 (line length) - let formatter handle

### ty Type Checker
- Focuses on inference over annotation
- Built-in library support (no plugins)
- Gradual typing friendly with minimal false positives
- Use for fast incremental checking in development

## Module Organization
- Declare public API explicitly with `__all__`
- Prefix private modules with underscore
- Layer architecture: models → services → infrastructure
- Dependency injection via constructor with Protocol types
- One public entry point per module

## Production Patterns

### Reliability
- Design for graceful degradation with fallbacks
- Make operations idempotent using request IDs
- Structured logging with correlation IDs
- Timeout everything that can block
- Circuit breakers for external dependencies

### Observability
- Trace context propagation through all operations
- Emit metrics for timing and counters
- Include structured context in all errors
- Log at boundaries, not implementation details
- Separate business events from debug logs

### API Design
- Keyword-only arguments for optional parameters
- Return types should be specific, parameter types general
- Version through addition, not modification
- Fail closed: require explicit enablement for dangerous operations
- Document failure modes in docstrings

## CI/CD Integration
- Tier checks: fast (linting) → medium (types) → slow (integration)
- Make CI reproducible locally
- Pin tool versions explicitly
- Fail builds on any error, warning, or TODO
- Automate dependency updates with constraints

## Quick Decision Guide
- Mutability? → No, unless proven necessary
- Raw dict/list? → No, use TypedDict/NamedTuple
- String flags? → No, use Enums
- isinstance checks? → No, use Protocols
- Global state? → No, use dependency injection
- Nested conditions? → No, use early returns
- Complex state? → State machine pattern
- External service? → Add timeout, retry, fallback
- Performance issue? → Measure first, then optimize
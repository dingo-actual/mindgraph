# Explanations Guide

## Purpose

This guide provides practical steps for creating effective explanations following the Diátaxis framework. An explanation is understanding-oriented documentation that illuminates why things work the way they do. This guide helps documentation writers craft explanations that deepen conceptual understanding through thoughtful exposition of design decisions, historical context, and theoretical foundations.

## Prerequisites

- Understanding of the Diátaxis framework's four documentation types
- Experience writing technical documentation
- Basic knowledge of the system or product being documented
- Ability to articulate complex concepts clearly

## Understanding Explanation Fundamentals

### Step 1: Recognize What Makes an Explanation

An explanation differs fundamentally from other documentation types by focusing on understanding rather than action. While tutorials teach by doing and how-to guides solve problems, explanations illuminate the reasoning behind decisions and the conceptual landscape surrounding implementations.

**Example: Explanation vs Reference**
```markdown
# Reference: Cache Configuration (✗)
`cache.size`: Maximum cache size in MB (default: 512)
`cache.ttl`: Time-to-live in seconds (default: 3600)

# Explanation: Understanding Our Caching Strategy (✓)
Our caching architecture balances memory usage against 
response time, employing a two-tier approach that...
```

The explanation provides context and reasoning; the reference merely states facts.

### Step 2: Identify Topics Worth Explaining

Not every aspect of your system needs explanatory documentation. Focus on areas where understanding the "why" significantly improves users' ability to work effectively with your product.

**Example: Topic Selection Criteria**
```python
# Topics that benefit from explanation:
complex_topics = [
    "Authentication architecture",  # Multiple moving parts
    "Data consistency model",       # Non-obvious trade-offs  
    "Plugin system design",         # Extensibility patterns
    "Performance optimizations"     # Counter-intuitive choices
]

# Topics that don't need explanation:
simple_topics = [
    "Button colors",               # Self-evident
    "Default port numbers",        # Arbitrary choices
    "Variable naming"              # Convention-based
]
```

## Creating the Explanation Structure

### Step 3: Establish the Conceptual Scope

Begin by clearly defining what aspect of understanding your explanation will address. Unlike tutorials with concrete outcomes, explanations explore territories of knowledge that must be meaningfully bounded.

**Example: Effective Scope Definition**
```markdown
# About Database Connection Pooling

This explanation covers how our connection pooling system
manages database resources, why we chose specific pool
sizes, and the trade-offs between connection reuse and
resource consumption.

We'll explore:
- The lifecycle of pooled connections
- Why we rejected thread-local storage
- How pool sizing affects application behavior
- Design decisions influenced by cloud deployments
```

### Step 4: Build from Familiar to Complex

Structure explanations to guide readers from concepts they likely understand to more sophisticated ideas. This scaffolding approach helps readers construct robust mental models.

**Example: Progressive Complexity**
```markdown
## Understanding Rate Limiting

### The Shopping Cart Analogy
Rate limiting works like a store limiting customers
during sales - controlling flow prevents system overload.

### Technical Implementation
Our rate limiter uses token buckets because this
algorithm naturally handles burst traffic while
maintaining long-term limits...

### Mathematical Foundation
The token generation rate R and bucket capacity B
create a system where average throughput ≤ R while
allowing bursts up to B tokens...
```

## Writing Explanation Content

### Step 5: Embrace Design Rationale Documentation

Explanations excel at documenting why decisions were made, including rejected alternatives. This historical context proves invaluable when revisiting architectural choices.

**Example: Design Decision Documentation**
```markdown
## Why We Chose Event Sourcing

### The Problem Space
Our financial system needed perfect audit trails,
time-travel queries, and regulatory compliance...

### Rejected Alternatives
**Change Data Capture**: While CDC provides audit logs,
it couldn't support our time-travel requirements without
significant additional infrastructure...

**Temporal Tables**: Database-specific implementations
would have locked us into particular vendors...

### Our Choice
Event sourcing emerged as the best fit because...
```

### Step 6: Connect Concepts Across Boundaries

Explanations should weave connections between different parts of your system and even to external concepts. These connections help readers see the bigger picture.

**Example: Cross-Boundary Connections**
```markdown
## How Our API Gateway Relates to Microservices

Our gateway pattern mirrors Netflix's Zuul architecture
but adapts it for our stateless design. Unlike traditional
proxies, our gateway maintains service discovery through...

This connects to our overall resilience strategy (see
"Circuit Breaker Patterns") and influences how we handle
authentication tokens (detailed in "Security Architecture").
```

### Step 7: Include Honest Trade-off Analysis

Every design decision involves trade-offs. Acknowledging these openly builds trust and helps users make informed decisions about system usage.

**Example: Trade-off Documentation**
```markdown
## Performance vs Consistency Trade-offs

Our system prioritizes availability over strict consistency,
following the CAP theorem's constraints. This means:

**We gain:**
- 99.99% uptime even during network partitions
- Sub-100ms response times globally
- Horizontal scaling without coordination

**We sacrifice:**
- Immediate consistency (eventual within ~2 seconds)
- Some operations require conflict resolution
- Certain financial operations need special handling
```

## Ensuring Explanation Effectiveness

### Step 8: Use Visual Aids Strategically

Complex concepts often benefit from visual representation. Diagrams, charts, and conceptual illustrations can convey relationships that would require paragraphs of text.

**Example: When to Use Visuals**
```python
# Good candidates for visual explanation:
visual_topics = {
    "state_machines": "State transition diagrams",
    "data_flow": "Architecture diagrams", 
    "algorithms": "Flowcharts or animations",
    "performance": "Benchmark comparison charts",
    "relationships": "Entity relationship diagrams"
}

# Poor candidates (better as text):
text_topics = {
    "design_philosophy": "Narrative explanation",
    "historical_context": "Timeline prose",
    "simple_concepts": "Brief paragraphs"
}
```

### Step 9: Provide Concrete Examples

Abstract concepts become clearer with concrete examples. However, avoid turning the explanation into a tutorial by keeping examples illustrative rather than instructional.

**Example: Illustrative vs Instructional**
```markdown
# Illustrative (✓)
Consider how our circuit breaker works: imagine a service
that usually responds in 50ms suddenly taking 5 seconds.
The circuit breaker would open after detecting this pattern,
preventing cascading failures across dependent services.

# Instructional (✗)
To implement a circuit breaker:
1. Install the circuit-breaker package
2. Configure the threshold settings
3. Wrap your service calls
```

### Step 10: Acknowledge Uncertainty and Evolution

Documentation should reflect reality, including areas of ongoing research or future changes. This honesty helps readers understand the maturity of different system aspects.

**Example: Acknowledging Evolution**
```markdown
## Future Directions for Our Storage Layer

Our current B-tree implementation serves us well for
read-heavy workloads. However, we're investigating
LSM-trees for write-intensive use cases...

Note: This architecture may evolve as we gather more
production metrics. Key decision points include:
- Write amplification measurements by Q3
- SSD endurance testing results
- Cost analysis of increased storage requirements
```

## Testing and Validation

### Step 11: Validate Conceptual Accuracy

Unlike tutorials that can be tested by following steps, explanations require different validation approaches focusing on conceptual clarity and accuracy.

**Example: Explanation Review Checklist**
```markdown
- [ ] Technical accuracy verified by system architects
- [ ] Concepts build logically from simple to complex
- [ ] Trade-offs are honestly presented
- [ ] Historical context is factually correct
- [ ] External references are authoritative
- [ ] Examples illuminate without instructing
- [ ] Accessible to target audience knowledge level
```

### Step 12: Test with Diverse Readers

Explanations benefit from review by readers with varying expertise levels. Experts catch technical errors while newcomers identify conceptual gaps.

**Example: Reader Testing Protocol**
```python
reader_profiles = {
    "expert": {
        "focus": "Technical accuracy, completeness",
        "questions": ["Are design rationales sound?",
                     "Any missing architectural context?"]
    },
    "intermediate": {
        "focus": "Conceptual clarity, connections",
        "questions": ["Do concepts flow logically?",
                     "Are comparisons helpful?"]
    },
    "beginner": {
        "focus": "Accessibility, prerequisites",
        "questions": ["What prior knowledge is assumed?",
                     "Where do I get lost?"]
    }
}
```

## Common Anti-Patterns to Avoid

### The How-To Contamination

Explanations frequently drift into procedural instructions. Maintain focus on understanding, not action.

**Anti-pattern Example:**
```markdown
# Don't do this in explanations:
"To understand caching, first install Redis, then
configure the connection settings, and run these commands..."

# Do this instead:
"Our caching strategy uses Redis because its in-memory
architecture provides microsecond latency while its
persistence options offer durability when needed..."
```

### The Reference Trap

Avoid turning explanations into exhaustive catalogs of features or options. That's what reference documentation provides.

**Anti-pattern Example:**
```markdown
# Avoid exhaustive listings:
"The API supports GET, POST, PUT, DELETE, PATCH, HEAD,
OPTIONS methods with parameters x, y, z..."

# Focus on conceptual understanding:
"Our API follows REST principles, where resources are
manipulated through standard HTTP verbs. This design
enables cache-friendly operations and stateless scaling..."
```

### The Tutorial Tendency

Resist creating step-by-step learning experiences within explanations. Link to tutorials for hands-on learning.

**Anti-pattern Example:**
```markdown
# Don't build tutorials in explanations:
"Let's explore authentication by building a login system.
First, create a new project..."

# Maintain conceptual focus:
"Our authentication system uses JWTs because they enable
stateless verification across microservices. For hands-on
experience, see our [authentication tutorial](../tutorials/)."
```

## Performance Considerations

Explanations about performance require special attention to benchmarking methodology and honest representation of results.

**Example: Performance Explanation**
```markdown
## Understanding Query Performance

Our query optimizer makes decisions based on statistics
gathered during off-peak hours. This approach means:

Benchmark methodology:
- Tests run on dedicated hardware (m5.2xlarge)
- Dataset: 10M records with realistic distribution
- Measured after warm-up period

Results show 3x improvement for analytical queries
but 15% overhead for simple lookups. This trade-off
reflects our priority on complex reporting over OLTP...
```

## Maintenance Strategy

Explanations require updates when fundamental understanding changes, not just when features change. This makes them more stable than other documentation types but requires different maintenance triggers.

**Maintenance Triggers:**
- Architectural changes that invalidate mental models
- Discovery of better analogies or explanations
- Significant performance characteristic changes
- New industry standards affecting design context
- User feedback indicating conceptual confusion

## Quick Reference Card

| Element | Explanation Approach |
|---------|---------------------|
| **Purpose** | Enable understanding of "why" |
| **Voice** | Analytical, honest about trade-offs |
| **Depth** | Comprehensive within defined scope |
| **Examples** | Illustrative, not instructional |
| **Structure** | Familiar → Complex progression |
| **Success Metric** | Reader gains conceptual understanding |
| **Maintenance** | Update when understanding changes |

## Conclusion

Writing effective explanations requires a different mindset from other documentation types. Success comes from maintaining focus on conceptual understanding while resisting the pull toward instruction or reference. The goal is to illuminate the reasoning, context, and connections that help users build robust mental models of your system.

The best explanations acknowledge complexity honestly, document trade-offs transparently, and guide readers from familiar concepts to sophisticated understanding. They serve as the conceptual foundation that makes other documentation types more effective, enabling users to not just use your system, but to reason about it intelligently.
# Documentation Standards - Quick Reference

## Overview

The Diátaxis framework organizes documentation into four distinct types, each serving a specific user need. Every document must belong to exactly one category, embodying the Unix philosophy of doing one thing well. This separation prevents mixed-purpose documents that serve no audience effectively.

## The Four Documentation Types

| Type | Purpose | User's Question | Key Phrase |
|------|---------|-----------------|------------|
| **Tutorial** | Learning by doing | "I'm new to this" | "Let me show you" |
| **How-To Guide** | Solving problems | "How do I accomplish X?" | "Here's how" |
| **Reference** | Looking up information | "What are the options?" | "Here are the facts" |
| **Explanation** | Understanding concepts | "Why does this work?" | "Here's the thinking" |

## Type-Specific Guidelines

### Tutorials (Learning-Oriented)

**Essential Elements:**

- Clear learning objective stated upfront
- Complete environment setup included
- Step-by-step instructions (no decisions)
- Progressive examples from simple to complex
- Visible success celebration
- Under 30 minutes completion time
- Next steps for continued learning

**Must test with beginners.** Remove all friction. Build confidence through guaranteed success.

### How-To Guides (Problem-Oriented)

**Required Components:**

- Problem-focused title: "How to [accomplish specific goal]"
- Prerequisites listed explicitly
- Numbered, actionable steps
- Performance implications noted
- Alternative approaches documented
- Common errors and solutions
- Links to relevant reference docs

**Assume basic familiarity.** Focus on efficiency. Document trade-offs and design rationale.

### Reference (Information-Oriented)

**Must Include:**

- Complete API signatures
- All parameters with types and defaults
- Return values and exceptions
- Complexity analysis (O-notation)
- Minimal examples (1-3 lines)
- Version information
- Cross-references to related items

**Optimize for lookup speed.** Maintain rigid consistency. Include performance characteristics.

### Explanation (Understanding-Oriented)

**Key Topics:**

- Architecture decisions and trade-offs
- Design rationale and rejected alternatives
- Conceptual overviews with diagrams
- Historical context
- Mathematical foundations
- Comparison with alternatives
- Future roadmap

**Build mental models.** Focus on "why" not "how." Include visual aids where helpful.

## Cross-Type Linking Strategy

Link forward in the learning journey. Never create circular references.

**Allowed:** Tutorial → How-To → Reference → Explanation → Tutorial  
**Forbidden:** Reference → How-To, Tutorial → Explanation (too early)

## Classification Quick Test

Ask yourself these questions in order:

1. Is the user learning something new? → **Tutorial**
2. Does the user have a specific task? → **How-To Guide**
3. Is the user looking up details? → **Reference**
4. Does the user want deeper understanding? → **Explanation**

Stop at the first "yes" – that's your document type.

## Quality Checklists

**All Documents:**

- [ ] Single, clear purpose
- [ ] Appropriate to type
- [ ] Links follow patterns
- [ ] Examples tested
- [ ] Version info current

**Tutorials:** Beginner-tested, works perfectly, builds confidence  
**How-To:** Clear goal, actionable steps, handles errors  
**Reference:** Complete, consistent, complexity documented  
**Explanation:** Conceptual clarity, honest trade-offs, good visuals

## Common Anti-Patterns

- **Tutorial Contamination:** Adding reference details to learning experiences
- **How-To Overexplanation:** Teaching theory instead of solving problems
- **Reference Tutorials:** Excessive examples in lookup documentation
- **Explanation Instructions:** Step-by-step procedures in conceptual docs

Each type serves one purpose. Mixing types reduces effectiveness for all audiences.

## Implementation Strategy

Start small with the most critical user needs. Audit existing documentation to identify mixed-content documents that need splitting. Create missing document types only when users demonstrate need through support requests or confusion. Maintain the hierarchy: Overview → Architecture → Implementation → Examples → Performance within each document type.

## Maintenance Schedule

**Weekly:** Update for product changes, fix broken examples  
**Monthly:** Audit popular pages, check links, update benchmarks  
**Quarterly:** Coverage gaps, user surveys, refresh visuals, archive obsolete content

Success comes from consistent application of these principles rather than perfection. Users learn to navigate predictable patterns, finding exactly what they need when they need it.

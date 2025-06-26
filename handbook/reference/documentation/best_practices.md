# Documentation Best Practices

1. Write for Your Audience - Identify whether readers are end-users, developers, or maintainers, and tailor technical depth, terminology, and examples to their specific needs and expertise level.

2. Document the Why, Not Just How - Explain design decisions, trade-offs, and constraints alongside implementation details to preserve crucial context that code alone cannot convey effectively.

3. Keep Documentation Close to Code - Store docs in the repository, use docstrings, and embed comments near complex logic to minimize drift between documentation and implementation.

4. Show Working Examples First - Lead with executable code samples and concrete use cases before diving into abstract concepts, APIs, or architectural details.

5. Maintain a Single Source of Truth - Avoid duplicating information across multiple locations; instead, reference authoritative sources to prevent inconsistencies and reduce maintenance burden.

6. Version Documentation with Code - Ensure documentation matches specific releases, clearly marking deprecated features and migration paths between versions to prevent confusion.

7. Test Your Documentation - Regularly verify code examples compile and run correctly, and have newcomers follow setup instructions to identify gaps or ambiguities.

8. Document Failure Modes and Limitations - Explicitly state what the software doesn't do, known issues, performance boundaries, and error conditions users might encounter.

9. Structure for Scanability - Use clear headings, bullet points, and visual hierarchy to help readers quickly locate specific information without reading everything.

10. Automate Where Possible - Generate API references from code, use linters to enforce documentation standards, and integrate documentation builds into CI/CD pipelines.

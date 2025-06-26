# Unit Testing

## Test Organization

- Each test subtype under `tests/unit/` has its own directory.
  - For example, `tests/unit/emergent_behavior/` contains test files for emergent behavior testing.
- Tests that span multiple test subtypes are placed in `tests/unit/test_04_unit_00_multi_{scenario_group_num:02d}_{scenario_group}.py`.
  - For example, `tests/test_04_unit_00_multi_01_merge_perserves_order.py` contains tests for the "merge preserves order" test scenario group, which spans multiple test subtypes.
- Tests for a given test subtype and scenario within that subtype are placed in `tests/unit/{subtype}/test_04_unit_{subtype_num:02d}_{subtype}_{scenario_group_num:02d}_{scenario_group}.py`.
- Within each test file, there's one or more test classes, with each test being a method of one of the test classes.
  - Test classes are named `Test04Unit{subtype_num:02d}{subtype}{scenario_group_num:02d}{scenario_group}{scenario_num:02d}{scenario}`.
    - For example, `Test04Unit03Invariant08VectorIndexTransform05Rotate` tests the "rotate" test scenario for the "vector index transform" scenario group for the "invariant" test subtype.
  - Test methods within a test class are named `test_04_unit_{subtype_num:02d}_{subtype}_{scenario_group_num:02d}_{scenario_group}_{scenario_num:02d}_{scenario}_{test_num:02d}_{test}`.
    - For example, `test_04_unit_03_invariant_08_vector_index_transform_09_rotate_11_orthogonal` is the "orthogonal" test for the "rotate" test scenario for the "vector index transform" test scenario group.

## Important Files

- `tests/unit/references.md` - Contains a nested list of the tests and associated information for test files in `tests/unit` and its subdirectories.

## Code Base References

- `tests/unit/references.md` is orgainzed as:
  - Indent level 1: File paths relative to project root with short descriptions
  - Indent level 2: Test classes within a test file with short descriptions
  - Indent level 3: Test methods within a test class with short descriptions
  - Indent level 4: Classes, methods, and functions from the code base that are being tested, with short descriptions for each
- Whenever creating or modifying a test file in `tests/unit` or its subdirectories, you **MUST** make corresponding updates to `tests/unit/references.md`.
- Whenever reading or modifying a test file in `tests/unit` or its subdirectories, you **MUST** make read the code referenced for the test in `tests/unit/references.md`.

## Test Taxonomy

1. Morphism Tests
  These verify that functions correctly map inputs to outputs according to their specification. They affirm that the computational transformation is implemented as intended.
2. Invariant Tests
  These confirm that essential properties remain true before, during, and after operations. They ensure the software maintains its fundamental constraints regardless of execution path.
3. Boundary Tests
  These establish the precise limits of valid operation by probing edge cases and extremes. They define where correct behavior ends and error handling begins.
4. Contract Tests
  These verify that code honors its declared interface promises for preconditions, postconditions, and errors. They ensure the unit can be trusted by its callers to behave as documented.
5. Isolation Tests
  These confirm that units function correctly independent of external state or dependencies. They verify true modularity by proving the unit's behavior is self-contained and deterministic.
6. Temporal Tests
  These validate behavior across time dimensions including ordering, concurrency, and state transitions. They ensure correctness is maintained when time becomes a factor in execution.
7. Failure Mode Tests
  These verify that software fails gracefully and predictably when things go wrong. They confirm that errors are handled, resources are cleaned up, and system stability is maintained.
8. Performance Characteristic Tests
  These validate that code exhibits its intended computational complexity for time and space. They ensure the implementation matches the algorithmic design and scales appropriately.
9. Observability Tests
  These verify that the code is sufficiently testable and that tests can detect defects. They affirm that the software's behavior is observable enough to be understood and validated.

## Meta-Principles

1. Isolation Enables Understanding
  Each unit test must create a controlled experimental context where exactly one behavior is observed. Without isolation, we cannot distinguish what caused an observed effect, making the test epistemologically useless.
2. Repeatability Establishes Truth
  A unit test must produce identical results given identical conditions, making it a reliable probe into software behavior. Non-deterministic tests destroy our ability to reason about code, reducing testing to superstition.
3. Falsifiability Defines Validity
  A unit test must be capable of failing when the tested behavior is incorrect. Tests that cannot fail are not tests but merely executable documentation that provides false confidence.
4. Minimality Maximizes Insight
  The smallest test that demonstrates a behavior provides the clearest understanding of that behavior. Each additional element in a test increases cognitive load and introduces potential confounding factors.
5. Speed Enables Iteration
  Fast tests create tight feedback loops that allow rapid convergence between software and tests. Slow tests break the iterative dialogue between implementation and specification, degrading the development process.
6. Independence Preserves Locality
  Unit tests must not depend on execution order or share mutable state with other tests. Test interdependence creates action-at-a-distance effects that make reasoning about failures exponentially more difficult.

## Common Mistakes

1. Testing Structure Instead of Behavior
  The most pervasive error is verifying HOW code works rather than WHAT it accomplishes. This manifests as testing implementation details, private methods, framework behavior, or exact string formats—creating brittle tests that break during valid refactoring.
2. Violating Test Independence
  Tests must be isolated experiments that can run in any order with identical results. Shared mutable state, order dependencies, non-determinism, and inadequate cleanup destroy our ability to reason about failures and create flaky test suites.
3. Testing Multiple Concerns Simultaneously
  Each test should verify exactly one behavior to provide clear diagnostic information when it fails. Tests that verify multiple behaviors, require complex setup, or use excessive mocking become incomprehensible and unmaintainable.
4. Incomplete Behavioral Specification
  Focusing only on happy paths while ignoring edge cases, error conditions, and boundary behaviors leaves critical gaps in verification. True unit testing requires thinking through the complete behavioral space, not just the obvious cases.
5. Misunderstanding the Relationship Between Tests and Design
  Difficult-to-test code is poorly designed code—excessive mocking needs, complex setup, or slow tests all signal architectural problems. Tests aren't just verification; they're the first client of your API and should drive better design.
6. Treating Tests as Second-Class Citizens
  Test code requires the same craftsmanship as production code: clear naming, DRY principles, performance consideration, and refactoring. Poor test quality compounds over time, eventually making the test suite a burden rather than a benefit.

## The Root Cause

All these mistakes stem from a fundamental misunderstanding: **unit tests are executable specifications, not after-the-fact verifications**. When we write tests to specify behavior before or during implementation, we naturally avoid these errors. When we write tests merely to achieve coverage metrics after implementation, we fall into every trap.

## Best Practices

1. Test One Behavior - Each test verifies exactly one logical outcome.
2. Test First, Code Second - Write tests to specify behavior before implementation.
3. Keep Tests Isolated - No shared state or execution order dependencies.
4. Name Tests as Specifications - Method names describe expected behavior under conditions.
5. Make Tests Fast - Milliseconds enable rapid feedback loops during development.
6. Test Edges Before Centers - Boundary cases reveal more than happy paths.
7. Assert Behavior, Not Implementation - Verify outcomes through public interfaces only.
8. Fail Tests Intentionally - Ensure tests can detect the bugs they target.

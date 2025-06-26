# Property Testing

## Test Organization

- Each test subtype under `tests/property/` has its own directory.
  - For example, `tests/property/emergent_behavior/` contains test files for emergent behavior testing.
- Tests that span multiple test subtypes are placed in `tests/property/test_03_property_00_multi_{scenario_group_num:02d}_{scenario_group}.py`.
  - For example, `tests/test_03_property_00_multi_01_merge_perserves_order.py` contains tests for the "merge preserves order" test scenario group, which spans multiple test subtypes.
- Tests for a given test subtype and scenario within that subtype are placed in `tests/property/{subtype}/test_03_property_{subtype_num:02d}_{subtype}_{scenario_group_num:02d}_{scenario_group}.py`.
- Within each test file, there's one or more test classes, with each test being a method of one of the test classes.
  - Test classes are named `Test03Property{subtype_num:02d}{subtype}{scenario_group_num:02d}{scenario_group}{scenario_num:02d}{scenario}`.
    - For example, `Test03Property03Invariant08VectorIndexTransform05Rotate` tests the "rotate" test scenario for the "vector index transform" scenario group for the "invariant" test subtype.
  - Test methods within a test class are named `test_03_property_{subtype_num:02d}_{subtype}_{scenario_group_num:02d}_{scenario_group}_{scenario_num:02d}_{scenario}_{test_num:02d}_{test}`.
    - For example, `test_03_property_03_invariant_08_vector_index_transform_09_rotate_11_orthogonal` is the "orthogonal" test for the "rotate" test scenario for the "vector index transform" test scenario group.

## Important Files

- `tests/property/references.md` - Contains a nested list of the tests and associated information for test files in `tests/property` and its subdirectories.

## Code Base References

- `tests/property/references.md` is orgainzed as:
  - Indent level 1: File paths relative to project root with short descriptions
  - Indent level 2: Test classes within a test file with short descriptions
  - Indent level 3: Test methods within a test class with short descriptions
  - Indent level 4: Classes, methods, and functions from the code base that are being tested, with short descriptions for each
- Whenever creating or modifying a test file in `tests/property` or its subdirectories, you **MUST** make corresponding updates to `tests/property/references.md`.
- Whenever reading or modifying a test file in `tests/property` or its subdirectories, you **MUST** make read the code referenced for the test in `tests/property/references.md`.

## Test Taxonomy

1. Algebraic Properties
  Tests that verify mathematical laws like associativity, commutativity, identity, and distributivity are preserved by operations. These ensure our implementations form the algebraic structures we claim (monoids, groups, rings).
2. Morphism Properties
  Tests that verify structure-preserving mappings, ensuring transformations maintain essential relationships between elements. These include homomorphisms, functors, and isomorphisms that guarantee `f(a ⊕ b) = f(a) ⊗ f(b)`.
3. Invariant Properties
  Tests that verify critical properties remain true throughout all operations and state transitions. These include state invariants, loop invariants, and conservation laws that must never be violated.
4. Relational Properties
  Tests that verify consistent relationships between operations, such as ordering, equivalence, and duality. These ensure properties like transitivity (`x ≤ y ∧ y ≤ z ⇒ x ≤ z`) hold across the system.
5. Compositional Properties
  Tests that verify operations combine predictably, maintaining closure, associativity, and modularity. These ensure that `(f ∘ g) ∘ h = f ∘ (g ∘ h)` and components compose without surprises.
6. Boundary Properties
  Tests that verify correct behavior at limits, edges, and special cases like zero, infinity, or maximum values. These ensure robustness when approaching singularities or domain boundaries.
7. Behavioral Contracts
  Tests that verify APIs fulfill their promised preconditions, postconditions, and exception guarantees. These ensure proper resource management and progress guarantees are maintained.
8. Model Properties
  Tests that verify implementations correctly simulate or refine their abstract specifications. These use techniques like bisimulation to ensure all observable behaviors match the model.
9. Oracle Properties
  Tests that compare results against trusted references, inverse operations, or alternative implementations. These verify correctness through properties like `decode(encode(x)) = x` or cross-validation.
10. Metamorphic Properties
  Tests that verify relationships between different inputs without knowing exact outputs. These include scaling (`f(k*x) = k*f(x)`), translation, and partitioning relationships.
11. Temporal Properties
  Tests that verify correct behavior over time, including liveness, safety, and fairness properties. These ensure systems eventually reach desired states and maintain required conditions.

## Meta-Principles

This taxonomy is structured to capture:

1. Completeness: Every meaningful property test fits into at least one category
2. Orthogonality: Categories capture distinct aspects (though tests may span multiple)
3. Hierarchy: From mathematical foundations up to system-level properties
4. Practicality: Each category maps to concrete testing strategies

The fundamental insight is that property tests affirm the **faithful preservation of structure** - whether that structure is algebraic, relational, behavioral, or temporal. They verify that our implementations are proper morphisms from our mental models to executing code.

## Common Mistakes

1. Confusing Properties with Examples
  The fundamental error is writing tests that check specific cases rather than universal invariants. This includes testing implementation steps instead of observable properties, or creating overly specific "properties" that only work for certain values.
2. Poor Generator Design
  Failing to thoughtfully design the input space leads to missing edge cases, poor shrinking behavior, or exponential generation times. Generators that don't cover interesting values or can't shrink to minimal failing cases make debugging nightmarish.
3. Testing at Wrong Abstraction Level
  Testing internal implementation details breaks encapsulation, while testing trivial tautologies provides no value. Over-constraining with too many assumptions effectively reduces property tests to example tests.
4. Inadequate Oracle Strategy
  Using the implementation under test as its own oracle, or comparing against equally buggy references, defeats the purpose. Forgetting to test how operations compose together misses critical integration properties.
5. Uncontrolled Dependencies
  Properties that depend on system time, external state, or uncontrolled randomness become flaky and irreproducible. This includes hidden assumptions about input characteristics not guaranteed by generators.
6. Thinking in Isolation
  Testing operations individually without verifying they compose correctly misses crucial system properties. Properties should verify not just individual operations but how they interact.

## Best Practices

1. Think in invariants - What properties must hold for all valid inputs?
2. Design input space thoughtfully - Cover edges, ensure shrinking, avoid explosion
3. Test observable contracts - Match abstraction to interface level
4. Choose oracles wisely - Simpler implementations or mathematical laws
5. Control all sources of variation - Deterministic, isolated, reproducible
6. Verify compositional behavior - Test how operations work together

The core insight: Property tests verify that implementations preserve structure and satisfy contracts across the entire input space, not just at specific points.

# Performance Testing

## Test Organization

- Each test subtype under `tests/performance/` has its own directory.
  - For example, `tests/performance/emergent_behavior/` contains test files for emergent behavior testing.
- Tests that span multiple test subtypes are placed in `tests/performance/test_02_performance_00_multi_{scenario_group_num:02d}_{scenario_group}.py`.
  - For example, `tests/test_02_performance_00_multi_01_model_service_scaling_at_load.py` contains tests for the "model service scaling at load" test scenario group, which spans multiple test subtypes.
- Tests for a given test subtype and scenario within that subtype are placed in `tests/performance/{subtype}/test_02_performance_{subtype_num:02d}_{subtype}_{scenario_group_num:02d}_{scenario_group}.py`.
- Within each test file, there's one or more test classes, with each test being a method of one of the test classes.
  - Test classes are named `Test02Performance{subtype_num:02d}{subtype}{scenario_group_num:02d}{scenario_group}{scenario_num:02d}{scenario}`.
    - For example, `Test02Performance04StressResilience07RequestSpike09QuadraticIncrease` tests the "quadratic increase" test scenario for the "request spike" test scenario group for the "stress resilience" test subtype.
  - Test methods within a test class are named `test_02_performance_{subtype_num:02d}_{subtype}_{scenario_group_num:02d}_{scenario_group}_{scenario_num:02d}_{scenario}_{test_num:02d}_{test}`.
    - For example, `test_02_performance_05_stress_resilience_07_request_spike_09_quadratic_increase_11_2hrs` is the "2hrs" test for the "quadratic increase" test scenario for the "request spike" test scenario group.

## Important Files

- `tests/performance/references.md` - Contains a nested list of the tests and associated information for test files in `tests/performance` and its subdirectories.

## Code Base References

- `tests/performance/references.md` is orgainzed as:
  - Indent level 1: File paths relative to project root with short descriptions
  - Indent level 2: Test classes within a test file with short descriptions
  - Indent level 3: Test methods within a test class with short descriptions
  - Indent level 4: Classes, methods, and functions from the code base that are being tested, with short descriptions for each
- Whenever creating or modifying a test file in `tests/performance` or its subdirectories, you **MUST** make corresponding updates to `tests/performance/references.md`.
- Whenever reading or modifying a test file in `tests/performance` or its subdirectories, you **MUST** make read the code referenced for the test in `tests/performance/references.md`.

## Test Taxonomy

1. Load Tolerance Tests
  System maintains functional correctness as demand approaches designed capacity. Tests verify that increasing load doesn't compromise core functionality until reaching defined limits.
2. Scalability Tests
  System performance scales predictably with resource allocation. Tests confirm that adding resources (vertical or horizontal) yields proportional performance improvements.
3. Temporal Stability Tests
  System maintains consistent performance over extended time periods. Tests detect degradation from resource leaks, state accumulation, or aging effects.
4. Stress Resilience Tests
  System degrades gracefully under extreme conditions beyond normal operation. Tests ensure controlled failure modes and recovery capabilities when limits are exceeded.
5. Latency Distribution Tests
  System provides predictable response time characteristics across all percentiles. Tests measure not just average performance but variance, tail behavior, and deadline adherence.
6. Resource Boundary Tests
  System respects and operates correctly within finite resource constraints. Tests verify behavior when approaching limits of memory, I/O, network, or concurrency resources.
7. Workload Composition Tests
  System handles realistic combinations of concurrent operations effectively. Tests confirm that mixed workloads don't create unexpected interference or priority inversions.

### Meta-Principles

Each category tests a fundamental invariant that must hold for the system to be considered performant:

- Compositional Nature: Complex performance profiles emerge from combining these fundamental tests
- Observable Boundaries: Each category reveals specific system limits and characteristics
- Degradation Patterns: Tests reveal not just limits but how systems approach those limits
- Predictability: Performance tests affirm that system behavior is predictable and measurable

## Common Mistakes

1. Testing in Fantasy Land
  Performance tests run in environments that bear little resemblance to production reality - wrong scale, idealized networks, missing system interactions, or divergent configurations. The test results become fiction when the test environment is fictional.
2. Pretending Performance is Deterministic
  Treating performance as a single number rather than a statistical distribution, ignoring variance, running tests once, and reporting averages instead of percentiles. Performance is inherently stochastic - tests must embrace this reality.
3. Measuring Only the Comfortable Middle
  Testing exclusively happy paths under moderate load while ignoring initialization effects, error scenarios, overload conditions, and long-term degradation. Real systems fail at the edges, not in the center.
4. Creating Self-Fulfilling Prophecies
  Test harnesses that hide the very problems they should reveal through coordinated omission, inadequate load generation, wrong measurement granularity, or low-resolution timing. The test infrastructure becomes the bottleneck.
5. Temporal Blindness
  Ignoring how systems behave over time - missing warm-up effects, resource leaks, garbage collection impacts, and gradual degradation. Performance is not a snapshot but a movie.
6. Testing Synthetic Abstractions
  Using artificial workloads, unrealistic data patterns, and isolated component tests that don't reflect actual usage. Real performance emerges from the messy complexity of production workloads, not clean laboratory conditions.

### Meta-Principle

Performance testing is **empirical science**, not engineering convenience. These mistakes all stem from treating performance tests as a checkbox rather than as rigorous experiments designed to reveal truth about system behavior under stress.

## Best Practices

1. Continuous Baselines - Track performance metrics across every code change
2. Production Fidelity - Match real infrastructure, data volumes, and patterns
3. Statistical Rigor - Multiple runs, report percentiles not averages
4. Component Isolation - Measure each layer to pinpoint bottlenecks
5. Resource Correlation - Monitor CPU, memory, I/O alongside latencies
6. Failure Testing - Include error paths and recovery scenarios
7. Automated Regression Detection - Machines catch subtle degradations humans miss
8. Define Success Criteria - Set specific SLOs before testing begins

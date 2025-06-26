# Integration Testing

## Test Organization

- Each test subtype under `tests/integration/` has its own directory.
  - For example, `tests/integration/emergent_behavior/` contains test files for emergent behavior testing.
- Tests that span multiple test subtypes are placed in `tests/integration/test_01_integration_00_multi_{scenario_group_num:02d}_{scenario_group}.py`.
  - For example, `tests/test_01_integration_00_multi_03_client_server_config_error.py` contains tests for the "client server config error" test scenario group, which spans multiple test subtypes.
- Tests for a given test subtype and scenario within that subtype are placed in `tests/integration/{subtype}/test_01_integration_{subtype_num:02d}_{subtype}_{scenario_group_num:02d}_{scenario_group}.py`.
- Within each test file, there's one or more test classes, with each test being a method of one of the test classes.
  - Test classes are named `Test01Integration{subtype_num:02d}{subtype}{scenario_group_num:02d}{scenario_group}{scenario_num:02d}{scenario}`.
    - For example, `Test01Integration05ResourceCoordination02HorizontalScaling05LoadBalancing` tests the "load balancing" test scenario for the "horizontal scaling" test scenario group for the "resource coordination" test subtype.
  - Test methods within a test class are named `test_01_integration_{subtype_num:02d}_{subtype}_{scenario_group_num:02d}_{scenario_group}_{scenario_num:02d}_{scenario}_{test_num:02d}_{test}`.
    - For example, `test_01_integration_05_resource_coordination_02_horizontal_scaling_05_load_balancing_11_work_stealing` is the "work stealing" test for the "load balancing" test scenario for the "horizontal scaling" test scenario group.

## Important Files

- `tests/integration/references.md` - Contains a nested list of the tests and associated information for test files in `tests/integration` and its subdirectories.

## Code Base References

- `tests/integration/references.md` is orgainzed as:
  - Indent level 1: File names with short descriptions
  - Indent level 2: Test classes with short descriptions
  - Indent level 3: Test methods with short descriptions
  - Indent level 4: Classes, methods, and functions from the code base that are being tested, with short descriptions for each
- Whenever creating or modifying a test file in `tests/integration` or its subdirectories, you **MUST** make corresponding updates to `tests/integration/references.md`.
- Whenever reading or modifying a test file in `tests/integration` or its subdirectories, you **MUST** make read the code referenced for the test in `tests/integration/references.md`.

## Test Taxonomy

1. Contract Conformance Tests
  Verify that components honor their declared interfaces when composed together. Ensure type signatures, behavioral contracts, protocols, and data schemas remain compatible across boundaries.
2. Boundary Traversal Tests
  Verify correct behavior as data and control flow cross component boundaries. Test serialization, context propagation, resource handoffs, and lifecycle coordination between components.
3. Emergent Behavior Tests
  Verify properties that only exist when components interact as a system. Test compositional invariants, interaction patterns, cascading effects, and feedback loops that arise from integration.
4. Failure Propagation Tests
  Verify system resilience when individual components fail. Ensure failures are isolated, degradation is graceful, recovery is coordinated, and errors maintain meaning across layers.
5. Resource Coordination Tests
  Verify efficient resource usage across component boundaries. Test shared resources, lifecycle management, quota distribution, and deadlock prevention in the integrated system.
6. Temporal Coordination Tests
  Verify time-dependent interactions between components. Test synchronization, ordering guarantees, timeout coordination, and clock consistency across distributed components.
7. Configuration Coherence Tests
  Verify consistent configuration across all components. Test configuration propagation, conflict detection, dynamic reconfiguration, and environment consistency throughout the system.
8. Performance Composition Tests
  Verify performance characteristics of the integrated system. Test latency accumulation, throughput bottlenecks, resource amplification, and performance interference between components.

### Compositional Meta-Principle

These categories compose to test complex integration scenarios - for example, combining Failure + Temporal tests how failures affect synchronization, or Resource + Performance tests how contention impacts latency. This compositional approach enables testing emergent properties by combining fundamental test categories, aligning with the principle that complex behaviors arise from simple, well-defined interactions.

## Common Mistakes

1. Testing the Mocked System Instead of the Real System
  Integration tests that mock too many dependencies end up testing the mocks' behavior rather than actual component interactions. This creates false confidence since mocks often implement idealized behavior that diverges from real components over time.
2. Assuming Synchronous, Reliable Communication
  Writing tests that assume instant, ordered, always-successful communication between components ignores the fundamental nature of distributed systems. Real integrations involve latency, message reordering, partial failures, and network partitions that must be explicitly tested.
3. Testing Only the Happy Integration Path
  Focusing exclusively on successful component coordination while ignoring failure modes, timeout cascades, and partial state corruptions. The most critical integration behaviors emerge when components disagree, fail, or enter undefined states.
4. Environmental Fidelity Decay
  Integration test environments that start as production-like gradually accumulate shortcuts, simplified configurations, and missing components. This drift creates tests that pass in CI but fail in production due to untested environmental dependencies.
5. Ignoring Emergent Resource Constraints
  Testing components in isolation often succeeds, but integration reveals resource competition, lock contention, and cascading bottlenecks. Failing to test under realistic concurrent load misses deadlocks, resource starvation, and performance cliffs.
6. Binary Thinking About Integration State
  Treating integration as "working" or "broken" rather than recognizing the spectrum of partial functionality, degraded modes, and inconsistent states. Real systems exist in partially integrated states far more often than in fully coherent ones.

### Meta-Pattern: The Idealization Trap

Each mistake stems from oversimplifying the messy reality of component interaction—assuming cleaner contracts, more reliable communication, and more binary states than actually exist in production systems.

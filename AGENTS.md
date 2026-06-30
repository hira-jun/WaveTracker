# WaveTracker Agent Workflow

This file defines the recommended agent workflow for TDD and DDD execution.

## Modes

### Explore

- Goal: Read-only discovery of existing behavior, constraints, and boundaries.
- Output: concise findings, impacted files, and proposed test cases.

### Design

- Goal: Shape bounded context impact and use-case boundary before coding.
- Output: small design note with dependencies, invariants, and anti-pattern checks.

### Implement

- Goal: Apply minimal production code changes that satisfy failing tests.
- Output: focused code diff with boundary-safe dependencies.

### Test

- Goal: Add and run unit/integration/e2e tests based on scope.
- Output: pass/fail evidence and deterministic fixture updates.

### Review

- Goal: Validate DDD boundaries, TDD cycle completion, and regression risk.
- Output: findings-first review with severity and missing tests.

## Standard PR Flow

1. Explore impacted behavior and boundaries.
2. Design minimal change and choose test scope.
3. Add failing test first.
4. Implement minimum change.
5. Refactor with tests green.
6. Review architecture and test coverage deltas.

## Fast Checks

- No route-to-adapter direct orchestration for complex business flow.
- No framework exceptions in domain modules.
- Coordinate normalization stays centralized.
- Raw ZIP vs parsed entities remain storage-separated.

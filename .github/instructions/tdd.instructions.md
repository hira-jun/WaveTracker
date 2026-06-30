---
applyTo: "**"
description: "TDD conventions for WaveTracker test-first implementation and test layering."
---

# TDD Instructions

Scope notes:
- Backend tests: `backend/tests/**`
- Frontend tests: `frontend/tests/**`
- Collector contract checks: `collectors/**`

- Follow Red -> Green -> Refactor for every behavior change.
- Write or update tests before production code changes.
- Keep tests deterministic: avoid hidden time, random, network, and global state dependencies.
- Classify tests by intent:
  - unit: pure domain logic and lightweight adapters
  - integration: route/service + storage boundaries
  - e2e: end-to-end user flow and ZIP contract scenarios
- Prefer fast unit tests over broad integration tests.
- Use shared fixtures/builders to avoid duplicated test setup.
- In frontend tests, verify user-visible behavior, not internal implementation details.
- In collector validation, assert required ZIP entries and schema compatibility.
- Every PR should include:
  - at least one failing test observed before implementation
  - evidence of green tests after implementation
  - brief note for refactor intent if structure changed

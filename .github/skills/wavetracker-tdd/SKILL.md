---
name: wavetracker-tdd
description: "Use when implementing or modifying behavior in WaveTracker with a strict test-first workflow across backend, frontend, and collector contracts."
---

# WaveTracker TDD Skill

## Purpose

Use this skill to keep changes small, verifiable, and regression-resistant.

## Workflow

1. Define behavior change in one sentence.
2. Add or update the smallest failing test.
3. Implement the minimum change to make it pass.
4. Refactor with tests green.
5. Record edge cases as additional tests.

## Backend Pattern

- Prefer unit tests for domain logic in `backend/app/domain`.
- Use integration tests for route/use-case/storage boundaries.
- Add fixture builders in `backend/tests/conftest.py` when setup repeats.

## Frontend Pattern

- Test page/component behavior from user interaction.
- Validate coordinate conversion and visible state transitions.
- Keep API mocking in service boundary tests, not UI internals.

## Collector Pattern

- Validate ZIP contract entries and metadata schema.
- Add negative tests for missing files and malformed JSON.

## Done Criteria

- New behavior is covered by tests.
- Existing tests remain green.
- Refactor changes keep semantics intact.

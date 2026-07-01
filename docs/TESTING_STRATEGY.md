# Testing Strategy

## Objectives

- Keep behavior changes safe through test-first development.
- Optimize feedback speed with a test pyramid.
- Make regressions visible in CI before merge.

## Test Pyramid Targets

- Unit: 70%
- Integration: 20%
- End-to-end or contract: 10%

## Scope by Area

### Backend

- Unit: `backend/app/domain/**` rules and value behavior.
- Integration: API/use-case/storage boundaries in `backend/tests/**`.
- Contract: ZIP parser and required artifact checks.

### Frontend

- Unit/component: map interaction, coordinate transform, async states.
- Integration: page + service boundary with mocked API.

### Collectors

- Contract tests for generated ZIP entries and metadata schema.
- Negative tests for missing required files and malformed content.

## TDD Cycle

1. Add failing test for the target behavior.
2. Implement minimal production change.
3. Refactor only with tests green.

## Quality Gates (Phased)

- Phase A (warning): run tests + report architecture anti-pattern findings.
- Phase B (required): block merge on failing tests and selected anti-patterns.
- First promoted required rule: no FastAPI dependency (`from fastapi`, `import fastapi`, `HTTPException`) inside `backend/app/domain/**`.
- Second promoted required rule: no direct imports of local storage implementations (`local_blob_adapter`, `local_table_adapter`) inside `backend/app/api/routes/**`.
- Third promoted required rule: no direct adapter references (`table_adapter.`, `blob_adapter.`, `local_*_adapter`) inside `backend/app/api/routes/**`.

## Minimal PR Checklist

- New or changed behavior has tests.
- Test results are green in local or CI runs.
- Any refactor is covered by existing tests.

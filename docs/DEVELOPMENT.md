# Development

## Conventions

- Keep Phase0 focused on harness and scaffolding.
- Keep storage contracts explicit and versioned.
- Keep route and component boundaries narrow.

## Commands

- Backend: `make -C backend lint test run`
- Frontend: `make -C frontend lint test dev`
- Infra: `make -C infra config up`

## Commands (PowerShell Fallback)

- Backend lint: `Set-Location backend; python -m ruff check app tests`
- Backend test: `Set-Location backend; python -m pytest -q`
- Frontend lint: `Set-Location frontend; npm run lint`
- Frontend test: `Set-Location frontend; npm run test`
- Infra config: `Set-Location infra; docker compose -f docker-compose.yml config`

## Branching

- Use small, focused commits by concern.
- Do not mix infra changes with feature changes unless required.

## TDD and DDD Harness

- Workflow definition: `AGENTS.md`
- Testing strategy: `docs/TESTING_STRATEGY.md`
- DDD architecture guide: `docs/ARCHITECTURE_DDD.md`
- Agent instructions:
	- `.github/instructions/tdd.instructions.md`
	- `.github/instructions/ddd.instructions.md`
	- `.github/instructions/architecture.instructions.md`
- Skills:
	- `.github/skills/wavetracker-tdd/SKILL.md`
	- `.github/skills/wavetracker-ddd/SKILL.md`

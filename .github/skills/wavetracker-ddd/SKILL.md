---
name: wavetracker-ddd
description: "Use when shaping WaveTracker features with bounded contexts, use cases, domain rules, and storage ports."
---

# WaveTracker DDD Skill

## Purpose

Use this skill to keep business rules explicit and infrastructure concerns replaceable.

## Bounded Contexts

- Admin: authentication, credential lifecycle, admin-only controls.
- Survey: ZIP ingestion, parsing, session creation, reading persistence.
- Floor: floor metadata, map assets, normalized coordinates.
- Analytics: aggregation, issue summaries, reporting read models.

## Layering Rules

- API layer: transport concerns, request/response mapping.
- Application/use-case layer: orchestration and transaction boundaries.
- Domain layer: invariants, policies, value objects, domain errors.
- Infrastructure layer: adapters for blob/table/local/azure implementations.

## Use-Case Style

- One use-case per command/query behavior.
- Inject ports into use-cases.
- Return explicit result objects instead of loose dictionaries.

## Error Boundary

- Raise domain/application errors below API layer.
- Map to HTTP errors only in routes.

## Anti-Patterns

- Route handlers performing multi-step business orchestration.
- Domain modules importing FastAPI or framework exceptions.
- Direct adapter calls from unrelated bounded contexts.

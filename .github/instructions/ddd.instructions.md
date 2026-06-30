---
applyTo: "backend/app/**"
description: "DDD conventions for WaveTracker bounded contexts, use cases, and dependency direction."
---

# DDD Instructions

- Keep bounded contexts explicit: Admin, Survey, Analytics, Floor.
- Keep dependency direction inward: API -> application/use-case -> domain -> ports.
- Do not call infrastructure adapters directly from route handlers.
- Put orchestration logic in use-case/application services, not in routes.
- Keep domain rules in domain modules and make them framework-agnostic.
- Prefer domain-specific exceptions inside domain/use-case layers.
- Convert domain errors to HTTP concerns only at API boundary.
- Keep entities and value objects focused on invariants and behavior.
- Keep repository and storage access behind ports/protocols.
- Avoid cross-context coupling; share only clearly defined contracts.

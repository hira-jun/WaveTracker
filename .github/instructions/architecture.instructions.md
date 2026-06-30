---
applyTo: "**"
description: "Architecture guardrails for WaveTracker layer boundaries and map-coordinate consistency."
---

# Architecture Instructions

Scope notes:
- Backend: `backend/app/**`
- Frontend: `frontend/src/**`

- Maintain clear layers and narrow interfaces between them.
- Keep transport-specific logic (HTTP, request parsing) out of domain logic.
- Keep coordinate normalization centralized and consistent:
  - xNorm = x / width
  - yNorm = y / height
- Keep raw ZIP storage separate from parsed analytical entities.
- Prefer explicit contracts over implicit dictionary-shaped payloads.
- Avoid circular dependencies between modules and contexts.
- Keep observability and validation near boundaries, not mixed with core domain rules.

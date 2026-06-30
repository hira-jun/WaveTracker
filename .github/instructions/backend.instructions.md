---
applyTo: "backend/**"
description: "Backend conventions for WaveTracker FastAPI code, validation, and storage abstraction."
---

# Backend Instructions

- Use Python 3.11+.
- Keep API routes in `backend/app/api/routes` and shared schemas in `backend/app/api/schemas`.
- Validate all request/response bodies with Pydantic models.
- Keep storage interactions behind interfaces so local and Azure adapters are swappable.
- Prefer deterministic unit tests and avoid hidden side effects.

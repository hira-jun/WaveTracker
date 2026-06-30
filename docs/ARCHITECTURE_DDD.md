# Architecture (DDD)

## Bounded Contexts

- Admin: authentication and admin lifecycle operations.
- Survey: upload, parse, session creation, reading ingestion.
- Floor: floor definitions and map coordinate handling.
- Analytics: read-model aggregation and reporting.

## Layered Structure

- API: transport and schema mapping.
- Application/Use Case: workflow orchestration and dependency composition.
- Domain: business invariants and rules.
- Infrastructure: storage and external adapters.

## Dependency Direction

- Outer layers depend inward.
- Domain does not depend on FastAPI or adapter implementations.
- Routes should delegate business orchestration to use-cases.

## Storage Separation

- Raw uploaded ZIP payloads are blob-oriented artifacts.
- Parsed records for sessions/readings/issues are table-oriented entities.

## Coordinate Consistency

- Normalized map coordinates are required for persisted points.
- Formula:
  - xNorm = x / width
  - yNorm = y / height

## Near-Term Refactor Target

- Move multi-step survey upload orchestration from route handler to a dedicated use-case.
- Keep route layer responsible for HTTP concerns and result mapping only.

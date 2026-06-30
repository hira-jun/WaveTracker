# Architecture

## Target Stack

- Frontend: React + TypeScript
- Backend: FastAPI
- Hosting: Azure App Service
- Storage: Blob (raw files) + Table (normalized records)

## Phase0 Boundaries

- In scope:
  - Development harness
  - Collector templates
  - Copilot skill and instructions
- Out of scope:
  - Full business APIs
  - Full analytics and heatmaps
  - Entra ID enforcement

## Data Flow (Planned)

1. Collector script captures Wi-Fi data offline.
2. ZIP package is uploaded through web UI.
3. Backend stores raw ZIP and parsed entities separately.
4. Frontend consumes normalized readings for map visualization.

# Setup

## Prerequisites

- Python 3.11+
- Node.js 20+
- Docker Desktop

## Python Distribution Note

- Use a standard CPython distribution (python.org installer, py launcher, or uv-managed Python).
- MSYS2-managed Python in this workspace could not install `pydantic-core` wheels and attempted a Rust build.
- If you are on MSYS2 shell, prefer running backend commands with a non-MSYS CPython executable.

## Local Bootstrap

1. Backend
   - `cd backend`
   - `python -m pip install -e .[dev]`
2. Frontend
   - `cd frontend`
   - `npm install`
3. Infra
   - `cd infra`
   - `docker compose -f docker-compose.yml up --build`

## PowerShell Quick Commands

- Backend install: `Set-Location backend; python -m pip install -e .[dev]`
- Backend run: `Set-Location backend; python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
- Frontend install: `Set-Location frontend; npm install`
- Frontend run: `Set-Location frontend; npm run dev -- --host 0.0.0.0 --port 3000`
- Infra config check: `Set-Location infra; docker compose -f docker-compose.yml config`

## TDD/DDD Harness Quick Start

1. Review workflow and rules
   - `AGENTS.md`
   - `.github/instructions/tdd.instructions.md`
   - `.github/instructions/ddd.instructions.md`
   - `.github/instructions/architecture.instructions.md`
2. Review supporting design and test guides
   - `docs/TESTING_STRATEGY.md`
   - `docs/ARCHITECTURE_DDD.md`
3. Run local checks before push
   - Backend: `Set-Location backend; python -m pytest -q`
   - Frontend: `Set-Location frontend; npm run test`
   - Collectors contract: `Set-Location .; d:/workspace/WaveTracker-1/.venv/Scripts/python.exe -m pytest collectors/tests -q`
4. CI quality gate
   - GitHub Actions workflow: `.github/workflows/quality-gate.yml`
   - Architecture warnings remain in warning mode.
   - Required architecture rule is enabled: `backend/app/domain/**` must not import FastAPI concerns.
   - Required architecture rule is enabled: `backend/app/api/routes/**` must not import local storage implementation modules.
   - Required architecture rule is enabled: `backend/app/api/routes/**` must not directly reference adapters (`table_adapter` / `blob_adapter`).

## CORS Configuration (Local/Container)

- Backend accepts frontend origins from `CORS_ALLOW_ORIGINS` (comma-separated).
- Default when unset: `http://localhost:3000,http://127.0.0.1:3000`
- Example: `CORS_ALLOW_ORIGINS=http://localhost:3000,http://localhost:5173`

## Admin Screen (First Access)

- Open frontend and switch to the `Admin` tab.
- On first access, set the admin password (minimum 8 characters).
- After setup, the same password is used for admin login.
- Admin-authenticated operations:
   - Create floor
   - Upload floor map
   - Update admin settings
- Additional admin security operations:
   - Change admin password (`/admin/change-password`)
   - Logout / token invalidation (`/admin/logout`)
- Admin state is stored at `backend/data/admin/state.json` in local development.
- Admin session token is stored in browser `localStorage` with key `wavetracker_admin_token`.

## Health Check

- Bash: `infra/scripts/health-check.sh`
- PowerShell: `infra/scripts/health-check.ps1`

## Azure Deployment (Bicep, Dev)

1. Azure login and subscription selection
   - `az login`
   - `az account set --subscription <subscription-id-or-name>`
2. Resource group
   - `az group create --name <resource-group-name> --location japaneast`
3. Validate Bicep template
   - `Set-Location infra/bicep`
   - `az bicep build --file main.bicep`
4. Deploy
   - `Set-Location infra/bicep/scripts`
   - `./deploy.ps1 -ResourceGroupName <resource-group-name>`

### Deployed Resources (Dev)

- Azure Container Apps environment
- Backend and Frontend Container Apps
- Azure Container Registry
- Azure Storage Account (Blob containers: `raw-uploads`, `floor-maps`)
- Azure Cosmos DB (Table API tables: `Floors`, `SurveySessions`, `SurveyReadings`, `IssueReports`)
- Log Analytics workspace

### Continue Later

- Use `docs/BICEP_NEXT_STEPS.md` as the resumable checklist and execution guide.

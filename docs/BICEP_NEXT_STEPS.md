# Bicep Next Steps and Resume Guide

This file tracks what is already implemented and what to do next so work can resume quickly.

## Current Status Snapshot (2026-06-30)

Completed:
- Added Bicep entrypoint and modules under `infra/bicep/`.
- Added dev parameter file at `infra/bicep/params/dev.bicepparam`.
- Added deployment script at `infra/bicep/scripts/deploy.ps1`.
- Added setup instructions for Azure Bicep deployment in `docs/SETUP.md`.
- Confirmed template build succeeds: `az bicep build --file infra/bicep/main.bicep`.

Known warning:
- Cosmos Table API resources may emit BCP081 type warnings during build. This is expected and does not block deployment.

## Resume From Here

1. Open workspace root.
2. Validate template still compiles.
3. Build and push container images to ACR.
4. Run Bicep deployment to dev resource group.
5. Verify backend/frontend endpoints and storage writes.

## Step-by-Step Execution

### Step 1: Validate Bicep

Run:

```powershell
Set-Location infra/bicep
az bicep build --file main.bicep
```

Success criteria:
- Build exits with code 0.
- Only known BCP081 warning is present.

### Step 2: Create or confirm resource group

Run:

```powershell
az group create --name <rg-name> --location japaneast
```

Success criteria:
- Resource group exists and is in the target subscription.

### Step 3: Build and push backend/frontend images

Inputs needed:
- ACR login server output from deployment or pre-created registry.
- Image tags for backend and frontend.

Suggested commands:

```powershell
# Example only. Replace values with real registry and tags.
docker build -t <acr-login-server>/backend:<tag> backend
docker build -t <acr-login-server>/frontend:<tag> frontend
docker push <acr-login-server>/backend:<tag>
docker push <acr-login-server>/frontend:<tag>
```

Success criteria:
- Both images are visible in ACR repositories.

### Step 4: Deploy infra to dev

Run:

```powershell
Set-Location infra/bicep/scripts
./deploy.ps1 -ResourceGroupName <rg-name>
```

Optional override for parameters:

```powershell
./deploy.ps1 -ResourceGroupName <rg-name> -ParameterFile ../params/dev.bicepparam
```

Success criteria:
- Deployment status is Succeeded.
- Outputs include backendUrl and frontendUrl.

### Step 5: Smoke test apps

Checks:
- Open frontendUrl and verify app loads.
- Call backend health endpoint and verify 200 response.
- Upload survey ZIP and verify expected writes to Blob and Table API.

## Pending Implementation Tasks

Priority 1:
- Implement backend Azure storage adapters for Blob and Cosmos Table API.
- Wire dependency injection to select Azure adapters in cloud runtime.

Priority 2:
- Add image build and push automation in CI/CD.
- Add pre-deploy what-if command/script.

Priority 3:
- Add staging/prod parameter files and hardened network options.

## Task Checklist

- [x] Bicep structure created
- [x] Dev parameters created
- [x] Deploy script created
- [ ] Azure storage adapters implemented in backend
- [ ] CI/CD image pipeline added
- [ ] what-if validation added
- [ ] End-to-end smoke test executed in Azure

## Quick Restart Commands

```powershell
# 1) Build validation
Set-Location infra/bicep
az bicep build --file main.bicep

# 2) Deploy
Set-Location scripts
./deploy.ps1 -ResourceGroupName <rg-name>
```

# WaveTracker Bicep Infrastructure

This directory contains the Azure infrastructure definition for WaveTracker.

## Scope

- Environment: dev
- Runtime: Azure Container Apps
- Data: Blob Storage + Cosmos DB Table API
- Registry: Azure Container Registry
- Observability: Log Analytics

## File Layout

- `main.bicep`: Entry point for resource group deployment.
- `modules/`: Reusable infrastructure modules.
- `params/dev.bicepparam`: Development environment parameters.
- `scripts/deploy.ps1`: Helper script for deployment.

## Prerequisites

- Azure CLI with Bicep integration
- Logged in Azure session (`az login`)
- Existing Azure resource group

## Validate

```powershell
Set-Location infra/bicep
az bicep build --file main.bicep
```

## Deploy

```powershell
Set-Location infra/bicep/scripts
./deploy.ps1 -ResourceGroupName <your-resource-group>
```

## Post-Deploy Notes

- Push backend and frontend images to the generated ACR.
- Use `backendUrl` and `frontendUrl` outputs to confirm routing.
- Backend app settings are pre-wired for Azure Blob and Cosmos Table connection values.

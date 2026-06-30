using '../main.bicep'

param environment = 'dev'
param appName = 'wavetracker'
param location = 'japaneast'

param tags = {
  project: 'WaveTracker'
  environment: 'dev'
  owner: 'platform-team'
  managedBy: 'bicep'
}

param backendImageTag = 'latest'
param frontendImageTag = 'latest'

param backendCpu = '0.5'
param backendMemory = '1Gi'
param frontendCpu = '0.5'
param frontendMemory = '1Gi'

param acrSku = 'Basic'
param storageSku = 'Standard_LRS'
param cosmosOfferType = 'Standard'
param cosmosConsistencyLevel = 'Session'

targetScope = 'resourceGroup'

@description('Deployment environment name.')
@allowed([
  'dev'
  'staging'
  'prod'
])
param environment string = 'dev'

@description('Base application name used in resource naming.')
param appName string = 'wavetracker'

@description('Azure region for resources.')
param location string = resourceGroup().location

@description('Tags applied to all resources.')
param tags object = {
  project: 'WaveTracker'
  environment: environment
  managedBy: 'bicep'
}

@description('Container image tag for backend container.')
param backendImageTag string = 'latest'

@description('Container image tag for frontend container.')
param frontendImageTag string = 'latest'

@description('Container Apps CPU allocation for backend app.')
param backendCpu string = '0.5'

@description('Container Apps memory allocation for backend app.')
param backendMemory string = '1Gi'

@description('Container Apps CPU allocation for frontend app.')
param frontendCpu string = '0.5'

@description('Container Apps memory allocation for frontend app.')
param frontendMemory string = '1Gi'

@description('Azure Container Registry SKU.')
@allowed([
  'Basic'
  'Standard'
  'Premium'
])
param acrSku string = 'Basic'

@description('Storage account SKU used for blob data.')
@allowed([
  'Standard_LRS'
  'Standard_GRS'
  'Standard_RAGRS'
  'Standard_ZRS'
  'Standard_GZRS'
  'Standard_RAGZRS'
])
param storageSku string = 'Standard_LRS'

@description('Cosmos DB account offer type.')
@allowed([
  'Standard'
])
param cosmosOfferType string = 'Standard'

@description('Cosmos DB consistency level.')
@allowed([
  'Eventual'
  'ConsistentPrefix'
  'Session'
  'BoundedStaleness'
  'Strong'
])
param cosmosConsistencyLevel string = 'Session'

var suffix = toLower(uniqueString(subscription().id, resourceGroup().id, appName, environment))
var shortSuffix = substring(suffix, 0, 8)

var logAnalyticsName = substring('${appName}-${environment}-law-${shortSuffix}', 0, 63)
var containerEnvName = substring('${appName}-${environment}-cae-${shortSuffix}', 0, 32)
var acrName = substring(replace('${appName}${environment}${shortSuffix}acr', '-', ''), 0, 50)
var storageAccountName = substring(replace(toLower('${appName}${environment}${shortSuffix}sa'), '-', ''), 0, 24)
var cosmosAccountName = substring(replace(toLower('${appName}-${environment}-${shortSuffix}-cosmos'), '-', ''), 0, 44)
var backendAppName = substring('${appName}-${environment}-backend', 0, 32)
var frontendAppName = substring('${appName}-${environment}-frontend', 0, 32)

module logAnalytics './modules/log-analytics.bicep' = {
  name: 'logAnalyticsModule'
  params: {
    workspaceName: logAnalyticsName
    location: location
    tags: tags
  }
}

module containerEnv './modules/container-env.bicep' = {
  name: 'containerEnvModule'
  params: {
    managedEnvironmentName: containerEnvName
    location: location
    workspaceCustomerId: logAnalytics.outputs.customerId
    workspaceSharedKey: logAnalytics.outputs.sharedKey
    tags: tags
  }
}

module registry './modules/acr.bicep' = {
  name: 'acrModule'
  params: {
    acrName: acrName
    location: location
    sku: acrSku
    tags: tags
  }
}

module storage './modules/storage.bicep' = {
  name: 'storageModule'
  params: {
    storageAccountName: storageAccountName
    location: location
    skuName: storageSku
    tags: tags
    blobContainers: [
      'raw-uploads'
      'floor-maps'
    ]
  }
}

module cosmos './modules/cosmos-table.bicep' = {
  name: 'cosmosTableModule'
  params: {
    accountName: cosmosAccountName
    location: location
    tags: tags
    offerType: cosmosOfferType
    consistencyLevel: cosmosConsistencyLevel
    tableNames: [
      'Floors'
      'SurveySessions'
      'SurveyReadings'
      'IssueReports'
    ]
  }
}

module backend './modules/container-app-backend.bicep' = {
  name: 'backendContainerAppModule'
  params: {
    appName: backendAppName
    location: location
    tags: tags
    managedEnvironmentId: containerEnv.outputs.id
    acrLoginServer: registry.outputs.loginServer
    acrUsername: registry.outputs.username
    acrPassword: registry.outputs.password
    imageName: 'backend'
    imageTag: backendImageTag
    cpu: backendCpu
    memory: backendMemory
    blobEndpoint: storage.outputs.blobEndpoint
    rawUploadsContainerName: 'raw-uploads'
    floorMapsContainerName: 'floor-maps'
    cosmosTableEndpoint: cosmos.outputs.tableEndpoint
    cosmosPrimaryKey: cosmos.outputs.primaryKey
  }
}

module frontend './modules/container-app-frontend.bicep' = {
  name: 'frontendContainerAppModule'
  params: {
    appName: frontendAppName
    location: location
    tags: tags
    managedEnvironmentId: containerEnv.outputs.id
    acrLoginServer: registry.outputs.loginServer
    acrUsername: registry.outputs.username
    acrPassword: registry.outputs.password
    imageName: 'frontend'
    imageTag: frontendImageTag
    cpu: frontendCpu
    memory: frontendMemory
    backendBaseUrl: backend.outputs.httpsUrl
  }
}

output backendUrl string = backend.outputs.httpsUrl
output frontendUrl string = frontend.outputs.httpsUrl
output acrLoginServer string = registry.outputs.loginServer
output storageAccountName string = storage.outputs.accountName
output cosmosTableEndpoint string = cosmos.outputs.tableEndpoint

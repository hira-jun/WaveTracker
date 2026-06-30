param storageAccountName string
param location string
param skuName string = 'Standard_LRS'
param tags object = {}
param blobContainers array = []

resource storage 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: storageAccountName
  location: location
  tags: tags
  sku: {
    name: skuName
  }
  kind: 'StorageV2'
  properties: {
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
    supportsHttpsTrafficOnly: true
    accessTier: 'Hot'
  }
}

resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2023-05-01' = {
  parent: storage
  name: 'default'
}

resource containers 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-05-01' = [for containerName in blobContainers: {
  parent: blobService
  name: containerName
  properties: {
    publicAccess: 'None'
  }
}]

output id string = storage.id
output accountName string = storage.name
output blobEndpoint string = storage.properties.primaryEndpoints.blob

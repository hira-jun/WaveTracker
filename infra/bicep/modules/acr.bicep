param acrName string
param location string
param sku string = 'Basic'
param tags object = {}

resource acr 'Microsoft.ContainerRegistry/registries@2023-07-01' = {
  name: acrName
  location: location
  tags: tags
  sku: {
    name: sku
  }
  properties: {
    adminUserEnabled: true
    publicNetworkAccess: 'Enabled'
  }
}

var creds = acr.listCredentials()

output id string = acr.id
output name string = acr.name
output loginServer string = acr.properties.loginServer
output username string = creds.username
@secure()
output password string = creds.passwords[0].value

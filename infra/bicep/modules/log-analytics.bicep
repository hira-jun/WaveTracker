param workspaceName string
param location string
param tags object = {}

resource workspace 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: workspaceName
  location: location
  tags: tags
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
  }
}

var sharedKeys = workspace.listKeys()

output id string = workspace.id
output customerId string = workspace.properties.customerId
output sharedKey string = sharedKeys.primarySharedKey

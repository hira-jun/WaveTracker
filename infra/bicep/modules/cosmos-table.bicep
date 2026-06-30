param accountName string
param location string
param tags object = {}
param offerType string = 'Standard'
param consistencyLevel string = 'Session'
param tableNames array = []

resource account 'Microsoft.DocumentDB/databaseAccounts@2023-04-15' = {
  name: accountName
  location: location
  tags: tags
  kind: 'GlobalDocumentDB'
  properties: {
    databaseAccountOfferType: offerType
    locations: [
      {
        locationName: location
        failoverPriority: 0
      }
    ]
    consistencyPolicy: {
      defaultConsistencyLevel: consistencyLevel
    }
    capabilities: [
      {
        name: 'EnableTable'
      }
    ]
    enableAutomaticFailover: false
    publicNetworkAccess: 'Enabled'
  }
}

resource tableService 'Microsoft.DocumentDB/databaseAccounts/tableServices@2023-04-15' = {
  parent: account
  name: 'default'
}

resource tables 'Microsoft.DocumentDB/databaseAccounts/tableServices/tables@2023-04-15' = [for tableName in tableNames: {
  parent: tableService
  name: tableName
  properties: {
    resource: {
      id: tableName
    }
    options: {}
  }
}]

var keys = account.listKeys()

output id string = account.id
output tableEndpoint string = account.properties.documentEndpoint
@secure()
output primaryKey string = keys.primaryMasterKey

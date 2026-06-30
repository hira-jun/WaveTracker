param appName string
param location string
param tags object = {}
param managedEnvironmentId string
param acrLoginServer string
param acrUsername string
@secure()
param acrPassword string
param imageName string
param imageTag string = 'latest'
param cpu string = '0.5'
param memory string = '1Gi'
param blobEndpoint string
param rawUploadsContainerName string
param floorMapsContainerName string
param cosmosTableEndpoint string
@secure()
param cosmosPrimaryKey string

resource app 'Microsoft.App/containerApps@2024-03-01' = {
  name: appName
  location: location
  tags: tags
  properties: {
    managedEnvironmentId: managedEnvironmentId
    configuration: {
      ingress: {
        external: true
        targetPort: 8000
        transport: 'auto'
      }
      registries: [
        {
          server: acrLoginServer
          username: acrUsername
          passwordSecretRef: 'acr-password'
        }
      ]
      secrets: [
        {
          name: 'acr-password'
          value: acrPassword
        }
        {
          name: 'cosmos-primary-key'
          value: cosmosPrimaryKey
        }
      ]
    }
    template: {
      containers: [
        {
          name: 'backend'
          image: '${acrLoginServer}/${imageName}:${imageTag}'
          env: [
            {
              name: 'API_PORT'
              value: '8000'
            }
            {
              name: 'WT_STORAGE_MODE'
              value: 'azure'
            }
            {
              name: 'WT_BLOB_ENDPOINT'
              value: blobEndpoint
            }
            {
              name: 'WT_BLOB_RAW_CONTAINER'
              value: rawUploadsContainerName
            }
            {
              name: 'WT_BLOB_FLOOR_MAP_CONTAINER'
              value: floorMapsContainerName
            }
            {
              name: 'WT_TABLE_ENDPOINT'
              value: cosmosTableEndpoint
            }
            {
              name: 'WT_TABLE_PRIMARY_KEY'
              secretRef: 'cosmos-primary-key'
            }
          ]
          resources: {
            cpu: json(cpu)
            memory: memory
          }
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 2
      }
    }
  }
}

output id string = app.id
output fqdn string = app.properties.configuration.ingress.fqdn
output httpsUrl string = 'https://${app.properties.configuration.ingress.fqdn}'

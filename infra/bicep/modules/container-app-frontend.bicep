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
param backendBaseUrl string

resource app 'Microsoft.App/containerApps@2024-03-01' = {
  name: appName
  location: location
  tags: tags
  properties: {
    managedEnvironmentId: managedEnvironmentId
    configuration: {
      ingress: {
        external: true
        targetPort: 3000
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
      ]
    }
    template: {
      containers: [
        {
          name: 'frontend'
          image: '${acrLoginServer}/${imageName}:${imageTag}'
          env: [
            {
              name: 'VITE_API_BASE_URL'
              value: backendBaseUrl
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

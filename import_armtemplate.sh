#!/bin/bash

# Define parameters as JSON string
parameters='{"servers_infosys_name": {"value": "mytrion-com-server"}, "vulnerabilityAssessments_Default_storageContainerPath": {"value": ""}, "adminPassword": {"value": "trion$321!trion"}}'

# Check if storage account name, container name, template file name, and resource group name are provided
if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ] || [ -z "$4" ]; then
    echo "Usage: $0 <storage_account_name> <container_name> <template_file_name> <resource_group_name>"
    exit 1
fi

storage_account_name="$1"
container_name="$2"
template_file_name="$3"
resource_group_name="$4"

# Get storage account key
storage_account_key=$(az storage account keys list --account-name $storage_account_name --query "[0].value" -o tsv)

# Get SAS token for container
sas_token=$(az storage container generate-sas --account-name $storage_account_name --name $container_name --permissions acdlrw --expiry $(date -u -d "1 day" '+%Y-%m-%dT%H:%MZ') --key $storage_account_key --output tsv)

# Deploy template with parameters
az deployment group create --resource-group $resource_group_name --template-uri "https://$storage_account_name.blob.core.windows.net/$container_name/$template_file_name?$sas_token" --parameters "$parameters"

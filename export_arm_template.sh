#!/bin/bash

# Check if template_name and resource_group_name arguments are provided
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: $0 <template_name> <resource_group_name>"
    exit 1
fi

template_name="$1"
resource_group_name="$2"
template_file="${template_name}.json"

# Export template
az  group export --resource-group infosys_com_resourcegroup > $template_file

# Upload template to Azure Storage container
az storage blob upload --account-name warrioracc --container-name red --file $template_file --name $template_file

# Remove the downloaded JSON file
rm $template_file

# Create a new resource group
az group create --name $resource_group_name --location eastus

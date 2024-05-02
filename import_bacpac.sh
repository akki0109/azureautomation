#!/bin/bash

# Check if all required arguments are provided
if [ $# -ne 6 ]; then
    echo "Usage: $0 <resourceGroup> <storageAccount> <server> <database> <userId> <password>"
    exit 1
fi

# Assign command-line arguments to variables
resourceGroup=$1
storageAccount=$2
server=$3
database=$4
userId=$5
password=$6

# Get the storage account key
storageAccountKey=$(az storage account keys list --resource-group "$resourceGroup" --account-name "$storageAccount" --query "[0].value" -o tsv)

# Run the SQL database import command
az sql db import --resource-group "$resourceGroup" --server "$server" --name "$database" --storage-key-type "StorageAccessKey" --storage-key "$storageAccountKey" --storage-uri "https://$storageAccount.blob.core.windows.net/importsample/sample.bacpac" -u "$userId" -p "$password"

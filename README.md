# Exporting ARM Template of Master Resource Group to Azure Storage Blob and Create New Resource Group
./export_arm_template.sh <template_name> <resource_group_name>

# For Modifying Blob ARM Template
bash python arm_modify.py "connection_string_here" "container_name_here" "blob_name_here"

# Importing ARM Template
./script.sh <storage_account_name> <container_name> <template_file_name> <resource_group_name>

# Exporting BACPAC in Azure Blob
.\export_bacpak.ps1 -resourceGroupSQL "your_resource_group" -resourceGroupStorage "your_storage_group" -sqlServer "your_sql_server" -sqlUsername "your_username" -sqlPassword "your_password" -databaseName "your_database" -storageAccount "your_storage_account" -containerName "your_container_name"

# Importing BACPAC in Resource Group Created Earlier with an Existing Database
./import_bacpac.sh resourceGroup storageAccount server database userId password


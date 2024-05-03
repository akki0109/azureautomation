# Exporting ARM Template of Master Resource Group to Azure Storage Blob and Create New Resource Group
# account-name && --container-name && export resorcegroup name is static because all are one time defination quantity for whole lifecycle and will never change.
./export_arm_template.sh <template_name> <resource_group_name>

# For Modifying Blob ARM Template
 python arm_modify.py "connection_string_here" "container_name_here" "blob_name_here"

# Importing ARM Template
./import_armtemplate.sh <storage_account_name> <container_name> <template_file_name> <resource_group_name>

# Exporting BACPAC in Azure Blob
.\export_bacpak.ps1 -resourceGroupSQL "your_resource_group" -resourceGroupStorage "your_storage_group" -sqlServer "your_sql_server" -sqlUsername "your_username" -sqlPassword "your_password" -databaseName "your_database" -storageAccount "your_storage_account" -containerName "your_container_name"

# Importing BACPAC in Resource Group Created Earlier with an Existing Database
./import_bacpac.sh resourceGroup storageAccount server database userId password


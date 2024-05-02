param (
    [string]$resourceGroupSQL,
    [string]$resourceGroupStorage,
    [string]$sqlServer,
    [string]$sqlUsername,
    [string]$sqlPassword,
    [string]$databaseName,
    [string]$storageAccount,
    [string]$containerName
)

Import-Module Az

Connect-AzAccount

# You don't need to change the next lines
$bacpacFilename = (Get-Date).ToString("yyyy-MM-dd-HH-mm") + ".bacpac"
$storageKeyType = "StorageAccessKey"
$storageKey = (Get-AzStorageAccountKey -ResourceGroupName $resourceGroupStorage -AccountName $storageAccount) | Where-Object { $_.KeyName -eq "key2" }
$copyDatabaseName = (Get-Date).ToString("yyyyMMddHHmmss") + "-" + $databaseName
$bacpacFilename = (Get-Date).ToString("yyyy-MM-dd") + "-" + $copyDatabaseName + ".bacpac"
$baseStorageUri = "https://" + $storageAccount + ".blob.core.windows.net"
$bacpacUri = $baseStorageUri + "/" + $containerName + "/" + $bacpacFilename

# Copy database
Write-Host "Copying" $databaseName "to" $copyDatabaseName
New-AzSqlDatabaseCopy -ResourceGroupName $resourceGroupSQL -ServerName $sqlServer -DatabaseName $databaseName -CopyResourceGroupName $resourceGroupSQL -CopyServerName $sqlServer -CopyDatabaseName $copyDatabaseName
Write-Host "Copy completed"

# Export database
Write-Host "Exporting" $copyDatabaseName "to" $bacpacUri
$exportRequest = New-AzSqlDatabaseExport -ResourceGroupName $resourceGroupSQL -ServerName $sqlServer -DatabaseName $copyDatabaseName -StorageKeyType "StorageAccessKey" -StorageKey $storageKey.Value -StorageUri $bacpacUri -AdministratorLogin $sqlUsername -AdministratorLoginPassword $sqlPassword
$exportRequest
$exportStatus = Get-AzSqlDatabaseImportExportStatus -OperationStatusLink $exportRequest.OperationStatusLink
while ($exportStatus.Status -eq "InProgress")
{
    Start-Sleep -s 10
    $exportStatus = Get-AzSqlDatabaseImportExportStatus -OperationStatusLink $exportRequest.OperationStatusLink
}

# Remove the copied database
Remove-AzSqlDatabase -ResourceGroupName $resourceGroupSQL -ServerName $sqlServer -DatabaseName $copyDatabaseName

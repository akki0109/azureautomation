import logging
import json
import argparse
from azure.storage.blob import BlobServiceClient

def download_blob(storage_connection_string, container_name, blob_name):
    blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    blob_content = blob_client.download_blob().content_as_text()
    return blob_content

def upload_blob(storage_connection_string, container_name, blob_name, content):
    blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    blob_client.upload_blob(content, overwrite=True)

def main(storage_connection_string, container_name, blob_name):
    # Download the blob content from Azure Blob Storage
    blob_content = download_blob(storage_connection_string, container_name, blob_name)

    logging.info(f"Blob trigger function processed blob\n"
                 f"Blob Content: {blob_content}")

    # Parse the JSON content into a Python dictionary
    template = json.loads(blob_content)

    # Add adminPassword parameter to the parameters section
    if 'parameters' not in template:
        template['parameters'] = {}
    template['parameters']['adminPassword'] = {
        "type": "securestring",
        "metadata": {
            "description": "The administrator password for the SQL server."
        }
    }

    # Update the administratorLoginPassword property in the resource section properties
    if 'resources' in template:
        for resource in template['resources']:
            if 'properties' in resource and 'administratorLogin' in resource['properties']:
                properties = resource['properties']
                # Add the administratorLoginPassword property
                properties['administratorLoginPassword'] = "[parameters('adminPassword')]"

    # Serialize the modified template back to JSON
    modified_blob_content = json.dumps(template)

    # Upload the modified content back to Azure Blob Storage
    upload_blob(storage_connection_string, container_name, blob_name, modified_blob_content)

    logging.info(f"Modified Blob Content uploaded to {container_name}/{blob_name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process Azure Blob Storage parameters.')
    parser.add_argument('connection_string', type=str, help='Azure Blob Storage connection string')
    parser.add_argument('container_name', type=str, help='Azure Blob Storage container name')
    parser.add_argument('blob_name', type=str, help='Azure Blob Storage blob name')
    args = parser.parse_args()

    # Call the main function to modify the template
    main(args.connection_string, args.container_name, args.blob_name)

import logging
import json
import os
from azure.storage.blob import BlobServiceClient
import azure.functions as func

def download_blob(storage_connection_string, container_name, blob_name):
    blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    blob_content = blob_client.download_blob().readall()
    return blob_content

def upload_blob(storage_connection_string, container_name, blob_name, content):
    blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    blob_client.upload_blob(content, overwrite=True)

def modify_template(blob_content):
    try:
        template = json.loads(blob_content)
        if 'parameters' not in template:
            template['parameters'] = {}

        template['parameters']['database_name'] = {
            "type": "string",
            "metadata": {
                "description": "The name of the database."
            }
        }

        template['parameters']['adminPassword'] = {
            "type": "securestring",
            "metadata": {
                "description": "The administrator password for the SQL server."
            }
        }

        template['parameters']['administratorLogin'] = {
            "type": "string",
            "metadata": {
                "description": "The administrator login for the SQL server."
            }
        }

        if 'resources' in template:
            for resource in template['resources']:
                if 'name' in resource:
                    resource_name = resource['name']
                    start_index = resource_name.find('TrionDB')
                    end_index = start_index + len('TrionDB')
                    resource['name'] = resource_name[:start_index] + "[parameters('database_name')]" + resource_name[end_index:]
                if 'properties' in resource:
                    properties = resource['properties']
                    if 'administratorLogin' in properties:
                        properties['administratorLogin'] = "[parameters('administratorLogin')]"
                        if 'administratorLoginPassword' not in properties:
                            properties['administratorLoginPassword'] = "[parameters('adminPassword')]"

        return json.dumps(template)
    except Exception as e:
        logging.error(f"Error modifying template: {e}")
        return None

def main(myblob: func.InputStream):
    storage_connection_string = os.getenv('trion_STORAGE')
    logging.info(f"Blob trigger function processed blob\n"
                 f"Blob Size: {myblob.length} bytes")

    blob_name = myblob.name.split('/')[-1]
    if blob_name.endswith('.json'):
        blob_content = myblob.read().decode('utf-8')
        logging.info(f"Blob Content: {blob_content}")

        modified_template = modify_template(blob_content)
        if modified_template:
            upload_blob(storage_connection_string, "newarm", blob_name, modified_template)
            logging.info("Modified Blob Content uploaded")
        else:
            logging.error("Failed to modify template")
    else:
        logging.warning(f"Blob {blob_name} does not have a .json extension, skipping processing")

if __name__ == '__main__':
    app = func.WorkerApp()

    # Define your trigger function and bind it to blobs with .json extension in the arm container
    @app.blob_trigger(name="BlobTrigger2", path="arm/{name}", connection="trion_STORAGE")
    def BlobTrigger2(myblob: func.InputStream):
        main(myblob)

    app.run()

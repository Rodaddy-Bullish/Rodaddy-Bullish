from __future__ import annotations

import os

from google.cloud import secretmanager


def create_secret(project_id: str = 'atoms-b1fs-scratch-3ab6',
                  secret_id: str | bool = None,
                  ) -> str | bool | None:

    return_value = None

    if not secret_id:
        client = secretmanager.SecretManagerServiceClient()
        project_detail = f"projects/{project_id}"
        
        response = client.create_secret(
            request={
                "parent": project_detail,
                "secret_id": secret_id,
                "secret": {"replication": {"automatic": {}}},
            }
        )
        
        return_value = response.payload.data.decode("UTF-8")
        
        return return_value
    
    else:
        raise ValueError("Secret ID cannot be None")


def access_secret(project_id: str = 'atoms-b1fs-scratch-3ab6',
                  secret_id: str = "scratch_telegram_demo_secrets",
                  version_id: str = "latest") -> str:

    from google.cloud import secretmanager
    secret_client = secretmanager.SecretManagerServiceClient()
    project_detail = f"projects/{project_id}"
    secret_full_name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    print(f"Parent: {project_detail} \n Secret name: {secret_full_name}")
    
    response = secret_client.access_secret_version(name=secret_full_name)
    my_secret_value = response.payload.data.decode("UTF-8")
    return my_secret_value


def write_file_to_bucket(project_id: str = 'atoms-b1fs-scratch-3ab6',
                         bucket_name: str = 'scratch_telegram_demo',
                         source_file_name: str = 'test.txt',
                         destination_file_name: str | bool = None
                         ) -> bool:
    
    from google.cloud import storage
    
    if not destination_file_name:
        destination_file_name = source_file_name
    
    storage_client = storage.Client()
    
    bucket = storage_client.bucket(bucket_name)
    upload_object = bucket.blob(source_file_name)
    upload_object.upload_from_filename(destination_file_name)
    
    print(f"File {source_file_name} uploaded to {destination_file_name} in bucket {bucket_name}")
    return True
    

def main():
    project_id = "atoms-b1fs-scratch-3ab6"
    secret_id = "scratch_telegram_demo_secrets"
    
    secret: str = access_secret(project_id, secret_id)
    print(f"Secret: {secret}")


if __name__ == '__main__':
    main()

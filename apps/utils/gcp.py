import io
import traceback
import datetime

from google.cloud import storage


class GCP_UTIL:
    def __init__(self, credential_path):
        self.credentials = credential_path

    def upload_storage(self, bucket, path, data):
        if self.credentials is None:
            gcs = storage.Client()
        else:
            gcs = storage.Client.from_service_account_json(self.credentials)
        bucket = gcs.get_bucket(bucket)

        blob = bucket.blob(path)
        if isinstance(data, str):
            blob.upload_from_string(data, content_type='text/plain; charset=utf-8')
        elif isinstance(data, io.IOBase):
            blob.upload_from_file(data)
        else:
            try:
                blob.upload_from_string(data)
            except Exception as e:
                print('not defined file type: {type(data)}')
                print(traceback.format_exc())
                raise e
        
        return blob.path

    def download_storage_to_bytes(self, bucket, path):
        if self.credentials is None:
            gcs = storage.Client()
        else:
            gcs = storage.Client.from_service_account_json(self.credentials)
        bucket = gcs.get_bucket(bucket)

        blob = bucket.blob(path)
        bt = blob.download_as_bytes()

        return bt

    
    def generate_signed_url(self, bucket, path, expiration_hour=1):
        if self.credentials is None:
            gcs = storage.Client()
        else:
            gcs = storage.Client.from_service_account_json(self.credentials)
        bucket = gcs.get_bucket(bucket)

        blob = bucket.blob(path)
        url = blob.generate_signed_url(
            # version='v4', 
            expiration=datetime.timedelta(hours=expiration_hour), 
            method='GET')
        return url

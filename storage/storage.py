from azure.storage.blob import BlobServiceClient


class Storage:
    storage_instance = None

    def __init__(self):
        self.connect_str = 'DefaultEndpointsProtocol=https;AccountName=tema4cc;AccountKey=ut+pLmXCx+XDL7ALSGAeKuYxzbI0vBrNgZgs6qaXRxyOj/DcaVEqVD0DaZ51XkmiuLmrK6C2Cjne9p66cCo2cg==;EndpointSuffix=core.windows.net'
        self.container_name = 'images'
        self.blob_service_client, self.container_client = self.connect()

    @staticmethod
    def storage():
        if Storage.storage_instance is None:
            Storage.storage_instance = Storage()

        return Storage.storage_instance

    def connect(self):
        blob_service_client = BlobServiceClient.from_connection_string(
            conn_str=self.connect_str)
        try:
            container_client = blob_service_client.get_container_client(
                container=self.container_name)
            container_client.get_container_properties()
        except Exception as e:
            print("Creating container...")
            container_client = blob_service_client.create_container(self.container_name)

        return blob_service_client, container_client

    def upload_file(self, file):
        try:
            self.container_client.upload_blob(file.filename,
                                              file)
        except Exception as e:
            print("Ignoring duplicate filenames")


if __name__ == '__main__':
    pass

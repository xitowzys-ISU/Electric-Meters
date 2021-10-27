import owncloud
import urllib


class OwnCloudAPI:
    def __init__(self, host: str, id_private_storage: str, id_public_storage, password_private_storage: str) -> None:
        self.__host: str = host
        self.__id_private_storage = id_private_storage
        self.__id_public_storage = id_public_storage
        self.__password_private_storage = password_private_storage

        self.__oc = owncloud.Client.from_public_link(f"{host}index.php/s/{self.__id_private_storage}",
                                                     folder_password=self.__password_private_storage)

    def push_file(self, name_file, path_file):
        if self.__oc.drop_file(path_file):
            url = f"{self.__host}index.php/s/{self.__id_public_storage}/download?path=%2F&files={urllib.parse.quote_plus(name_file)}"
            return url

    def get_download_url(self, name_file):
        return f"{self.__host}index.php/s/{self.__id_public_storage}/download?path=%2F&files={urllib.parse.quote_plus(name_file)}.jpg"

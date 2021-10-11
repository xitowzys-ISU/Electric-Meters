import boto3
import botocore.exceptions
import requests
from core import YandexToloka


class YandexObjectStorage:
    def __init__(self,
                 aws_secret_access_key: str,
                 aws_access_key_id: str,
                 yandex_object_storage_bucket: str
                 ) -> None:
        self.__AWS_SECRET_ACCESS_KEY: str = aws_secret_access_key
        self.__AWS_ACCESS_KEY_ID: str = aws_access_key_id
        self.__YANDEX_OBJECT_STORAGE_BUCKET: str = yandex_object_storage_bucket
        self.__endpoint_url: str = "https://storage.yandexcloud.net"

    def load_image_on_yandex_storage(self, yt: "YandexToloka", img_id: str) -> str:
        """Cкачивает изображение из задания, загружает
        в Yandex Object Storage и возвращает ссылку на изображение

        :param yt: Объект класса YandexToloka
        :param img_id: id изображения

        :return: Ссылка на изображение
        """
        session = boto3.session.Session(
            aws_secret_access_key=self.__AWS_SECRET_ACCESS_KEY,
            aws_access_key_id=self.__AWS_ACCESS_KEY_ID
        )

        s3 = session.client(service_name="s3", endpoint_url=self.__endpoint_url)

        file = requests.get(f"{yt.get_url_api()}attachments/{img_id}/download", headers=yt.get_header())

        try:
            s3.put_object(Bucket=self.__YANDEX_OBJECT_STORAGE_BUCKET, Key=img_id, Body=file.content)
        except botocore.exceptions.ClientError as e:
            raise Exception("Ошибка подписки. Проверьте ключ, id и Bucket на подлинность.")

        return f"https://storage.yandexcloud.net/{self.__YANDEX_OBJECT_STORAGE_BUCKET}/{img_id}"

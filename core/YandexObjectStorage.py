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
        self.AWS_SECRET_ACCESS_KEY = aws_secret_access_key
        self.AWS_ACCESS_KEY_ID = aws_access_key_id
        self.YANDEX_OBJECT_STORAGE_BUCKET = yandex_object_storage_bucket

    def load_image_on_yandex_storage(self, yt: "YandexToloka" ,img_id: str) -> str:
        '''Cкачивает изображение из задания, загружает
        в Yandex Object Storage и возвращает ссылку на изображение

        :param yt: Объект класса YandexToloka
        :param img_id: id изображения

        :return: Ссылка на изображение
        '''
        session = boto3.session.Session(
            aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY,
            aws_access_key_id=self.AWS_ACCESS_KEY_ID
        )
        s3 = session.client(
            service_name="s3", endpoint_url="https://storage.yandexcloud.net"
        )

        file = requests.get(
            url=yt.URL_API + "attachments/%s/download" % img_id, headers=yt.HEADERS
        )

        url = yt.URL_API + "attachments/%s/download" % img_id

        try:
            s3.put_object(Bucket=self.YANDEX_OBJECT_STORAGE_BUCKET, Key=img_id, Body=file.content)
        except botocore.exceptions.ClientError as e:
            raise Exception("Ошибка подписки. Проверьте ключ, id и Bucket на подлинность.")

        return "https://storage.yandexcloud.net/schetchiki/%s" % img_id

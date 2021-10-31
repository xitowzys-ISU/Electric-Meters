import requests


class YandexToloka:
    def __init__(self, pool_id: int, toloka_oauth_token: str) -> None:
        self.__TOLOKA_OAUTH_TOKEN: str = toloka_oauth_token
        self.__pool_id: int = pool_id
        self.__url_api: str = "https://toloka.yandex.ru/api/v1/"
        self.__header = {
            "Authorization": f"OAuth {toloka_oauth_token}",
            "Content-Type": "application/JSON",
        }

    def get_all_submitted_tasks(self) -> str:
        """
        Получаем список всех заданий из пула, которые ждут проверки

        :return: json список
        """

        url_assignments = f"{self.__url_api}assignments/?status=SUBMITTED&limit=10000&pool_id={self.__pool_id}"

        return requests.get(url_assignments, headers=self.__header).json()["items"]

    def get_all_accepted_tasks(self) -> str:
        """
        Получаем список всех заданий из пула, которые приняты

        :return: json список
        """

        url_assignments = f"{self.__url_api}assignments/?status=ACCEPTED&limit=10000&pool_id={self.__pool_id}"

        return requests.get(url_assignments, headers=self.__header).json()["items"]

    def get_all_tasks(self) -> list:
        """
        Получаем список всех заданий

        :return: json список
        """

        url_assignments = f"{self.__url_api}tasks/?limit=10000&pool_id={self.__pool_id}"

        return requests.get(url_assignments, headers=self.__header).json()["items"]

    def upload_task_pool(self, json: list):
        """
        Загрузить задания в пул

        :return: json
        """
        return requests.post(url=self.__url_api + "tasks", headers=self.__header, json=json).json()

    def patch_task(self, task_id, json):
        url = f"{self.__url_api}assignments/{task_id}"
        return requests.patch(url, headers=self.__header, json=json)

    def get_header(self):
        """
        Получить header

        :return: header
        """
        return self.__header

    def set_pool__id(self, pool_id: int):
        """ Задать новый pool ID """
        self.__pool_id = pool_id

    def get_pool_id(self) -> int:
        """
        Получить id пула

        :return: id пула
        """
        return self.__pool_id

    def set_url_api(self, url_api: str) -> None:
        """ Задать новый URL API """
        self.__url_api = url_api

    def get_url_api(self):
        return self.__url_api

    def get_image(self, img_id):
        return requests.get(f"{self.__url_api}attachments/{img_id}/download", headers=self.__header)

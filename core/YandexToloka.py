import requests


class YandexToloka:
    def __init__(self, pool_id: int, toloka_oauth_token: str) -> None:
        self.__TOLOKA_OAUTH_TOKEN = toloka_oauth_token
        self.__POOL_ID = pool_id
        self.URL_API = "https://toloka.yandex.ru/api/v1/"
        self.HEADERS = {
            "Authorization": "OAuth %s" % toloka_oauth_token,
            "Content-Type": "application/JSON",
        }

    def get_all_submitted_tasks(self) -> str:
        """
        Получаем список всех заданий из пула, которые ждут проверки

        :return: json список
        """

        url_assignments = (
                self.URL_API + "assignments/?status=SUBMITTED&limit=10000&pool_id=%s" % self.__POOL_ID
        )

        return requests.get(url_assignments, headers=self.HEADERS).json()["items"]

    def get_pool_id(self) -> int:
        """
        Получить id пула

        :return: id пула
        """
        return self.__POOL_ID



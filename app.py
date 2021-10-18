import colorama

from consolemenu import *
from consolemenu.items import *

from core import YandexToloka, OwnCloudAPI

from loader import process_first_pool, process_second_pool

from config import TOLOKA_OAUTH_TOKEN
from config import OWN_CLOUD_PASSWORD_PRIVATE_STORAGE
from config import OWN_CLOUD_HOST, OWN_CLOUD_ID_PUBLIC_STORAGE, OWN_CLOUD_ID_PRIVATE_STORAGE

colorama.init()

POOL_ID_FIRST = 28738984
POOL_ID_SECOND = 28545280

YT_POOL_1 = YandexToloka(POOL_ID_FIRST, TOLOKA_OAUTH_TOKEN)
YT_POOL_2 = YandexToloka(POOL_ID_SECOND, TOLOKA_OAUTH_TOKEN)
OC = OwnCloudAPI(OWN_CLOUD_HOST, OWN_CLOUD_ID_PRIVATE_STORAGE, OWN_CLOUD_ID_PUBLIC_STORAGE,
                 OWN_CLOUD_PASSWORD_PRIVATE_STORAGE)


def start_process_first_pool() -> None:
    process_first_pool(YT_POOL_1, YT_POOL_2, OC)


if __name__ == '__main__':
    menu = ConsoleMenu("Yandex-Toloko", "Скрипт для автомизации получение готового датасета счетчиков")

    function_item = FunctionItem("Выгрузить все из 1 пула и создать готовый 2 пул", start_process_first_pool)

    menu.append_item(function_item)
    menu.show()
    # main()

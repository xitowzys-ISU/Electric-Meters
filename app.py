import colorama

from consolemenu import *
from consolemenu.items import *

from core import YandexToloka, OwnCloudAPI

from loader import process_first_pool, process_second_pool

from config import TOLOKA_OAUTH_TOKEN
from config import OWN_CLOUD_PASSWORD_PRIVATE_STORAGE
from config import OWN_CLOUD_HOST, OWN_CLOUD_ID_PUBLIC_STORAGE, OWN_CLOUD_ID_PRIVATE_STORAGE

colorama.init(autoreset=True)

POOL_ID_FIRST = 28984579
POOL_ID_SECOND = 28992557 #  29000040

YT_POOL_1 = YandexToloka(POOL_ID_FIRST, TOLOKA_OAUTH_TOKEN)
YT_POOL_2 = YandexToloka(POOL_ID_SECOND, TOLOKA_OAUTH_TOKEN)
OC = OwnCloudAPI(OWN_CLOUD_HOST, OWN_CLOUD_ID_PRIVATE_STORAGE, OWN_CLOUD_ID_PUBLIC_STORAGE,
                 OWN_CLOUD_PASSWORD_PRIVATE_STORAGE)


def start_process_first_pool() -> None:
    process_first_pool(yt_pool_1=YT_POOL_1, yt_pool_2=YT_POOL_2, oc=OC)


def start_process_second_pool() -> None:
    process_second_pool(
        path="./data/211026_190505_28984579_28992557_data.json",
        yt_pool_2=YT_POOL_2
    )


if __name__ == '__main__':
    menu = ConsoleMenu("Yandex-Toloko", "Скрипт для автомизации получение готового датасета счетчиков")

    start_first_pool = FunctionItem("Обработка первого пула и загрузка во второй пул", start_process_first_pool)
    start_second_pool = FunctionItem("Обработать данные из второго пула и оплатить первый пул", start_process_second_pool)

    menu.append_item(start_first_pool)
    menu.append_item(start_second_pool)
    menu.show()

    # start_process_first_pool()
    # start_process_second_pool()

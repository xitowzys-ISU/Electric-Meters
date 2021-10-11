from typing import Any, Union

import os
import json
import colorama
from tqdm import tqdm

from config import TOLOKA_OAUTH_TOKEN
from config import AWS_SECRET_ACCESS_KEY
from config import AWS_ACCESS_KEY_ID
from config import YANDEX_OBJECT_STORAGE_BUCKET
from core import YandexToloka, YandexObjectStorage


def parse_data_first_pool(submitted_tasks: str, YT_POOL_1: "YandexToloka", POOL_2_ID: int,
                          YOS: "YandexObjectStorage") -> tuple[
    dict[str, Any], list[dict[str, Union[dict[str, str], YandexToloka, int]]]]:
    """
    Парсинг данных полученных из 1 пула

    :param submitted_tasks: Список заданий из пула
    :param YT_POOL_1: Первый пул, где приминаем фотографии
    :param YT_POOL_2: Второй пул, где проверяются фотографии и размечают область циферблата
    :return:
    """

    # Заводим словари, чтобы помнить, как соотносятся id задания из первого пула и id задания из второго пула
    url_to_first_id_map: dict = {}
    json_second_task: list = []

    for task in tqdm(submitted_tasks):
        first_task_id = task["id"]
        img_id = task["solutions"][0]["output_values"]["img"]
        url_img = YOS.load_image_on_yandex_storage(YT_POOL_1, img_id)
        url_to_first_id_map[url_img] = first_task_id
        json_second_task.append(
            {"input_values": {"image": url_img}, "pool_id": POOL_2_ID, "overlap": 5}
        )

    return url_to_first_id_map, json_second_task


def process_first_pool(pool_id_first: int, pool_id_second: int) -> None:
    YT_POOL_1 = YandexToloka(pool_id_first, TOLOKA_OAUTH_TOKEN)
    YT_POOL_2 = YandexToloka(pool_id_second, TOLOKA_OAUTH_TOKEN)
    YOS = YandexObjectStorage(AWS_SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID, YANDEX_OBJECT_STORAGE_BUCKET)

    submitted_tasks = YT_POOL_1.get_all_submitted_tasks()

    """
    Для каждого задания из первого пула:
        * Запоминаем его id
        * Загружаем картинку в Yandex Object Storage
        * Оборачиваем параметры в json для второго задания
    """
    print(f"{colorama.Fore.YELLOW}Загрузка картинок в {colorama.Fore.RED}Yandex Object Storage:")
    url_to_first_id_map, json_second_task = parse_data_first_pool(submitted_tasks, YT_POOL_1,
                                                                  YT_POOL_2.get_pool_id(),
                                                                  YOS)

    second_tasks_request = YT_POOL_2.upload_task_pool(json_second_task)

    print(f"{colorama.Fore.YELLOW}Загрузка заданий в пул {pool_id_second}")
    print(f"{colorama.Fore.GREEN}Загрузка прошла успешно")

    first_id_to_second_id_map = {}
    # В ответ нам выдали id вторых заданий.
    # По ним мы сможем запросить ответы после завершения задания, поэтому запомним их
    for second_task in second_tasks_request["items"].values():
        second_task_id = second_task["id"]
        img_url = second_task["input_values"]["image"]
        first_task_id = url_to_first_id_map[img_url]
        first_id_to_second_id_map[first_task_id] = second_task_id

    if not os.path.exists("./data"):
        os.makedirs("./data")

    with open('./data/data.json', 'w') as f:
        json.dump(first_id_to_second_id_map, f, indent=4)


def start() -> None:
    colorama.init()

    POOL_ID_FIRST = 28420385
    POOL_ID_SECOND = 28545280

    process_first_pool(POOL_ID_FIRST, POOL_ID_SECOND)

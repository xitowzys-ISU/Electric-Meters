from typing import Any, Union

import os
import json
import time
import colorama
from tqdm import tqdm
import numpy as np
import pandas as pd

from config import OWN_CLOUD_HOST, OWN_CLOUD_ID_PUBLIC_STORAGE, OWN_CLOUD_ID_PRIVATE_STORAGE
from config import OWN_CLOUD_PASSWORD_PRIVATE_STORAGE
from config import TOLOKA_OAUTH_TOKEN

from core import YandexToloka, OwnCloudAPI


def parse_data_first_pool(submitted_tasks: str, YT_POOL_1: "YandexToloka", POOL_2_ID: int,
                          OC: "OwnCloudAPI") -> tuple[
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

    for task in tqdm(submitted_tasks[:5]):
        first_task_id = task["id"]
        img_id = task["solutions"][0]["output_values"]["img"]

        image = YT_POOL_1.get_image(img_id)
        out = open(f"./tmp/{img_id}.jpg", 'wb')
        out.write(image.content)
        out.close()

        url_img = OC.push_file(f"{img_id}.jpg", f"./tmp/{img_id}.jpg")
        os.remove(f"./tmp/{img_id}.jpg")


        url_to_first_id_map[url_img] = first_task_id
        json_second_task.append(
            {"input_values": {"image": url_img}, "pool_id": POOL_2_ID, "overlap": 5}
        )

    return url_to_first_id_map, json_second_task


def process_first_pool(yt_pool_1: "YandexToloka", yt_pool_2: "YandexToloka", oc: "OwnCloudAPI") -> None:
    submitted_tasks = yt_pool_1.get_all_submitted_tasks()

    submitted_tasks2 = yt_pool_2.get_all_tasks()

    if yt_pool_2.get_all_tasks():
        print(f"{colorama.Fore.RED}Во 2 пуле уже есть задание. Удалите их и запустите заного")
        time.sleep(5)
        return


    """
    Для каждого задания из первого пула:
        * Запоминаем его id
        * Загружаем картинку в Yandex Object Storage
        * Оборачиваем параметры в json для второго задания
    """
    print(f"{colorama.Fore.YELLOW}Загрузка картинок в {colorama.Fore.RED}Yandex Object Storage:")
    url_to_first_id_map, json_second_task = parse_data_first_pool(submitted_tasks, yt_pool_1,
                                                                  yt_pool_2.get_pool_id(),
                                                                  oc)

    second_tasks_request = yt_pool_2.upload_task_pool(json_second_task)

    print(f"{colorama.Fore.YELLOW}Загрузка заданий в пул {yt_pool_2.get_pool_id()}")
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

    time.sleep(5)


def is_training_tasks(tasks: list, task_id: str) -> bool:
    """Проверить является ли задание тренировочным

    :return: bool
    """
    for k in tasks:
        if k['id'] == task_id:
            if "known_solutions" in k:
                return True
            else:
                return False


def parse_training_tasks(find: str, tasks: list, task_id: str):
    for k in tasks:
        if k['id'] == task_id:
            return k['known_solutions'][0]["output_values"][find]


def unknown_fun(k, second_task_id, second_task):
    return list(map(lambda t: t['solutions'][
        np.where(np.array(list(map(lambda x: x['id'], t['tasks']))) == second_task_id)[0][0]]['output_values'][k],
                    second_task))


def process_second_pool(path: str, yt_pool_1: "YandexToloka", yt_pool_2: "YandexToloka") -> None:
    db = []

    with open(path, "r", encoding='utf-8') as f:
        first_id_to_second_id_map = json.load(f)

    # Меняем ключ значение местами
    first_id_to_second_id_map = {v: k for k, v in first_id_to_second_id_map.items()}

    tasks = yt_pool_2.get_all_tasks()
    second_tasks = yt_pool_2.get_all_accepted_tasks()

    print("------------------------------------------")

    for first_task_id in tqdm(first_id_to_second_id_map):
        second_task_id = first_id_to_second_id_map[first_task_id]

        if not is_training_tasks(tasks, second_task_id):
            # Получаем вектор ответов пользователей
            value_list = unknown_fun("value", second_task_id, second_tasks)
            check_count_list = unknown_fun("check_count", second_task_id, second_tasks)
            check_quality_list = unknown_fun("check_quality", second_task_id, second_tasks)

            if np.sum(check_count_list) < 3:
                print(second_task_id)
                print("На фотографии должен быть ровно один счетчик")
                json_check = {
                    "status": "REJECTED",
                    "public_comment": "На фотографии должен быть ровно один счетчик холодной либо горячей воды",
                }
                # Если больше двух людей сказали, что показания не видны, отклоняем задание
            elif np.sum(check_quality_list) < 3:
                print(second_task_id)
                print("Показания на счетчике отчетливо не видны")
                json_check = {
                    "status": "REJECTED",
                    "public_comment": "Показания на счетчике отчетливо не видны",
                }
                # В остальных случаях принимаем задание
            else:
                print(second_task_id)
                print("Изображение счетчика принято")
                json_check = {
                    "status": "ACCEPTED",
                    "public_comment": "Изображение счетчика принято",
                }

            # Найдем для принятых заданий самый частый ответ
            (values, counts) = np.unique(value_list, return_counts=True)
            ind = np.argmax(counts)
            value = values[ind]
            if json_check["status"] == "ACCEPTED":
                (values, counts) = np.unique(check_count_list, return_counts=True)
                ind = np.argmax(counts)
                check_count = values[ind]

                (values, counts) = np.unique(check_quality_list, return_counts=True)
                ind = np.argmax(counts)
                check_quality = values[ind]

                print(
                    "Показания счетчика: %s. Его подтвердили %d из 5 пользователей"
                    % (value, counts[ind])
                )

            print("------------------------------------------")
        else:
            value = parse_training_tasks("value", tasks, second_task_id)
            check_count = parse_training_tasks("check_count", tasks, second_task_id)
            check_quality = parse_training_tasks("check_quality", tasks, second_task_id)

            if not check_count:
                print(second_task_id)
                print("На фотографии должен быть ровно один счетчик")
                json_check = {
                    "status": "REJECTED",
                    "public_comment": "На фотографии должен быть ровно один счетчик холодной либо горячей воды",
                }
                # Если больше двух людей сказали, что показания не видны, отклоняем задание
            elif not check_quality:
                print(second_task_id)
                print("Показания на счетчике отчетливо не видны")
                json_check = {
                    "status": "REJECTED",
                    "public_comment": "Показания на счетчике отчетливо не видны",
                }
                # В остальных случаях принимаем задание
            else:
                print(second_task_id)
                print("Изображение счетчика принято")
                json_check = {
                    "status": "ACCEPTED",
                    "public_comment": "Изображение счетчика принято",
                }

            if json_check["status"] == "ACCEPTED":
                value_list, check_count_list, check_quality_list = [], [], []
                print(
                    "Показания счетчика: %s. Тренировочное задание"
                    % value
                )

            print("------------------------------------------")

        if json_check["status"] == "ACCEPTED":
            db.append(
                {
                    "first_task_id": first_task_id,
                    "second_task_id": second_task_id,
                    "url_img": first_id_to_second_id_map[first_task_id],
                    "check_count_list": check_count_list,
                    "check_quality_list": check_quality_list,
                    "value_list": value_list,
                    "check_count": check_count,
                    "check_quality": check_quality,
                    "values": value,
                }
            )

    # Сохраняем получившийся результат
    pd.DataFrame(db).to_csv("result.csv")


def start() -> None:

    process_first_pool(YT_POOL_1, YT_POOL_2, OC)
    # process_second_pool("./data/data.json", YT_POOL_1, YT_POOL_2)

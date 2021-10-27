import os
import json
import time
import colorama
import datetime
from tqdm import tqdm
import numpy as np
import pandas as pd

from core import YandexToloka, OwnCloudAPI


def parse_data_first_pool(submitted_tasks: str, yt_pool_1: "YandexToloka",
                          pool_2_id: int, oc: "OwnCloudAPI") -> tuple[dict, list]:
    # Заводим словари, чтобы помнить, как соотносятся id задания из первого пула и id задания из второго пула
    url_to_first_id_map: dict = {}
    json_second_task: list = []

    for task in tqdm(submitted_tasks):
        first_task_id = task["id"]
        img_id = task["solutions"][0]["output_values"]["img"]

        image = yt_pool_1.get_image(img_id)
        out = open(f"./tmp/{first_task_id}.jpg", 'wb')
        out.write(image.content)
        out.close()

        url_img = oc.push_file(f"{first_task_id}.jpg", f"./tmp/{first_task_id}.jpg")
        os.remove(f"./tmp/{first_task_id}.jpg")

        url_to_first_id_map[url_img] = first_task_id
        json_second_task.append(
            {"input_values": {"image": url_img}, "pool_id": pool_2_id, "overlap": 5}
        )

    return url_to_first_id_map, json_second_task


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


def response_vector(k, second_task_id, second_task) -> list:
    """По ключу возвращает вектор ответов id задания

    :return: list
    """
    result = []

    test2 = list(
        map(lambda t: np.where(np.array(list(map(lambda x: x['id'], t['tasks']))) == second_task_id), second_task))

    for i in enumerate(test2):
        for j in i[1]:
            if j:
                result.append(second_task[i[0]]['solutions'][j[0]]['output_values'][k])

    return result


def verifying_responses(check_count, check_quality) -> dict:
    if np.sum(check_count) < 3:
        json_check = {
            "status": "REJECTED",
            "public_comment": "На фотографии должен быть ровно один электрический счетчик с показателями",
        }
    elif np.sum(check_quality) < 3:
        json_check = {
            "status": "REJECTED",
            "public_comment": "Показания на счетчике отчетливо не видны",
        }
    else:
        json_check = {
            "status": "ACCEPTED",
            "public_comment": "Изображение счетчика принято",
        }

    return json_check


def process_first_pool(yt_pool_1: "YandexToloka", yt_pool_2: "YandexToloka", oc: "OwnCloudAPI") -> None:
    """
    Обработка первого пула и загрузка во второй пул

    :param yt_pool_1: Объект YandexToloka на первый пул
    :param yt_pool_2: Объект YandexToloka на второй пул
    :param oc: Объект на OwnCloudAPI

    :return: None
    """

    submitted_tasks = yt_pool_1.get_all_submitted_tasks()

    if yt_pool_2.get_all_tasks():
        print(
            f"{colorama.Fore.RED}Во втором пуле уже есть задание. Удалите задания из второго пула и запустите заного!")
        time.sleep(5)
        return

    """
    Для каждого задания из первого пула:
        * Запоминаем его id
        * Загружаем картинку в Yandex Object Storage
        * Оборачиваем параметры в json для второго задания
    """
    print(f"{colorama.Fore.YELLOW}Загрузка картинок в {colorama.Fore.BLUE}OwnCloud:")
    url_to_first_id_map, json_second_task = parse_data_first_pool(
        submitted_tasks=submitted_tasks,
        yt_pool_1=yt_pool_1,
        pool_2_id=yt_pool_2.get_pool_id(),
        oc=oc
    )

    print(f"{colorama.Fore.YELLOW}Загрузка заданий в пул {yt_pool_2.get_pool_id()}")

    second_tasks_request = yt_pool_2.upload_task_pool(json_second_task)

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

    basename = "data.json"
    suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    filename = "_".join([suffix, str(yt_pool_1.get_pool_id()), str(yt_pool_2.get_pool_id()), basename])

    with open('./data/' + filename, 'w') as f:
        json.dump(first_id_to_second_id_map, f, indent=4)

    time.sleep(5)


def process_second_pool(path: str, yt_pool_2: "YandexToloka") -> None:
    db = []

    with open(path, "r", encoding='utf-8') as f:
        first_id_to_second_id_map = json.load(f)

    tasks = yt_pool_2.get_all_tasks()
    second_tasks = yt_pool_2.get_all_accepted_tasks()

    for first_task_id in tqdm(first_id_to_second_id_map):
        second_task_id = first_id_to_second_id_map[first_task_id]

        if not is_training_tasks(tasks, second_task_id):
            # Получаем вектор ответов пользователей
            value_list = response_vector("value", second_task_id, second_tasks)
            check_count_list = response_vector("check_count", second_task_id, second_tasks)
            check_quality_list = response_vector("check_quality", second_task_id, second_tasks)
            result = response_vector("result", second_task_id, second_tasks)

            json_check = verifying_responses(check_count_list, check_quality_list)

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
                    f"{colorama.Fore.GREEN}ID картинки -> [{first_task_id}] ({json_check['public_comment']}): {colorama.Fore.RESET}Показания счетчика: {value}. "
                    f"Его подтвердили {counts[ind]} из 5 пользователей")

            if json_check["status"] == "REJECTED":
                print(
                    f"{colorama.Fore.RED}ID картинки -> [{first_task_id}] ({json_check['public_comment']})")


        else:
            print(f"{colorama.Fore.YELLOW}Тренировочное задание", end=" ")
            value = parse_training_tasks("value", tasks, second_task_id)
            check_count = parse_training_tasks("check_count", tasks, second_task_id)
            check_quality = parse_training_tasks("check_quality", tasks, second_task_id)
            result = parse_training_tasks("result", tasks, second_task_id)

            json_check = verifying_responses(check_count, check_quality)

            if json_check["status"] == "ACCEPTED":
                value_list, check_count_list, check_quality_list = [], [], []

                print(
                    f"{colorama.Fore.GREEN}ID картинки -> [{first_task_id}] ({json_check['public_comment']}): {colorama.Fore.RESET}Показания счетчика: {value}. "
                    f"Его подтвердили {counts[ind]} из 5 пользователей")

            if json_check["status"] == "REJECTED":
                print(
                    f"{colorama.Fore.RED}ID картинки -> [{first_task_id}] ({json_check['public_comment']})")

        # yt_pool_2.patch_task(first_task_id, json_check)

        if json_check["status"] == "ACCEPTED":
            for coord in result:
                db.append(
                    {
                        "first_task_id": first_task_id,
                        "second_task_id": second_task_id,
                        "url_img": first_task_id,
                        "result": coord,
                        "check_count_list": check_count_list,
                        "check_quality_list": check_quality_list,
                        "value_list": value_list,
                        "check_count": check_count,
                        "check_quality": check_quality,
                        "values": value,
                    }
                )

    # Сохранить получившийся результат
    pd.DataFrame(db).to_csv("result.csv")

    input()
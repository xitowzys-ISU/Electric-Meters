import pandas as pd
import numpy as np
import requests
import boto3


# Данная функция скачивает изображение из первого задания, загружает
# в Yandex Object Storage и возвращает ссылку на изображение
def load_image_on_yandex_storage(img_id):
    session = boto3.session.Session(
        aws_secret_access_key="cULzT_bV4UJwCdPsI9r8jj9IBAEg-qqjWCTDsbLC",
        aws_access_key_id="IS0a55N1XO7Qn8CsLiZE"
    )
    s3 = session.client(
        service_name="s3", endpoint_url="https://storage.yandexcloud.net"
    )
    file = requests.get(
        url=URL_API + "attachments/%s/download" % img_id, headers=HEADERS
    )

    url = URL_API + "attachments/%s/download" % img_id

    s3.put_object(Bucket="electronic-counters", Key=img_id, Body=file.content)
    return "https://storage.yandexcloud.net/schetchiki/%s" % img_id


# Указываем ключ к API, а также ID пула первого и второго задания
TOLOKA_OAUTH_TOKEN = "AQAAAAA9qRB3AACtpXZ8QnWcIEyYgXeCj3UqkEg"
POOL_ID_FIRST = 28420385
POOL_ID_SECOND = 7006945
URL_API = "https://toloka.yandex.ru/api/v1/"
HEADERS = {
    "Authorization": "OAuth %s" % TOLOKA_OAUTH_TOKEN,
    "Content-Type": "application/JSON",
}

# Получаем список всех заданий из первого пула, которые ждут проверки
url_assignments = (
        URL_API + "assignments/?status=SUBMITTED&limit=10000&pool_id=%s" % POOL_ID_FIRST
)

submitted_tasks = requests.get(url_assignments, headers=HEADERS).json()["items"]

# Заводим словари, чтобы помнить, как соотносятся id задания из первого пула
# и id задания из второго пула
url_to_first_id_map = {}
first_id_to_second_id_map = {}
json_second_task = []

print(submitted_tasks)
# Для каждого задания из первого пула:
# * Запоминаем его id
# * Загружаем картинку в Yandex Object Storage
# * Оборачиваем параметры в json для второго задания
# for task in submitted_tasks:
#     first_task_id = task["id"]
#     img_id = task["solutions"][0]["output_values"]["img"]
#     url_img = load_image_on_yandex_storage(img_id)
#     url_to_first_id_map[url_img] = first_task_id
#     json_second_task.append(
#         {"input_values": {"image": url_img}, "pool_id": POOL_ID_SECOND, "overlap": 5}
#     )

# # Загружаем задания во второй пул
# # "Не баг, а фича": добавлять через API задания в пул можно только тогда,
# # когда сам пул создан через API
# second_tasks_request = requests.post(
#     url=URL_API + "tasks?open_pool=true", headers=HEADERS, json=json_second_task
# ).json()
#
# # В ответ нам выдали id вторых заданий.
# # По ним мы сможем запросить ответы после завершения задания, поэтому запомним их
# for second_task in second_tasks_request["items"].values():
#     second_task_id = second_task["id"]
#     img_url = second_task["input_values"]["image"]
#     first_task_id = url_to_first_id_map[img_url]
#     first_id_to_second_id_map[first_task_id] = second_task_id
#
#
# # Эту функцию я писал ночью, утром я сам не смог понять, как она работает
# # Она возращает ответы пользователей для конкретного поля
# def unknown_fun(k):
#     return list(map(lambda t: t['solutions'][
#         np.where(np.array(list(map(lambda x: x['id'], t['tasks']))) == second_task_id)[0][0]]['output_values'][k],
#                     second_task))
#
#
# # Меняем keys и values местами
# first_id_to_url_map = dict((v, k) for k, v in url_to_first_id_map.items())
# db = []
#
# # Выполняем этот код только после того, как задание 2 будет выполнено
# for first_task_id in first_id_to_second_id_map:
#
#     # Для каждого проверяемого задания 1
#     second_task_id = first_id_to_second_id_map[first_task_id]
#
#     # Получаем результаты задания 2
#     url_assignments = (
#             URL_API + "assignments/?status=ACCEPTED&task_id=%s" % second_task_id
#     )
#     second_task = requests.get(url_assignments, headers=HEADERS).json()["items"]
#
#     # Получаем вектор ответов пользователей
#     value_list = unknown_fun("value")
#     check_count_list = unknown_fun("check_count")
#     check_quality_list = unknown_fun("check_quality")
#
#     # Если больше двух людей ответили на первый вопрос «нет»,
#     # то значит счетчика на изображении нет,
#     # либо на изображении несколько счетчиков. Отклоняем задание
#     if np.sum(check_count_list) < 3:
#         json_check = {
#             "status": "REJECTED",
#             "public_comment": "На фотографии должен быть ровно один счетчик холодной либо горячей воды",
#         }
#     # Если больше двух людей сказали, что показания не видны, отклоняем задание
#     elif np.sum(check_quality_list) < 3:
#         json_check = {
#             "status": "REJECTED",
#             "public_comment": "Показания на счетчике отчетливо не видны",
#         }
#     # В остальных случаях принимаем задание
#     else:
#         json_check = {
#             "status": "ACCEPTED",
#             "public_comment": "Изображение счетчика принято",
#         }
#
#     url = URL_API + "assignments/%s" % first_task_id
#     result_patch_request = requests.patch(url, headers=HEADERS, json=json_check)
#
#     # Найдем для принятых заданий самый частый ответ
#     (values, counts) = np.unique(value_list, return_counts=True)
#     ind = np.argmax(counts)
#     if counts[ind] > 3 and json_check["status"] == "ACCEPTED":
#         print(
#             "Показания счетчика: %s. Его подтвердили %d из 5 пользователей"
#             % (values[ind], counts[ind])
#         )
#
#     # Чтобы ничего не забыть и не потерять, записываем в массив
#     db.append(
#         {
#             "first_task_id": first_task_id,
#             "second_task_id": second_task_id,
#             "url_img": first_id_to_url_map[first_task_id],
#             "check_count_list": check_count_list,
#             "check_quality_list": check_quality_list,
#             "value_list": value_list,
#         }
#     )
#
# # Сохраняем получившийся результат
# pd.DataFrame(db).to_csv("result.csv")

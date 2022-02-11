import time
import json
import multiprocessing
from bootstrap import start_bot
from config import TELEGRAM_BOT_TOKEN


def test_unauthorized_bot(caplog):

    token: str = "5112688413:AAHT8bcemHrysm3OjY9QVHp-JcQ0EOr-Js8()"
    start_bot(token)

    assert "Бот неавторизован. Проверьте API ключ" in caplog.text


def test_started_bot():
    """should be ok"""
    t = multiprocessing.Process(target=start_bot, args=(TELEGRAM_BOT_TOKEN,))
    t.start()
    time.sleep(5)
    t.terminate()

    with open('./logs/logs.log') as f:
        for line in f:
            pass
        json_line = json.loads(line)

    assert "Бот активирован" == json_line['record']['message']

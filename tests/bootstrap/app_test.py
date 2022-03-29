import time
import json
import pytest
import multiprocessing
from bootstrap import start_bot
from config import localization
from config import TELEGRAM_BOT_TOKEN


def test_unauthorized_bot():

    token: str = "5112688413:AAHT8bcemHrysm3OjY9QVHp-JcQ0EOr-Js8()"

    with pytest.raises(SystemExit) as e:
        start_bot(token)
    assert e.type == SystemExit
    assert e.value.code == 1


def test_started_bot():
    """should be ok"""
    t = multiprocessing.Process(target=start_bot, args=(TELEGRAM_BOT_TOKEN,))
    t.start()
    time.sleep(3)
    t.terminate()

    with open('./logs/logs.log') as f:
        for line in f:
            pass
        json_line = json.loads(line)

    assert localization.getText(
        "bot_logger_activate") == json_line['record']['message']

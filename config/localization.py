import os
from loguru import logger
from config import LOCALIZATION
from configparser import ConfigParser, NoSectionError, NoOptionError

localization = ConfigParser()
language = LOCALIZATION.upper()
localization.read("./config/localization/{}.ini".format(LOCALIZATION))


def getText(option: str) -> str:
    try:
        return localization.get(language, option)
    except (NoSectionError, NoOptionError):
        logger.warning(
            f"[Localization warning] The translation wasn't detected: {option}")
        return ""

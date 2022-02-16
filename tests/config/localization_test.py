import pytest
from config import localization


def test_no_translation_found(caplog):

    text = "hohmba"
    localization.getText(text)
    assert f"[Localization warning] The translation wasn't detected: {text}" in caplog.text

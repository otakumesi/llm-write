import pytest
from gptwrite.lang_conf import LangConf


def test_lang_conf():
    lang_conf = LangConf.from_lang("en")
    
    assert lang_conf.description == "en"
    assert lang_conf.generation == "English"
    assert lang_conf.t("messages.want_more") == "Please continue."

def test_lang_conf_ja():
    lang_conf = LangConf.from_lang("ja")
    
    assert lang_conf.description == "ja"
    assert lang_conf.generation == "Japanese"
    assert lang_conf.t("messages.want_more") == "続きを書いてください。"

def test_lang_conf_fallback():
    lang_conf = LangConf.from_lang("fr")
    
    assert lang_conf.description == "en"
    assert lang_conf.generation == "French"
    assert lang_conf.t("messages.want_more") == "Please continue."
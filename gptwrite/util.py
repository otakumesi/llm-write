import logging
import i18n
from iso639 import Lang


logger = logging.getLogger(__name__)


def init_i18n(lang: Lang) -> str:
    i18n.set("locale", lang.pt1)
    i18n.set("fallback", "en")
    i18n.set("file_format", "yaml")
    i18n.set("enable_yaml", True)

    if lang.pt1 not in ["en", "ja"]:
        logger.warning(
            f"{lang.name} is not supported in CLI texts. "
            "Fallback to English. "
            "(There is no problem with generated text!) ")
        return "en"

    return lang.pt1
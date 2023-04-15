import logging
import i18n
from pathlib import Path
from typing import Any
from dataclasses import dataclass
from iso639 import Lang

logger = logging.getLogger(__name__)


@dataclass
class LangConf:
    description: str
    generation: str

    @staticmethod
    def from_lang(lang: str) -> "LangConf":
        lang = Lang(lang)
        return LangConf(lang.pt1, lang.name)

    def __post_init__(self) -> None:
        self.init_i18n()

        if self.description not in ["en", "ja"]:
            logger.warning(
                f"{self.description} is not supported in CLI texts. "
                "Fallback to English. "
                "(There is no problem with generated text!) ")
            self.description = "en"

    def init_i18n(self) -> str:
        i18n.load_path.append(Path(__file__).parent.absolute() / "locales")
        i18n.set("locale", self.description)
        i18n.set("fallback", "en")
        i18n.set("file_format", "yaml")
        i18n.set("enable_yaml", True)
    
    def t(self, key: str, **kwargs: Any) -> str:
        return i18n.t(key, locale=self.description, *kwargs)
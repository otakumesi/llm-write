from typing import List
from dataclasses import dataclass
import questionary
from gptwrite.accepted_language import ACCEPTED_LANGUAGES
from gptwrite.lang_conf import LangConf


class QuestionaryUI:
    lang_conf: LangConf

    def ask_language(self) -> str:
        lang = questionary.select('Language?', default="English", choices=ACCEPTED_LANGUAGES).unsafe_ask()
        self.lang_conf = LangConf.from_lang(lang)
        return self.lang_conf

    def ask_theme(self) -> str:
        return questionary.text(self.lang_conf.t("messages.want_theme")).unsafe_ask()
    
    def confirm_want_add_topic(self) -> bool:
        return questionary.confirm(self.lang_conf.t("messages.want_add_topic"), default=False).unsafe_ask()
    
    def ask_want_topic(self, topics) -> str:
        return questionary.checkbox(
            self.lang_conf.t("messages.want_topic"),
            choices=topics).unsafe_ask()
    
    def ask_want_topic_nuance(self) -> str:
        return questionary.text(self.lang_conf.t("messages.want_topic_nuance")).unsafe_ask()
    
    def ask_want_select_topics(self, topics: List[str]) -> List[str]:
        return questionary.checkbox(
            self.lang_conf.t("messages.want_topic"),
            choices=topics).unsafe_ask()
    
    def ask_want_paragraph_topics(self, selected_topics: List[str]) -> List[str]:
        return questionary.checkbox(
                self.lang_conf.t("messages.want_paragraph_topic"),
                choices=selected_topics).unsafe_ask()
    
    def ask_want_paragraph_nuance(self) -> str:
        return questionary.text(self.lang_conf.t("messages.want_paragraph_nuance")).unsafe_ask()

    def confirm_want_add_paragraph(self) -> bool:
        return questionary.confirm(self.lang_conf.t("messages.want_add_paragraph"), default=True).unsafe_ask()

    def ask_want_paragraph_nuance(self) -> str:
        return questionary.text(self.lang_conf.t("messages.want_paragraph_nuance")).unsafe_ask()

    def confirm_want_remove_topics(self) -> bool:
        return questionary.confirm(self.lang_conf.t("messages.remove_topics")).unsafe_ask()

    def confirm_want_accept_text(self, text: str) -> bool:
        return questionary.confirm(self.lang_conf.t("messages.accept_text") + "\n" + text).unsafe_ask()
    
    def confirm_want_save(self) -> bool:
        return questionary.confirm(self.lang_conf.t("messages.save"), default=False).ask()

    def ask_output_path(self) -> str:
        return questionary.text('Output Path?').ask()

    def confirm_want_more(self) -> bool:
        return questionary.confirm(self.lang_conf.t("messages.confirm_want_more")).unsafe_ask()
    
    def ask_want_complementary(self) -> str:
        return questionary.text(self.lang_conf.t("messages.want_complementary")).unsafe_ask()
import os
import logging
from pathlib import Path
import questionary
from gptwrite.lang_conf import LangConf
from gptwrite.accepted_language import ACCEPTED_LANGUAGES
from gptwrite.core import select_topics, generate_topics, generate_texts


logger = logging.getLogger(__name__)


def write() -> None:
    lang = questionary.select('Language?', default="English", choices=ACCEPTED_LANGUAGES).unsafe_ask()
    lang_conf = LangConf.from_lang(lang)

    if not os.environ.get("OPENAI_API_KEY", None):
        logger.error(lang_conf.t("messages.no_api_key"))
        exit()

    theme = questionary.text(lang_conf.t("messages.want_theme")).unsafe_ask()
    generated_topics = generate_topics(theme, lang_conf)
    selected_topics = select_topics(generated_topics, lang_conf)

    while True:
        if questionary.confirm(lang_conf.t("messages.want_add_topic"), default=False).unsafe_ask():
            topic_nuance = questionary.text(lang_conf.t("messages.want_topic_nuance")).unsafe_ask()
            generated_topics = generate_topics(theme=theme, lang_conf=lang_conf, nuance=topic_nuance)
            selected_topics += select_topics(topics=generated_topics, lang_conf=lang_conf)
        else:
            break

    paragraphs = []
    while selected_topics:
        paragraph_topics = questionary.checkbox(
            lang_conf.t("messages.want_paragraph_topic"),
            choices=selected_topics).unsafe_ask()
        paragraph_nuance = questionary.text(lang_conf.t("messages.want_paragraph_nuance")).unsafe_ask()
        text = generate_texts(theme=theme, topics=paragraph_topics, nuance=paragraph_nuance, lang_conf=lang_conf)

        if questionary.confirm(lang_conf.t("messages.accept_text") + "\n" + text).unsafe_ask():
            paragraphs.append(text)
            if questionary.confirm(lang_conf.t("messages.remove_topics")).unsafe_ask():
                selected_topics = [t for t in selected_topics if t not in paragraph_topics]
        
        if not questionary.confirm(lang_conf.t("messages.want_add_paragraph"), default=True).unsafe_ask():
            break

    article = "\n\n".join(paragraphs)
    if questionary.confirm(lang_conf.t("messages.save"), default=False).ask():
        try:
            output_path = questionary.text('Output Path?').ask()
            Path(output_path).write_text(article)
        except Exception as e:
            logger.error(e)
            print(article)
    else:
        print(article)
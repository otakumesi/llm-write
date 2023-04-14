import os
import logging
from pathlib import Path
from iso639 import Lang
import i18n
import questionary
from util import init_i18n
from accepted_language import ACCEPTED_LANGUAGES
from core import select_topics, generate_topics, generate_texts


logger = logging.getLogger(__name__)
i18n.load_path.append(Path(__file__).parent.absolute() / "locales")


def write():
    lang = questionary.select('Language?', default="English", choices=ACCEPTED_LANGUAGES).unsafe_ask()
    lang = Lang(lang)

    lang_for_generating = lang.name
    lang_for_description = init_i18n(lang)

    if not os.environ.get("OPENAI_API_KEY", None):
        logger.error(i18n.t("messages.no_api_key", locale=lang_for_description))
        exit()

    theme = questionary.text(i18n.t("messages.want_theme", locale=lang_for_description)).unsafe_ask()
    generated_topics = generate_topics(theme, lang_for_generating)
    selected_topics = select_topics(generated_topics, lang_for_description)

    while True:
        if questionary.confirm(i18n.t("messages.want_add_topic", locale=lang_for_description), default=False).unsafe_ask():
            topic_nuance = questionary.text(i18n.t("messages.want_topic_nuance", locale=lang_for_description)).unsafe_ask()
            generated_topics = generate_topics(theme, lang_for_generating, topic_nuance)
            selected_topics += select_topics(generated_topics, lang_for_description)
        else:
            break

    paragraphs = []
    while selected_topics:
        paragraph_topics = questionary.checkbox(
            i18n.t("messages.want_paragraph_topic", locale=lang_for_description),
            choices=selected_topics).unsafe_ask()
        paragraph_nuance = questionary.text(i18n.t("messages.want_paragraph_nuance", locale=lang_for_description)).unsafe_ask()
        text = generate_texts(theme, paragraph_topics, paragraph_nuance, lang_for_generating, lang_for_description)

        if questionary.confirm(i18n.t("messages.accept_text") + "\n" + text).unsafe_ask():
            paragraphs.append(text)
            if questionary.confirm(i18n.t("messages.remove_topics")).unsafe_ask():
                selected_topics = [t for t in selected_topics if t not in paragraph_topics]
        
        if not questionary.confirm(i18n.t("messages.want_add_paragraph", locale=lang_for_description), default=True).unsafe_ask():
            break

    article = "\n\n".join(paragraphs)
    if questionary.confirm(i18n.t("messages.save", locale=lang_for_description), default=False).ask():
        try:
            output_path = questionary.text('Output Path?').ask()
            Path(output_path).write_text(article)
        except Exception as e:
            logger.error(e)
            print(article)
    else:
        print(article)
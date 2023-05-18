import os
import logging
from pathlib import Path
from llmwrite.lang_conf import LangConf
from llmwrite.accepted_language import ACCEPTED_LANGUAGES
from llmwrite.core import generate_topics, generate_texts
from llmwrite.questionary_ui import QuestionaryUI


logger = logging.getLogger(__name__)

def run(qui = QuestionaryUI()) -> None:
    lang_conf = qui.ask_language()

    if not os.environ.get("OPENAI_API_KEY", None):
        logger.error(lang_conf.t("messages.no_api_key"))
        exit()

    theme = qui.ask_theme()
    generated_topics = generate_topics(theme, lang_conf)
    selected_topics = qui.ask_want_select_topics(generated_topics)

    while qui.confirm_want_add_topic():
        topic_nuance = qui.ask_want_topic_nuance()
        generated_topics = generate_topics(theme=theme, lang_conf=lang_conf, nuance=topic_nuance)
        selected_topics += qui.ask_want_select_topics(generated_topics)

    paragraphs = []
    while selected_topics:
        paragraph_topics = qui.ask_want_paragraph_topics(selected_topics)
        paragraph_nuance = qui.ask_want_paragraph_nuance()
        text = generate_texts(theme=theme, topics=paragraph_topics, nuance=paragraph_nuance, qui=qui)

        if qui.confirm_want_accept_text(text):
            paragraphs.append(text)
            if qui.confirm_want_remove_topics():
                selected_topics = [t for t in selected_topics if t not in paragraph_topics]
        
        if not qui.confirm_want_add_paragraph():
            break

    article = "\n\n".join(paragraphs)
    if qui.confirm_want_save():
        try:
            output_path = qui.ask_output_path()
            Path(output_path).write_text(article)
        except Exception as e:
            logger.error(e)
            print(article)
    else:
        print(article)


def write(qui = QuestionaryUI()) -> None:
    try:
        run(qui)
    except KeyboardInterrupt:
        print("^C")
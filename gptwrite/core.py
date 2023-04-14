import re
import logging
import i18n
import openai
import questionary
from gptwrite.prompts import build_prompt_generate_topics, build_prompt_generate_texts, build_prompt_rewrite_texts


ACTIONS = ["Thought", "Consult", "Write"]

logger = logging.getLogger(__name__)


def select_topics(topics, lang_for_description):
    selected_topics = questionary.checkbox(
        i18n.t("messages.want_topic", locale=lang_for_description),
        choices=topics).unsafe_ask()
    return selected_topics

def generate_topics(theme, lang_for_generating, nuance=None):
    messages = [{
        "role": "user",
        "content": build_prompt_generate_topics(theme, lang_for_generating, nuance)
    }]
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages)
    content = response.choices[0].message.content
    return put_generated_text_into_list(content)

def put_generated_text_into_list(text):
    topics = []
    for line in text.split("\n"):
        if line.startswith("- "):
            topics.append(line[2:].strip())
            continue
        if line.startswith("・ "):
            topics.append(line[2:].strip())
            continue
        if line.startswith("* "):
            topics.append(line[2:].strip)
            continue
        num_list_match = re.search(r"^(\d+)\. ", line)
        if num_list_match:
            topics.append(line[len(num_list_match.groups()[0]):].strip())
            continue
    return topics

def generate_texts(theme, topics, nuance, lang_for_generating, lang_for_description):
    messages = [{
        "role": "user",
        "content": build_prompt_generate_texts(theme, topics, nuance, lang_for_generating)
    }]

    writes = []

    while True:
        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                stop="\n\n")
        content = response.choices[0].message.content
        print(content)

        if content.startswith("[Consult]"):
            comprementary = questionary.text(i18n.t("messages.want_complementary", locale=lang_for_description)).unsafe_ask()
            messages.append({
                "role": "user",
                "content": f"[Complement]{comprementary}"
            })
            continue

        if content.startswith("[Thought]"):
            messages.append({
                "role": "assistant",
                "content": content
            })
            continue
        
        if content.startswith("[Write]"):
            writes.append(content[7:].strip())
            if not questionary.confirm(i18n.t("messages.confirm_want_more", locale=lang_for_description)).unsafe_ask():
                break
            messages.append({
                "role": "assistant",
                "content": f"[Request]{i18n.t('messages.want_more', locale=lang_for_description)}"
            }) 
            continue

        messages.append({"role": "system", "content": i18n.t("messages.", locale=lang_for_description)})

    return rewrite_texts(writes, lang_for_generating)

def rewrite_texts(sentences, lang_for_generating):
    messages = [{
        "role": "user",
        "content": build_prompt_rewrite_texts(sentences, lang_for_generating)
    }]
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages)
    content = response.choices[0].message.content
    return content
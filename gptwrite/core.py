import re
import logging
from typing import List, Callable, Optional, Dict
import i18n
import openai
import questionary
from gptwrite.prompts import build_prompt_generate_topics, build_prompt_generate_texts, build_prompt_rewrite_texts


GenerateFunc = Callable[[str, List[str], Optional[str], str, str], str]
OpenAIMessages = List[Dict[str, str]]

ACTIONS = ["Thought", "Consult", "Write"]

logger = logging.getLogger(__name__)


def generate_text_by_llm(
        messages: OpenAIMessages,
        model_name: str = "gpt-3.5-turbo",
        stop: Optional[str] = None
    ) -> str:
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=messages,
        stop=stop)
    content = response.choices[0].message.content
    return content

def select_topics(
        topics: List[str],
        lang_for_description: str,
    ) -> List[str]:
    selected_topics = questionary.checkbox(
        i18n.t("messages.want_topic", locale=lang_for_description),
        choices=topics).unsafe_ask()
    return selected_topics

def generate_topics(
        theme: str,
        lang_for_generating: str,
        nuance: Optional[str] = None,
        generate_text_func: GenerateFunc = generate_text_by_llm,
    ) -> List[str]:
    messages = [{
        "role": "user",
        "content": build_prompt_generate_topics(theme, lang_for_generating, nuance)
    }]
    content = generate_text_func(messages=messages)
    return put_generated_text_into_list(content)

def put_generated_text_into_list(text: str) -> List[str]:
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

def generate_texts(
        theme: str,
        topics: List[str],
        nuance: Optional[str],
        lang_for_generating: str,
        lang_for_description: str,
        generate_text_func: GenerateFunc  = generate_text_by_llm,
    ) -> str:
    messages = [{
        "role": "user",
        "content": build_prompt_generate_texts(theme, topics, nuance, lang_for_generating)
    }]

    writes = []

    while True:
        content = generate_text_func(messages=messages, stop="\n\n")
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

    result_texts = ""
    while True:
        result_texts += rewrite_texts(writes, lang_for_generating)
        if not questionary.confirm(i18n.t("messages.want_more", locale=lang_for_description)).unsafe_ask():
            break
    return "\n".join(result_texts)

def rewrite_texts(
        sentences: List[str],
        lang_for_generating: str,
        generate_text_func: GenerateFunc = generate_text_by_llm,
    ) -> str:
    messages = [{
        "role": "user",
        "content": build_prompt_rewrite_texts(sentences, lang_for_generating)
    }]

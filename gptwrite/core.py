import re
import logging
from typing import Optional, Any, Protocol, List, Dict
import openai
import questionary
from gptwrite.prompts import build_prompt_generate_topics, build_prompt_generate_texts, build_prompt_rewrite_texts
from gptwrite.lang_conf import LangConf


OpenAIMessages = List[Dict[str, str]]
class ExecuteLLM(Protocol):
    def __call__(
            self,
            messages: OpenAIMessages,
            model_name: str = "gpt-3.5-turbo",
            stop: Optional[str] = None,
        ) -> str:
        raise NotImplementedError


ACTIONS = ["Thought", "Consult", "Write"]

logger = logging.getLogger(__name__)


def generate_text_by_llm(
        messages: OpenAIMessages,
        model_name: str = "gpt-3.5-turbo",
        stop: Optional[str] = None
    ) -> str:
    response: Any = openai.ChatCompletion.create(
        model=model_name,
        messages=messages,
        stop=stop)
    content = response.choices[0].message.content
    return content

def select_topics(
        topics: List[str],
        lang_conf: LangConf,
    ) -> List[str]:
    selected_topics = questionary.checkbox(
        lang_conf.t("messages.want_topic"),
        choices=topics).unsafe_ask()
    return selected_topics

def generate_topics(
        theme: str,
        lang_conf: LangConf,
        nuance: Optional[str] = None,
        generate_text_func: ExecuteLLM = generate_text_by_llm,
    ) -> List[str]:
    prompt = build_prompt_generate_topics(theme=theme, language=lang_conf.generation, nuance=nuance)
    messages = [{
        "role": "user",
        "content": prompt,
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
        nuance: str,
        lang_conf: LangConf,
        generate_text_func: ExecuteLLM = generate_text_by_llm,
    ) -> str:
    prompt = build_prompt_generate_texts(theme=theme, topics=topics, nuance=nuance, language=lang_conf.generation)
    messages = [{
        "role": "user",
        "content": prompt,
    }]

    writes = []

    while True:
        content = generate_text_func(messages=messages, stop="\n\n")
        print(content)

        if content.startswith("[Consult]"):
            comprementary = questionary.text(lang_conf.t("messages.want_complementary")).unsafe_ask()
            messages.append({
                "role": "user",
                "content": f"[Complement]{comprementary}",
            })
            continue

        if content.startswith("[Thought]"):
            messages.append({
                "role": "assistant",
                "content": content,
            })
            continue
        
        if content.startswith("[Write]"):
            writes.append(content[7:].strip())
            if not questionary.confirm(lang_conf.t("messages.confirm_want_more")).unsafe_ask():
                break
            messages.append({
                "role": "assistant",
                "content": f"[Request]{lang_conf.t('messages.want_more')}",
            }) 
            continue

        messages.append({"role": "system", "content": lang_conf.t("messages.include_action")})

    return rewrite_texts(writes, lang_conf)

def rewrite_texts(
        sentences: List[str],
        lang_conf: LangConf,
        generate_text_func: ExecuteLLM = generate_text_by_llm,
    ) -> str:
    print(lang_conf.t("messages.rewrite"))
    prompt = build_prompt_rewrite_texts(sentences=sentences, language=lang_conf.generation)
    messages = [{
        "role": "user",
        "content": prompt,
    }]

    result_texts = ""
    while True:
        content = generate_text_func(messages=messages)
        print(content)
        result_texts += content
        if not questionary.confirm(lang_conf.t("messages.want_more")).unsafe_ask():
            break
        messages.append({"role": "user", "content": f"[Request]{lang_conf.t('messages.want_more')}"})
    return result_texts
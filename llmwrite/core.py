import re
import logging
from typing import Optional, Any, Protocol, List, Dict
import openai
from yaspin import yaspin
from llmwrite.prompts import build_prompt_generate_topics, build_prompt_generate_texts, build_prompt_rewrite_texts
from llmwrite.lang_conf import LangConf
from llmwrite.questionary_ui import QuestionaryUI


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
        lang_conf: LangConf,
        model_name: str = "gpt-3.5-turbo",
        stop: Optional[str] = None
    ) -> str:
    with yaspin(text=lang_conf.t("messages.generating_text"), color="yellow") as spinner:
        response: Any = openai.ChatCompletion.create(
            model=model_name,
            messages=messages,
            stop=stop)
        spinner.ok("🆗")
    content = response.choices[0].message.content
    return content

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
    content = generate_text_func(messages=messages, lang_conf=lang_conf)
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
        qui: QuestionaryUI,
        generate_text_func: ExecuteLLM = generate_text_by_llm,
    ) -> str:
    prompt = build_prompt_generate_texts(theme=theme, topics=topics, nuance=nuance, language=qui.lang_conf.generation)
    messages = [{
        "role": "user",
        "content": prompt,
    }]

    writes = []

    while True:
        content = generate_text_func(messages=messages, stop="\n\n", lang_conf=qui.lang_conf)
        print(content)

        if content.startswith("[Consult]"):
            comprementary = qui.ask_want_complementary()
            messages.append({
                "role": "user",
                "content": f"[Answer]{comprementary}",
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
            if not qui.confirm_want_more():
                break
            messages.append({
                "role": "assistant",
                "content": f"[Request]{qui.lang_conf.t('messages.want_more')}",
            }) 
            continue

        messages.append({"role": "system", "content": qui.lang_conf.t("messages.include_action")})

    return rewrite_texts(writes, qui)

def rewrite_texts(
        sentences: List[str],
        qui: QuestionaryUI,
        generate_text_func: ExecuteLLM = generate_text_by_llm,
    ) -> str:
    print(qui.lang_conf.t("messages.rewrite"))
    prompt = build_prompt_rewrite_texts(sentences=sentences, language=qui.lang_conf.generation)
    messages = [{
        "role": "user",
        "content": prompt,
    }]

    result_texts = ""
    while True:
        content = generate_text_func(messages=messages, lang_conf=qui.lang_conf)
        print(content)
        result_texts += content
        if not qui.confirm_want_more():
            break
        messages.append({"role": "user", "content": f"[Request]{qui.lang_conf.t('messages.want_more')}"})
    return result_texts
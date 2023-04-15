import pytest
from gptwrite.prompts import build_prompt_generate_topics, build_prompt_generate_texts, build_prompt_rewrite_texts

GENERATE_TOPICS_PROMPT_NO_NUANCE = """# Instruction
A user wants to write an article based on the following theme.
What topics should be available to write an article on the entered theme?
Please write a bullet list of the topics that might be needed.

# User Input (Theme)
ここにテーマが入力されます。

# Output Example
- Topic 1
- Topic 2
- Topic 3

# CAUTION
- Please do not use the same topic as the theme.
- Please output should be in the form of a list.
- Please must be sure to reply using Japanese!

# System Output (Topics)
<Your outputs>"""

GENERATE_TOPICS_PROMPT_NO_NUANCE = """# Instruction
A user wants to write an article based on the following theme.
What topics should be available to write an article on the entered theme?
Please write a bullet list of the topics that might be needed.

# User Input (Theme)
ここにテーマが入力されます。

# Topic Scope
ここにニュアンスが入ります。

# Output Example
- Topic 1
- Topic 2
- Topic 3

# CAUTION
- Please do not use the same topic as the theme.
- Please output should be in the form of a list.
- Please must be sure to reply using Japanese!

# System Output (Topics)
<Your outputs>"""

def test_build_prompt_generate_topics():
    prompt = build_prompt_generate_topics("ここにテーマが入力されます。", "Japanese", "ここにニュアンスが入ります。")
    assert prompt == GENERATE_TOPICS_PROMPT_NO_NUANCE


GENERATE_TEXT_PROMPT = """# Instruction
A user wants to write an article based on the following theme.
Please choose actions for writing paragraph about the theme, nuance and topics.

# Theme
ここにテーマが入力されます。

# Nuance
ここにニュアンスが入ります。

# Topics
- ここにトピックが入ります。

With the goal of writing an paragraph for the above topics, choose an action and output it in the following format.

Use the following format:
[<Action>] <Your answer based on the action>

# Actions
Thought: you may think about what you should write.
Consult: you may consult users about addtional information or what you should write.
Write: you write paragraph based on topics in an article about ここにテーマが入力されます。.

# CAUTION
- Please include the action in your answer.
- Please write the action in square brackets.
- Please must be sure to reply using Japanese!"""

def test_build_prompt_generate_texts():
    prompt = build_prompt_generate_texts(
        theme="ここにテーマが入力されます。",
        nuance="ここにニュアンスが入ります。",
        language="Japanese",
        topics=["ここにトピックが入ります。"],
    )
    assert prompt == GENERATE_TEXT_PROMPT


REWRITING_TEXT_PROMPT = """# Instruction
Please Write good paragraphs, piecing together the following sentences given.

# Sentences
- Sentence 1
- Sentence 2

# CAUTION
- Please must be sure to reply using English!"""

def test_build_prompt_rewrite_texts():
    prompt = build_prompt_rewrite_texts(
        language="English",
        sentences=["Sentence 1", "Sentence 2"],
    )
    assert prompt == REWRITING_TEXT_PROMPT
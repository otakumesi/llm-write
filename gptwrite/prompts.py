def build_prompt_generate_topics(theme, language, nuance=None):
    prompt = GENERATE_TOPICS_PROMPT_PREFIX.format(theme=theme, language=language)
    if nuance:
        prompt += GENERATE_TOPICS_PROMPT_NUANCE.format(nuance=nuance)
    prompt += GENERATE_TOPICS_PROMPT_SUFFIX.format(language=language)
    return prompt


GENERATE_TOPICS_PROMPT_PREFIX = """# Instruction
A user wants to write an article based on the following theme.
What topics should be available to write an article on the entered theme?
Please write a bullet list of the topics that might be needed.

# User Input (Theme)
{theme}"""

GENERATE_TOPICS_PROMPT_NUANCE = """
# Topic Scope
{nuance}"""

GENERATE_TOPICS_PROMPT_SUFFIX = """
# Output Example
- Topic 1
- Topic 2
- Topic 3

# CAUTION
- Please do not use the same topic as the theme.
- Please output should be in the form of a list.
- Please must be sure to reply using {language}!

# System Output (Topics)
<Your outputs>"""


def build_prompt_generate_texts(theme, topics, nuance, language):
    return GENERATE_TEXT_PROMPT.format(
        theme=theme,
        topics="\n".join(["- " + topic for topic in topics]),
        nuance=nuance,
        language=language)

GENERATE_TEXT_PROMPT = """# Instruction
A user wants to write an article based on the following theme.
Please choose actions for writing paragraph about the theme, nuance and topics.

# Theme
{theme}

# Nuance
{nuance}

# Topics
{topics}

With the goal of writing an paragraph for the above topics, choose an action and output it in the following format.

Use the following format:
[<Action>] <Your answer based on the action>

# Actions
Thought: you may think about what you should write.
Consult: you may consult users about addtional information or what you should write.
Write: you write paragraph based on topics in an article about {theme}.

# CAUTION
- Please include the action in your answer.
- Please write the action in square brackets.
- Please must be sure to reply using {language}!"""
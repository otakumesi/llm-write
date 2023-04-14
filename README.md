# GPT-Write :writing_hand:

__GPT make writing an article brazing fast :fire:.__

PyPi:
- https://pypi.org/project/gptwrite/

![GPT-Write Demo](https://github.com/otakumesi/gpt-write/blob/main/demo.gif?raw=true "デモ")

## :telescope: Overview
- GPT-Write is the CLI tool for Intractive Automated Article Writing.  
- You can create articles, just answer the questions.   
- Since the language is specified in the GPT prompt and GPT is allowed to generate the text, it could theoretically be used in a variety of languages.  
    - However, the supported languages in the shell messages are only English and Japanese.


## :runner: Installation
```sh
pip install gptwrite
```

## :computer: Usage

```sh
# Set Environment "OPENAI_API_KEY"
export OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxx

# Run
gptwrite
? Language? <Select Language>
# ...(Lots of questions come in to the interactive.)
```
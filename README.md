# LLM-Write (powered by GPT-3) :writing_hand:

__LLM make writing an article brazing fast :fire:.__

PyPi:
- https://pypi.org/project/llmwrite/

![LLM-Write Demo](https://github.com/otakumesi/gpt-write/blob/main/demo.gif?raw=true "デモ")

## :telescope: Overview
- This app is built with GPT-3.
- LLM-Write is the CLI tool for Intractive Automated Article Writing.  
- You can create articles, just answer the questions.   
- Since the language is specified in the LLM prompt and LLM is allowed to generate the text, it could theoretically be used in a variety of languages.  
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

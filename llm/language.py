"""RD.E Language: finds the language of each post and translates it to English.

Function: process_post(post)

Input:
    post (str): the post as it was sent, in any language.
    Sample: "Nou bezwen dlo nan Delmas 60, nou se 200 fanmi."

Output (dict):
    language (str): the language name in English, such as "English", "Haitian Creole" or "Urdu".
    english (str): the post in English (the same text if it is already English).
                   Names of places and people and all numbers stay exactly the same.
    translated (bool): True if the post was not in English and was translated.
    Sample: {"language": "Haitian Creole", "english": "We need water in Delmas 60, we are 200 families.",
             "translated": True}

Raises ValueError if the LLM's answer can't be used.
Test it: python3 llm/language.py      Score it: python3 score.py language
"""
import ollama

# This lets the file work both as "python3 llm/language.py" and as "from llm.language import ...".
if __package__:
    from .utils import read_json
else:
    from utils import read_json

instruction = """TODO: say who the LLM is and what it must do."""

context = """TODO: the labels, rules and facts the LLM needs."""

examples = """TODO: a few examples of input and the exact output you want."""

output_format = """TODO: the exact JSON the LLM must return."""


def build_prompt(post):
    prompt = f"""<instruction>{instruction}</instruction>
<context>{context}</context>
<examples>{examples}</examples>
<output_format>{output_format}</output_format>
<query>Post: {post}
Output:</query>"""
    return prompt


def process_post(post):
    # TODO: write this function. The docstring at the top of this file is the contract.
    # 1. build_prompt(...), call
    #    ollama.generate(model="llama3.2", prompt=prompt, format="json", options={"num_predict": 500}),
    #    and read the answer with read_json.
    # 2. Check it: language is a str, and english is a str that is not empty. Ask for the two keys language and english.
    #    Ask again (up to 3 tries) if it fails, then raise ValueError.
    # 3. translated is False if the language is English, and then english is the post exactly as written. Return {"language": ..., "english": ..., "translated": ...}.
    raise NotImplementedError("process_post is not written yet")


if __name__ == "__main__":
    post = input("Post: ")
    print(process_post(post))

"""RD.A Sorter: decides what kind of help each post asks for, and how urgent it is.

Function: sort_post(post)

Input:
    post (str): the post in English, with personal details hidden.
    Sample: "We are 20 people in Carrefour with no water since yesterday."

Output (dict):
    need_type (str): rescue, medical, food_water, shelter, infrastructure or other.
                     If a post names more than one need, the first one in this list wins.
    urgency (str): emergency, high, normal or low.
    Sample: {"need_type": "food_water", "urgency": "high"}

Raises ValueError if the LLM's answer can't be used.
Test it: python3 llm/sorter.py      Score it: python3 score.py sorter
"""
import ollama

# This lets the file work both as "python3 llm/sorter.py" and as "from llm.sorter import ...".
if __package__:
    from .utils import read_json
else:
    from utils import read_json

NEED_TYPES = ["rescue", "medical", "food_water", "shelter", "infrastructure", "other"]
URGENCIES = ["emergency", "high", "normal", "low"]

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


def sort_post(post):
    # TODO: write this function. The docstring at the top of this file is the contract.
    # 1. build_prompt(...), call
    #    ollama.generate(model="llama3.2", prompt=prompt, format="json", options={"num_predict": 500}),
    #    and read the answer with read_json.
    # 2. Check it: answer["needs"] is a list and answer["urgency"] is in URGENCIES. Ask the LLM to list every need the post has.
    #    Ask again (up to 3 tries) if it fails, then raise ValueError.
    # 3. Your code, not the LLM, picks need_type: the first word in NEED_TYPES that is in the list (or "other"). Return {"need_type": ..., "urgency": ...}.
    raise NotImplementedError("sort_post is not written yet")


if __name__ == "__main__":
    post = input("Post: ")
    result = sort_post(post)
    print(result)

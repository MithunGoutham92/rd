"""RD.D Details: pulls out the details coordinators need from a post.

Function: extract_details(post)

Input:
    post (str): the post in English, with personal details hidden.
    Sample: "We are 200 families in Delmas 60 with no water since Tuesday."

Output (dict):
    kind (str): request (asks for help), offer (offers help) or report (news, questions, other).
    places (list of str): places named in the post, copied from it.
    needs (list of str): things the post asks for or offers, such as "water" or "tents".
    amounts (list of str): numbers of people or things, copied from the post, such as "200 families".
    times (list of str): times or dates copied from the post, such as "since Tuesday".
    Sample: {"kind": "request", "places": ["Delmas 60"], "needs": ["water"],
             "amounts": ["200 families"], "times": ["since Tuesday"]}

Raises ValueError if the LLM's answer can't be used.
Test it: python3 llm/details.py      Score it: python3 score.py details
"""
import ollama

# This lets the file work both as "python3 llm/details.py" and as "from llm.details import ...".
if __package__:
    from .utils import read_json
else:
    from utils import read_json

KINDS = ["request", "offer", "report"]
LIST_KEYS = ["places", "needs", "amounts", "times"]

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


def extract_details(post):
    # TODO: write this function. The docstring at the top of this file is the contract.
    # 1. build_prompt(...), call
    #    ollama.generate(model="llama3.2", prompt=prompt, format="json", options={"num_predict": 500}),
    #    and read the answer with read_json.
    # 2. Check it: answer["kind"] is in KINDS, and every key in LIST_KEYS is a list.
    #    Ask again (up to 3 tries) if it fails, then raise ValueError.
    # 3. Return a dict with kind and the four list keys.
    raise NotImplementedError("extract_details is not written yet")


if __name__ == "__main__":
    post = input("Post: ")
    result = extract_details(post)
    print(result)

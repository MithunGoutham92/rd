"""Phase 2 team tool: checks whether a new post repeats an earlier post.

Function: find_duplicate(text, need_type, kind, places, posts)

Input:
    text (str): the new post, with personal details hidden.
    need_type (str): the new post's need type, from the Sorter.
    kind (str): the new post's kind, from Details.
    places (list of str): the new post's places, from Details.
    posts (list of dict): saved posts, each with id, duplicate_of, need_type, kind, places and text.
    Sample: "Family stuck under a house on Rue 4", "rescue", "request", ["Rue 4"],
            [{"id": 1, "duplicate_of": None, "need_type": "rescue", "kind": "request",
              "places": ["Rue 4"], "text": "Family trapped under a house, Rue 4"}]

Output (dict):
    duplicate_of (int or None): the matching post's id, or None if there is no match.
    Sample: {"duplicate_of": 1}

The code keeps only earlier posts with the same need type and kind at the same place
(same_place in utils.py). The LLM then chooses which of those posts, if any, is the same situation.
Raises ValueError if the LLM's answer can't be used.
"""
import ollama

if __package__:
    from .utils import same_place, read_json
else:
    from utils import same_place, read_json

instruction = """TODO: say who the LLM is and what it must do."""

context = """TODO: the labels, rules and facts the LLM needs."""

examples = """TODO: a few examples of input and the exact output you want."""

output_format = """TODO: the exact JSON the LLM must return."""


def build_prompt(text, candidates):
    numbered = ""
    number = 1
    for post in candidates:
        numbered = numbered + str(number) + ". " + post["text"] + "\n"
        number += 1
    prompt = f"""<instruction>{instruction}</instruction>
<context>{context}</context>
<examples>{examples}</examples>
<output_format>{output_format}</output_format>
<query>Posts:
{numbered}New post: {text}
Output:</query>"""
    return prompt


def find_duplicate(text, need_type, kind, places, posts):
    # TODO: write this function. The docstring at the top of this file is the contract.
    # 1. The candidates are the earlier posts that are not duplicates themselves, with the same need_type
    #    and kind, at the same place (same_place from utils). If there are none, return
    #    {"duplicate_of": None}.
    # 2. build_prompt(text, candidates), call
    #    ollama.generate(model="llama3.2", prompt=prompt, format="json", options={"num_predict": 500}),
    #    and read the answer with read_json. Ask for one key, post: 0 if no candidate is the same
    #    situation, 1 for the first candidate, and so on. Ask again (up to 3 tries), then raise ValueError.
    # 3. Return {"duplicate_of": the id of that candidate, or None}.
    raise NotImplementedError("find_duplicate is not written yet")


if __name__ == "__main__":
    posts = [{"id": 1, "duplicate_of": None, "need_type": "rescue", "kind": "request",
              "places": ["Rue 4"], "text": "Family trapped under a house, Rue 4"}]
    print(find_duplicate("Please help, family stuck under a house on Rue 4", "rescue", "request", ["Rue 4"], posts))

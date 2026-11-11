"""Phase 2 team tool: writes one area's section of the situation report.

Function: write_section(area_name, post_texts)

Input:
    area_name (str): the area.
    post_texts (list of str): that area's posts, with personal details hidden.
    Sample: "Delmas 60", ["We are 200 families in Delmas 60 with no water."]

Output (str): the draft section, as short sentences.
    Sample: "200 families in Delmas 60 have no water."

Fact Checking checks every sentence of the section against the posts before a coordinator sees it.
Raises ValueError if the LLM's answer can't be used.
"""
import ollama

# This lets the file work both as "python3 llm/report_writer.py" and as "from llm.report_writer import ...".
if __package__:
    from .utils import read_json
else:
    from utils import read_json

instruction = """TODO: say who the LLM is and what it must do."""

context = """TODO: the labels, rules and facts the LLM needs."""

examples = """TODO: a few examples of input and the exact output you want."""

output_format = """TODO: the exact JSON the LLM must return."""


def build_prompt(area_name, post_texts):
    posts = ""
    for text in post_texts:
        posts = posts + text + "\n"
    prompt = f"""<instruction>{instruction}</instruction>
<context>{context}</context>
<examples>{examples}</examples>
<output_format>{output_format}</output_format>
<query>Area: {area_name}
Posts:
{posts}Output:</query>"""
    return prompt


def write_section(area_name, post_texts):
    # TODO: write this function. The docstring at the top of this file is the contract.
    # 1. build_prompt(area_name, post_texts), call
    #    ollama.generate(model="llama3.2", prompt=prompt, format="json", options={"num_predict": 500}),
    #    and read the answer with read_json. Ask for one key, section: short sentences that use only
    #    facts from the posts. Ask again (up to 3 tries) if it is missing or empty, then raise ValueError.
    # 2. Return the section as a string (not a dict).
    raise NotImplementedError("write_section is not written yet")


if __name__ == "__main__":
    print(write_section("Delmas 60", ["We are 200 families in Delmas 60 with no water."]))

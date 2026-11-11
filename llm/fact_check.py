"""RD.C Fact Checking: checks each sentence of a situation report against the posts.

Function: check_report(report, posts)

Input:
    report (str): the draft report in English.
    posts (list of dict): the posts the report is based on, each with id (int) and text (str).
    Sample: "Families in Delmas 60 need water. A clinic opened in Delmas.",
            [{"id": 4, "text": "We are 200 families in Delmas 60 with no water."}]

Output (dict):
    claims (list of dict): one for each sentence, with:
        claim (str): the sentence.
        status (str): supported if a post states the same fact, otherwise not_found.
        post_ids (list of int): the ids of the posts that state the fact ([] if not_found).
    Sample: {"claims": [{"claim": "Families in Delmas 60 need water.", "status": "supported", "post_ids": [4]},
                        {"claim": "A clinic opened in Delmas.", "status": "not_found", "post_ids": []}]}

Raises ValueError if the LLM's answer can't be used.
Test it: python3 llm/fact_check.py      Score it: python3 score.py fact_check
"""
import ollama

# This lets the file work both as "python3 llm/fact_check.py" and as "from llm.fact_check import ...".
if __package__:
    from .utils import split_sentences, read_json
else:
    from utils import split_sentences, read_json

instruction = """TODO: say who the LLM is and what it must do."""

context = """TODO: the labels, rules and facts the LLM needs."""

examples = """TODO: a few examples of input and the exact output you want."""

output_format = """TODO: the exact JSON the LLM must return."""


def build_prompt(sentence, posts):
    numbered = ""
    for post in posts:
        numbered = numbered + "#" + str(post["id"]) + ": " + post["text"] + "\n"
    prompt = f"""<instruction>{instruction}</instruction>
<context>{context}</context>
<examples>{examples}</examples>
<output_format>{output_format}</output_format>
<query>Posts:
{numbered}Sentence: {sentence}
Output:</query>"""
    return prompt


def check_report(report, posts):
    # TODO: write this function. The docstring at the top of this file is the contract.
    # 1. Split the report with split_sentences.
    # 2. For each sentence, find the ids of the posts that state the same fact. A sentence copied word
    #    for word from a post is supported by that post: no LLM call is needed. Otherwise
    #    build_prompt(sentence, posts), call
    #    ollama.generate(model="llama3.2", prompt=prompt, format="json", options={"num_predict": 500}),
    #    and read the answer with read_json. Ask for one key, post_ids (a list of ids from posts).
    #    Ask again (up to 3 tries) if it is not such a list, then raise ValueError.
    # 3. status is "supported" if post_ids is not empty, otherwise "not_found".
    # 4. Return {"claims": [...]}, one dict for each sentence.
    # A helper function such as check_sentence(sentence, posts) keeps check_report short.
    raise NotImplementedError("check_report is not written yet")


if __name__ == "__main__":
    report = input("Report: ")
    posts = [{"id": 4, "text": "We are 200 families in Delmas 60 with no water."},
             {"id": 7, "text": "The road to Jacmel is open again."}]
    print(check_report(report, posts))

"""Scores one tool on the 10 given cases in data/cases.json and on your own cases. Do not change this file.

Run from the project folder:
    python3 score.py sorter            the 10 given cases, then yours
    python3 score.py sorter given      the 10 given cases only
    python3 score.py sorter mine       your cases only
    python3 score.py sorter 3          given case 3 only
    python3 score.py sorter mine 3     your case 3 only
Tools: sorter, privacy, fact_check, details, language
Your cases are in data/my_cases/<tool>.json, such as data/my_cases/sorter.json. Write 30 of them.
"""
import json
import sys

from llm.utils import load_data, split_sentences

GOAL = 30         # write 30 of your own, for 40 in all


def check_sorter(case):
    from llm.sorter import sort_post
    answer = sort_post(case["english"])
    expected = case["expected"]["need_type"]
    return answer["need_type"] == expected, f"need_type {answer['need_type']!r}, expected {expected!r}"


def check_privacy(case):
    from llm.privacy import redact
    keep = case["privacy"]["must_keep"]
    # Test 1: the post alone has nothing to hide, so the place words must stay.
    plain = redact(case["english"])["redacted_text"]
    # Test 2: the post with a made-up contact line: hide the name, number and email, keep the place words.
    text = redact(case["privacy"]["text"])["redacted_text"]
    shown = []
    for item in case["privacy"]["must_hide"]:
        if item in text:
            shown.append(item)
    kept_plain = 0
    kept = 0
    for word in keep:
        if word.lower() in plain.lower():
            kept_plain += 1
        if word.lower() in text.lower():
            kept += 1
    ok = not shown and kept_plain * 2 >= len(keep) and kept * 2 >= len(keep)
    return ok, (f"still shown: {shown}; place words kept {kept_plain} and {kept} of {len(keep)} "
                f"-> {plain!r} | {text!r}")


def check_fact_check(case):
    from llm.fact_check import check_report
    test = case["fact_check"]
    answer = check_report(test["report"], test["posts"])
    got = []
    for claim in answer["claims"]:
        got.append({"status": claim["status"], "post_ids": sorted(claim["post_ids"])})
    return got == test["expected"], f"got {got}, expected {test['expected']}"


def check_details(case):
    from llm.details import extract_details
    answer = extract_details(case["english"])
    expected = case["expected"]["kind"]
    return answer["kind"] == expected, f"kind {answer['kind']!r}, expected {expected!r}; places {answer['places']}"


def check_language(case):
    from llm.language import process_post
    answer = process_post(case["post"])
    expected = case["expected"]["translated"]
    english = answer["english"].lower()
    missing_numbers = []
    words = 0
    kept_words = 0
    for word in case["expected"]["kept_words"]:
        if word.isdigit():
            if word not in english:
                missing_numbers.append(word)
        else:
            words += 1
            if word.lower() in english:
                kept_words += 1
    ok = answer["translated"] == expected and not missing_numbers and kept_words * 2 >= words
    return ok, (f"translated {answer['translated']} ({answer['language']}), expected {expected}; "
                f"names kept {kept_words} of {words}, numbers lost {missing_numbers} -> {answer['english']!r} "
                f"| source English: {case['english']!r}")


CHECKS = {"sorter": check_sorter, "privacy": check_privacy, "fact_check": check_fact_check,
          "details": check_details, "language": check_language}


# ---------------------------------------------------------------------------
# Your own cases: data/my_cases/<tool>.json, a list of cases with these fields.
# "text" is text in quote marks, and a list of words means the value must be one of them.
# Any other field, such as "note" or "source", is allowed and not used.

NEED_TYPES = ["rescue", "medical", "food_water", "shelter", "infrastructure", "other"]
KINDS = ["request", "offer", "report"]
FIELDS = {
    "sorter": {"post": "text", "need_type": NEED_TYPES},
    "privacy": {"text": "text", "must_hide": "list of text", "must_keep": "list of text"},
    "fact_check": {"report": "text", "posts": "list", "claims": "list"},
    "details": {"post": "text", "kind": KINDS},
    "language": {"post": "text", "translated": "true or false", "keep": "list of text"},
}


def extra_problems(tool, case):
    """Checks that need more than one field."""
    problems = []
    if tool == "fact_check":
        ids = []
        for post in case["posts"]:
            if not isinstance(post, dict) or not isinstance(post.get("id"), int) \
                    or not isinstance(post.get("text"), str):
                problems.append('each post must be {"id": a number, "text": "..."}')
            else:
                ids.append(post["id"])
        for claim in case["claims"]:
            if not isinstance(claim, dict) or claim.get("status") not in ["supported", "not_found"] \
                    or not isinstance(claim.get("post_ids"), list):
                problems.append('each claim must be {"status": "supported" or "not_found", "post_ids": [...]}')
            elif any(post_id not in ids for post_id in claim["post_ids"]):
                problems.append(f"the post_ids {claim['post_ids']} must be ids of your posts {ids}")
            elif (claim["status"] == "supported") != bool(claim["post_ids"]):
                problems.append('a "supported" claim needs post ids, and a "not_found" claim needs []')
        sentences = len(split_sentences(case["report"]))
        if len(case["claims"]) != sentences:
            problems.append(f'the report has {sentences} sentences, so "claims" needs {sentences} claims')
    return problems


def mine_sorter(case):
    return check_sorter({"english": case["post"], "expected": {"need_type": case["need_type"]}})


def mine_privacy(case):
    from llm.privacy import redact
    text = redact(case["text"])["redacted_text"]
    shown = [item for item in case["must_hide"] if item in text]
    kept = [word for word in case["must_keep"] if word.lower() in text.lower()]
    ok = not shown and len(kept) * 2 >= len(case["must_keep"])
    return ok, f"still shown: {shown}; place words kept {len(kept)} of {len(case['must_keep'])} -> {text!r}"


def mine_fact_check(case):
    expected = [{"status": claim["status"], "post_ids": sorted(claim["post_ids"])} for claim in case["claims"]]
    return check_fact_check({"fact_check": {"report": case["report"], "posts": case["posts"],
                                            "expected": expected}})


def mine_details(case):
    return check_details({"english": case["post"], "expected": {"kind": case["kind"]}})


def mine_language(case):
    from llm.language import process_post
    answer = process_post(case["post"])
    english = answer["english"].lower()
    lost_numbers = [word for word in case["keep"] if word.isdigit() and word not in english]
    names = [word for word in case["keep"] if not word.isdigit()]
    kept = [word for word in names if word.lower() in english]
    ok = answer["translated"] == case["translated"] and not lost_numbers and len(kept) * 2 >= len(names)
    return ok, (f"translated {answer['translated']} ({answer['language']}), expected {case['translated']}; "
                f"names kept {len(kept)} of {len(names)}, numbers lost {lost_numbers} -> {answer['english']!r}")


MINE = {"sorter": mine_sorter, "privacy": mine_privacy, "fact_check": mine_fact_check,
        "details": mine_details, "language": mine_language}


# ---------------------------------------------------------------------------
# Reading and checking your own cases

def field_problem(value, kind):
    """Returns what is wrong with one field of your case, or "" if nothing is wrong."""
    if isinstance(kind, list):
        if value not in kind:
            return "must be one of: " + ", ".join(json.dumps(choice) for choice in kind)
    elif kind == "text":
        if not isinstance(value, str) or not value.strip():
            return "must be text in double quotes, and not empty"
    elif kind == "list of text":
        if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
            return 'must be a list of text, such as ["a", "b"], or [] for none'
    elif kind == "true or false":
        if not isinstance(value, bool):
            return "must be true or false, with no quote marks"
    elif kind == "list":
        if not isinstance(value, list):
            return "must be a list, in [ ]"
    return ""


def case_problems(tool, number, case):
    """Returns a list of the mistakes in one of your cases."""
    if not isinstance(case, dict):
        return [f"your case {number}: must be {{ ... }}, like the sample case"]
    problems = []
    for name, kind in FIELDS[tool].items():
        if name not in case:
            problems.append(f'your case {number}: has no "{name}"')
        elif field_problem(case[name], kind):
            problems.append(f'your case {number}: "{name}" {field_problem(case[name], kind)}')
    if not problems:
        for problem in extra_problems(tool, case):
            problems.append(f"your case {number}: {problem}")
    return problems


def load_my_cases(tool):
    """Reads your cases from data/my_cases/<tool>.json and numbers them 1, 2, 3, ...
    If the file has a mistake, it prints what is wrong and returns None."""
    name = f"my_cases/{tool}.json"
    try:
        cases = load_data(name)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as error:
        print(f"data/{name} is not valid JSON: {error.msg}, on line {error.lineno}.")
        print("Look for a missing comma, quote mark or bracket on that line or the line before it.")
        return None
    if not isinstance(cases, list):
        print(f"data/{name} must be a list of cases: it starts with [ and ends with ].")
        return None
    problems = []
    for number, case in enumerate(cases, start=1):
        problems += case_problems(tool, number, case)
    if problems:
        print(f"data/{name} has mistakes:")
        for problem in problems:
            print("  " + problem)
        return None
    for number, case in enumerate(cases, start=1):
        case["id"] = number
    return cases


def run(check, cases, label):
    """Runs one check on each case and prints PASS or FAIL.
    Returns how many passed, or None if the tool is not written yet."""
    passed = 0
    for case in cases:
        try:
            ok, note = check(case)
        except NotImplementedError as error:
            print(error)
            return None
        except Exception as error:
            ok, note = False, f"error: {error}"
        if ok:
            passed += 1
            print(f"{label} {case['id']}: PASS  {note}")
        else:
            print(f"{label} {case['id']}: FAIL  {note}")
    return passed


def main():
    args = sys.argv[1:]
    if not args or args[0] not in CHECKS:
        print("Usage: python3 score.py TOOL [given | mine] [NUMBER]   TOOL is one of:", ", ".join(CHECKS))
        return
    tool = args[0]
    which = "all"
    if len(args) > 1 and args[1] in ("given", "mine"):
        which = args[1]
        args = args[:1] + args[2:]
    number = None
    if len(args) > 1:
        number = args[1]
        if which == "all":
            which = "given"

    given = []
    mine = []
    if which in ("all", "given"):
        given = load_data("cases.json")["cases"]
    if which in ("all", "mine"):
        mine = load_my_cases(tool)
        if mine is None:
            return
    count_mine = len(mine)
    if number is not None:
        given = [case for case in given if str(case["id"]) == number]
        mine = [case for case in mine if str(case["id"]) == number]
        if not given and not mine:
            if which == "given":
                print(f"There is no given case {number}.")
            else:
                print(f"There is no case {number} in data/my_cases/{tool}.json.")
            return
    if which == "mine" and not mine:
        print(f"data/my_cases/{tool}.json has no cases yet.")
        return

    passed_given = 0
    passed_mine = 0
    if given:
        passed_given = run(CHECKS[tool], given, "Case")
        if passed_given is None:
            return
    if mine:
        if given:
            print(f"Given cases: {passed_given} of {len(given)}")
        passed_mine = run(MINE[tool], mine, "Your case")
        if passed_mine is None:
            return
        if given:
            print(f"Your cases: {passed_mine} of {len(mine)}")
    print(f"Score: {passed_given + passed_mine} of {len(given) + len(mine)}")
    if which != "given" and number is None and count_mine < GOAL:
        print(f"You have {count_mine} of your {GOAL} cases in data/my_cases/{tool}.json.")


if __name__ == "__main__":
    main()

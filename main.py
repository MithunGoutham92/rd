"""ReliefDesk: joins the five tools into one assistant for disaster-relief coordinators.

Run from the project folder:  python3 main.py
Type a post, "demo" to log the 10 posts in data/cases.json, "report" for the situation report, or "quit".
Posts are saved in data/posts.json. Nothing is sent to responders.
"""
from llm.details import extract_details
from llm.duplicates import find_duplicate
from llm.fact_check import check_report
from llm.language import process_post
from llm.privacy import redact
from llm.report_writer import write_section
from llm.sorter import sort_post
from llm.utils import load_data, save_data

UNKNOWN_AREA = "Place not given"


def area_name(post):
    """The area of a post is its first place."""
    name = UNKNOWN_AREA
    if post["places"]:
        name = post["places"][0]
    return name


def handle_post(message):
    """Runs one post through every tool. The post is saved only if every step works."""
    posts = load_data("posts.json")
    language = process_post(message)
    redacted = redact(language["english"])
    text = redacted["redacted_text"]
    sorted_post = sort_post(text)
    details = extract_details(text)
    duplicate = find_duplicate(text, sorted_post["need_type"], details["kind"], details["places"], posts)
    post = {
        "id": len(posts) + 1,
        "text": text,
        "language": language["language"],
        "need_type": sorted_post["need_type"],
        "urgency": sorted_post["urgency"],
        "kind": details["kind"],
        "places": details["places"],
        "needs": details["needs"],
        "amounts": details["amounts"],
        "times": details["times"],
        "duplicate_of": duplicate["duplicate_of"],
    }
    posts.append(post)
    save_data("posts.json", posts)

    line = "logged #" + str(post["id"]) + ": "
    if post["duplicate_of"]:
        line = line + "same as #" + str(post["duplicate_of"])
    else:
        line = line + ", ".join([post["need_type"], post["urgency"], post["kind"], area_name(post)])
    return line


def group_by_area(posts):
    """Returns a dict: area name -> list of posts in that area (duplicates left out)."""
    areas = {}
    for post in posts:
        if post["duplicate_of"] is None:
            area = area_name(post)
            if area not in areas:
                areas[area] = []
            areas[area].append(post)
    return areas


def build_report():
    """Writes the draft situation report, one area at a time. Sentences no post backs up are left out."""
    posts = load_data("posts.json")
    lines = ["DRAFT situation report, for coordinator review. Not sent to anyone."]
    areas = group_by_area(posts)
    for area in areas:
        post_texts = []
        evidence = []
        for post in areas[area]:
            post_texts.append(post["text"])
            evidence.append({"id": post["id"], "text": post["text"]})
        section = write_section(area, post_texts)
        checked = check_report(section, evidence)
        lines.append("")
        lines.append(area.upper())
        for claim in checked["claims"]:
            if claim["status"] == "supported":
                ids = []
                for post_id in claim["post_ids"]:
                    ids.append("#" + str(post_id))
                lines.append("- " + claim["claim"] + " (" + ", ".join(ids) + ")")
            else:
                lines.append("- [left out, no post backs it up] " + claim["claim"])
    return "\n".join(lines)


def run(command):
    try:
        if command.lower() == "report":
            print(build_report())
        else:
            print(handle_post(command))
    except NotImplementedError as error:
        print("Not ready yet:", error)
    except (ValueError, ConnectionError) as error:
        print("Sorry, we couldn't process this. Please try again.", error)


def main():
    print("ReliefDesk. Type a post, demo, report, or quit. Nothing is sent to responders.")
    while True:
        message = input("\n> ").strip()
        if message.lower() in ("quit", "exit"):
            break
        if not message:
            continue
        if message.lower() == "demo":
            for case in load_data("cases.json")["cases"]:
                print("\n> " + case["post"])
                run(case["post"])
            continue
        run(message)


if __name__ == "__main__":
    main()

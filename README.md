# ReliefDesk

ReliefDesk helps disaster-relief coordinators. People text the ReliefDesk number in different languages. The assistant translates each message, hides personal details names and phone numbers if present, so that the later tools never see them, sorts the need, pulls out the places, needs, amounts and times, deduplicates messages about the same incident, and continuously updates a situation report for the disaster relief personnel.

Every LLM call runs on your own computer using llama3.2 for consistency across teams and teammates.

## Goals

The assistant receives messages as JSON objects that look like this:

```json
[
  {
    "time": "2027-01-12 08:40",
    "sender": "555-0142",
    "location": {
      "latitude": 47.6097,
      "longitude": -122.3331,
      "accuracy_m": 800
    },
    "message": "We are 40 people trapped in Walmart with no clean water since the storm."
  }
]
```

`location` is where the mobile network estimates the sender's phone , not a place named in the
message. `accuracy_m` is the radius in metres: the phone can be anywhere within that distance of the point. `location` is `null` if the network cannot estimate the location. 

The assistant must:

1. Write a **situation report** that gives the **needs** and the **damage**. Every fact must come from the messages. No facts may come from the LLM's trained memory.
2. **Report each incident only one time.** Many people will report the same incident, in different words and in different
   languages. The report deduplicates and reports the incident only one time, but says how many messages report it. 
3. **Never ignore a single message.** An incident that only one message reports must still be in the report.
4. **Handle unusual messages** that are irrelevant (possibly texted by mistake or meant to be spam to harm the disaster relief efforts). 
5. **Keep an unbelievable message out of the report.** A message that is hard to believe must not go directly into the report but must be shared **separately**, as a **side note for the authorities**, so that they know about it. Your team decides how the assistant should do this.
6. **Keep personal details out of the report.** Names, phone numbers and email addresses should not appear in the report or
   the side note. The assistant still saves each message with its `sender` in `data/posts.json`, so that a human can
   contact the sender later based on the message ID (see the example below).

## Situation report

The assistant writes the report to `data/report.txt`. The report starts with one line that says
it is a draft for coordinator review. Then it has one section for each area:

| Part | What it holds |
|---|---|
| Area name | The place, such as `WALMART`. Messages with no place go under `PLACE NOT GIVEN`. |
| Needs | What people in this area need: water, food, shelter, medical help, rescue and so on, with amounts when the messages give them. |
| Damage | What the messages say is damaged or lost: houses, roads, bridges, power and so on. |

For example:

```
DRAFT situation report, for coordinator review. Not sent to anyone.

WALMART
Needs: About 40 people are trapped with no clean water. (12 messages: #3, #5, #8)
Damage: The bridge on Route 2 is down. (1 message: #15)
```


## Step 1: set up the team repository

1. **The team chooses one GitHub repository owner.** This person should:
   1. Make the team repository as a copy of this repository (for example, click **Fork** on this repository's GitHub page).
   2. On the team repository, add every teammate as a collaborator. To do this, each teammate must make a free GitHub account on https://github.com (if they do not have one) and share their user name with the repository owner. Each teammate accepts the email invitation.
   3. Send the team repository's URL to the team.
2. **Each person** clones the team repository onto their own computer. Each person copies their own tool file (such as `llm/sorter.py`) into the cloned folder. This replaces the file of the same name.
3. **Each person** runs their tool to check that it still works, then pushes their work to the team's GitHub repository, following the guidance shared in class. **Each person must have their own commits and at least one merge under their own GitHub account in the team repository** (see the rubric below).

## Step 2: build the project together

Your objective is described (it is vague intentionally) in "Goals" at the start of this README. The team should define the work to be done and divide this work as the team sees fit (see "Peer evaluation" in the rubric).

Plan to support each other and to teach each other what you are not familiar with. Agentic tools such as Claude Code and OpenAI Codex are permitted, but each person must be able to describe the code they committed in their own words.

## Step 3: try your assistant on the kinds of messages that will be tested

Before you hand in, check that your assistant works as it should. Cidney will evaluate the project with test messages of the kinds below. She will give each as a JSON file in the format shown in "Goals", and will run your `main.py` on it. Write your own test file in the same format.

- **3 repeated incidents:** one incident in **20** messages, another in **15** messages and another in **10** messages. The messages about
  each incident use different words and possibly different languages.
- **4 single incidents:** four different incidents, each in only one message. They must not be ignored.
- **2 unusual messages:** for example, "Is the airport open for tourists this weekend?"
- **1 unbelievable message:** for example, "A wave as tall as a mountain hit the town last night and nobody saw it."

Cidney then reads your `data/report.txt` and your side note. Start the run with `data/posts.json` as an empty list (`[]`).

## Rubric
**Peer evaluation (50%):** you will evaluate each of your teammates (not yourself) through the following questions.
Your responses are confidential and will never be shared with teammates under any circumstance.

| Question | Answer |
|---|---|
| Name | Their full name |
| Proactively seeks solutions, moving the team forward | Number: 1–5 Likert scale |
| Communicates respectfully | Number: 1–5 Likert scale |
| Can be trusted to complete their assigned task on time | Number: 1–5 Likert scale |
| Knows how and when to ask for help | Number: 1–5 Likert scale |
| Strengths | What does this teammate do particularly well? Give at least one specific detail. |
| Weaknesses | What are some specific ways this teammate could improve their contribution? Be constructive. |

The Likert scale is as follows:
- 5: strongly agree - 4: somewhat agree - 3: neutral - 2: somewhat disagree - 1: strongly disagree

**Submission (50%), 13 points:**

| Part | Points | Who | Full points when |
|---|---|---|---|
| Git merge | 1 | Each person | In the team repository's history, you have your own commits and at least one merge (a `git pull` that joined teammates' commits with yours). |
| Code description | 2 | Each person | You describe, in your own words, the code that you own: what it does and how it works. |
| 3 repeated incidents (20, 15, 10 messages) | 3 (1 each) | Whole team, shared equally | The incident is in the report one time, in the right area, with its needs and damage. It is not repeated for each message, and every fact comes from the messages. |
| 4 single incidents | 4 (1 each) | Whole team, shared equally | The incident is in the report. It is not left out, and it is not joined with a different incident. |
| 2 unusual messages | 2 (1 each) | Whole team, shared equally | The assistant does not stop with an error and does not make up facts. The message is handled in a sensible way (for example, under `PLACE NOT GIVEN`, or not in the report when it states no need or damage). |
| 1 unbelievable message | 1 | Whole team, shared equally | The message is not in the report. It is in the separate side note for the authorities, and your team's README says where to find it. |

Everyone on the team gets the same points for the test messages. The Git merge point and the code description points are for each person.

License
`data/cases.json`: Disaster Response Messages from https://github.com/rmunro/disaster_response_messages.git

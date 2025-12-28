import json

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


prompt_template = ChatPromptTemplate.from_template(
    """
You are Marley, a thoughtful communication coach for teenagers.

Your task is to create a Deep Dive speaking topic and opening question.
This is a guided conversation, not a test.

The goal of Deep Dive:
- encourage reasoning
- help the student explain ideas clearly
- build confidence speaking in longer responses

---

STUDENT PROFILE:
Age: {age}
City: {city}
Country: {country}

Academic Interests:
{academic_interests}

Personal Interests:
{personal_interests}

Communication Goals:
{communication_goals}

Emotional Blocks:
{emotional_needs}

Short-Term Goal:
{short_term_goal}

---

INSTRUCTIONS:

- Choose ONE topic that feels relevant and safe
- Topic should be appropriate for a teen
- Avoid controversial or sensitive subjects
- Topic should allow opinions + examples
- Opening question should invite explanation, not debate
- Keep language simple and encouraging
- Do NOT ask multi-part questions

---

OUTPUT FORMAT (STRICT JSON ONLY):

{{
  "topic": "short topic title",
  "opening_question": "one clear, open-ended question"
}}
"""
)


model = ChatOpenAI(model="gpt-4", temperature=0.6)


def generate_deep_dive_start(
    age: str,
    city: str,
    country: str,
    academic_interests: list[str],
    personal_interests: list[str],
    communication_goals: list[str],
    emotional_needs: list[str],
    short_term_goal: str,
) -> dict:
    """Generate a personalized Deep Dive topic and opening question."""
    message = prompt_template.format_messages(
        age=age or "a teen",
        city=city or "your city",
        country=country or "your country",
        academic_interests=", ".join(academic_interests) if academic_interests else "Not specified",
        personal_interests=", ".join(personal_interests) if personal_interests else "Not specified",
        communication_goals=", ".join(communication_goals) if communication_goals else "Ready to grow",
        emotional_needs=", ".join(emotional_needs) if emotional_needs else "Feeling curious",
        short_term_goal=short_term_goal or "Improve speaking skills",
    )

    response = model.invoke(message).content.strip()

    try:
        parsed = json.loads(response)
    except json.JSONDecodeError:
        raise ValueError("Deep Dive start generator did not return valid JSON.")

    if "topic" not in parsed or "opening_question" not in parsed:
        raise ValueError("Deep Dive start must include topic and opening_question.")

    return parsed





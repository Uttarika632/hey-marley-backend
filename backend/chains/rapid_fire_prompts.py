import json

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


prompt_template = ChatPromptTemplate.from_template(
    """
You are Marley, a friendly communication coach for teenagers.

Your task is to generate EXACTLY 3 Rapid Fire sentence starters.
These will be used in a 30-second speaking warm-up game.

The goal of Rapid Fire:
- help the teen start speaking immediately
- reduce hesitation
- feel natural and low-pressure
- warm them up for deeper speaking tasks

Use the student's personalization data to make the prompts feel familiar and relevant,
but keep them light and easy.

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

PROMPT RULES (VERY IMPORTANT):
- Each prompt must be a SENTENCE STARTER (not a question)
- Each prompt must feel easy to continue speaking from
- Use familiar contexts: school life, daily routines, interests, city culture
- Avoid heavy topics, debates, or abstract theory
- Do NOT give instructions
- Do NOT mention skills, scores, or improvement
- Keep language teen-friendly and simple
- Each prompt should end with “because…”, “when…”, or similar

OUTPUT FORMAT (STRICT):
Return ONLY a JSON array with exactly 3 strings.
"""
)


model = ChatOpenAI(model="gpt-4", temperature=0.52)


def generate_rapid_fire_prompts(
    age: str,
    city: str,
    country: str,
    academic_interests: list[str],
    personal_interests: list[str],
    communication_goals: list[str],
    emotional_needs: list[str],
    short_term_goal: str,
) -> list[str]:
    """Generate exactly three personalized Rapid Fire sentence starters."""
    message = prompt_template.format_messages(
        age=age or "a teen",
        city=city or "your city",
        country=country or "your country",
        academic_interests=", ".join(academic_interests) or "Not specified",
        personal_interests=", ".join(personal_interests) or "Not specified",
        communication_goals=", ".join(communication_goals) or "Ready to grow",
        emotional_needs=", ".join(emotional_needs) or "Feeling curious",
        short_term_goal=short_term_goal or "Share something simple",
    )

    response = model.invoke(message).content.strip()

    try:
        parsed = json.loads(response)
    except json.JSONDecodeError:
        raise ValueError("Rapid Fire prompt generator did not return valid JSON.")

    if not isinstance(parsed, list) or len(parsed) != 3:
        raise ValueError("Rapid Fire generator must return exactly 3 prompts.")

    return parsed






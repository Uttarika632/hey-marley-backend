import json

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


prompt_template = ChatPromptTemplate.from_template(
    """
You are Marley, a friendly communication coach for teenagers.

Your task is to generate EXACTLY 6 Word Bomb words.
These will be used in a 60-second speaking challenge where a new word appears every 10 seconds.

The goal of Word Bomb:
- challenge the teen to keep speaking while adapting to new words
- test verbal agility and quick thinking
- feel fun and achievable, not stressful

Use the student's personalization data to make the words feel relevant,
but keep them simple and easy to incorporate into speech.

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

WORD RULES (VERY IMPORTANT):
- Each word must be a SINGLE WORD (no phrases)
- Words should be concrete nouns, verbs, or adjectives
- Mix familiar words with slightly challenging ones
- Use words related to their interests, city, or daily life
- Avoid abstract concepts that are hard to speak about
- Avoid controversial or sensitive topics
- Keep words teen-friendly and simple
- Words should be easy to weave into a flowing sentence

OUTPUT FORMAT (STRICT):
Return ONLY a JSON array with exactly 6 strings.

Example:
["breakfast", "cricket", "monsoon", "guitar", "friendship", "adventure"]

Do not include anything outside the JSON array.
"""
)


model = ChatOpenAI(model="gpt-4", temperature=0.6)


def generate_word_bomb_words(
    age: str,
    city: str,
    country: str,
    academic_interests: list[str],
    personal_interests: list[str],
    communication_goals: list[str],
    emotional_needs: list[str],
    short_term_goal: str,
) -> list[str]:
    """Generate exactly six personalized Word Bomb words."""
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
        raise ValueError("Word Bomb generator did not return valid JSON.")

    if not isinstance(parsed, list) or len(parsed) != 6:
        raise ValueError("Word Bomb generator must return exactly 6 words.")

    return parsed





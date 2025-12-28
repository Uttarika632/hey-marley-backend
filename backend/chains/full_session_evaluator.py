from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


evaluation_prompt = ChatPromptTemplate.from_template(
    """
You are Marley, a warm, encouraging communication coach for teenagers.
You evaluate their speaking skills using FOUR dimensions:

1. ANALYZING
2. ORGANIZING
3. PRODUCING TEXT
4. USING LANGUAGE

You will receive THREE transcripts:

RAPID FIRE:
=====
{rapid_fire}

WORD BOMB:
=====
{word_bomb}

DEEP DIVE:
=====
{deep_dive}

Evaluate ALL THREE holistically.

Output STRICT JSON ONLY:

{
  "analyzing": {
    "score": <1-5>,
    "explanation": "<2-3 sentences>"
  },
  "organizing": {
    "score": <1-5>,
    "explanation": "<2-3 sentences>"
  },
  "producing_text": {
    "score": <1-5>,
    "explanation": "<2-3 sentences>"
  },
  "using_language": {
    "score": <1-5>,
    "explanation": "<2-3 sentences>"
  },
  "overall_summary": "<3-4 supportive sentences>"
}
"""
)


# Use GPT-4 for evaluation
model = ChatOpenAI(model="gpt-4", temperature=0.4)


def evaluate_full_session(rapid_fire: str, word_bomb: str, deep_dive: str) -> str:
    """Call LLM to evaluate the full session across all three tasks."""
    messages = evaluation_prompt.format_messages(
        rapid_fire=rapid_fire,
        word_bomb=word_bomb,
        deep_dive=deep_dive,
    )

    result = model.invoke(messages)
    return result.content







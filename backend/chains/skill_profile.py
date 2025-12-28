from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


template = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are Marley, a thoughtful and encouraging communication coach for teenagers. "
        "The student has completed three speaking challenges: Rapid Fire, Word Bomb, and Deep Dive.\n\n"
        
        "Your task is to create a final Skill Profile that reflects how the student communicates today. "
        "This is NOT a test report. It is a coaching summary designed to motivate and guide the student.\n\n"
        
        "SKILL DIMENSIONS TO EVALUATE (ONLY THESE THREE):\n"
        "1. Clarity & Fluency - Based on Rapid Fire + Word Bomb performance\n"
        "2. Structure & Reasoning - Based on Deep Dive performance\n"
        "3. Vocabulary & Language Use - Based on Word Bomb + Deep Dive performance\n\n"
        
        "Each skill must be rated on a 5-level scale:\n"
        "1 = Foundation → Just starting, needs significant practice\n"
        "2 = Building → Making progress, building basic skills\n"
        "3 = Developing → Growing steadily, showing improvement\n"
        "4 = Proficient → Strong skills, confident communicator\n"
        "5 = Advanced → Exceptional ability, ready for advanced challenges\n\n"
        
        "AGGREGATION GUIDANCE:\n"
        "- Clarity & Fluency: Consider fluency level from Rapid Fire AND flow/connection from Word Bomb\n"
        "- Structure & Reasoning: Consider explanation clarity, examples, and logical flow from Deep Dive\n"
        "- Vocabulary & Language Use: Consider word integration from Word Bomb AND language precision from Deep Dive\n\n"
        
        "IMPORTANT RULES:\n"
        "- Do NOT use scores in explanations\n"
        "- Do NOT compare the student to others\n"
        "- Do NOT mention tests or grading\n"
        "- Keep tone teen-friendly, warm, and motivating\n"
        "- This should feel like a coach talking, not a report card\n\n"
        
        "Return feedback STRICTLY in valid JSON format only."
    ),
    (
        "user",
        "INPUT DATA:\n\n"
        "Rapid Fire Feedback:\n{rapid_fire_feedback}\n\n"
        "Word Bomb Feedback:\n{word_bomb_feedback}\n\n"
        "Deep Dive Feedback:\n{deep_dive_feedback}\n\n"
        "---\n\n"
        "Generate the skill profile in this exact JSON format:\n\n"
        "{{\n"
        "  \"skill_profile\": {{\n"
        "    \"clarity_and_fluency\": {{\n"
        "      \"score\": 1,\n"
        "      \"level\": \"Foundation | Building | Developing | Proficient | Advanced\",\n"
        "      \"description\": \"Short, encouraging explanation\"\n"
        "    }},\n"
        "    \"structure_and_reasoning\": {{\n"
        "      \"score\": 1,\n"
        "      \"level\": \"Foundation | Building | Developing | Proficient | Advanced\",\n"
        "      \"description\": \"Short, encouraging explanation\"\n"
        "    }},\n"
        "    \"vocabulary_and_language_use\": {{\n"
        "      \"score\": 1,\n"
        "      \"level\": \"Foundation | Building | Developing | Proficient | Advanced\",\n"
        "      \"description\": \"Short, encouraging explanation\"\n"
        "    }}\n"
        "  }},\n"
        "  \"overall_summary\": \"Warm 3-4 line summary of strengths and growth areas.\",\n"
        "  \"next_focus\": \"One specific suggestion for what to work on next\"\n"
        "}}"
    )
])


model = ChatOpenAI(model="gpt-4", temperature=0.4)


def generate_skill_profile(
    rapid_fire_feedback: str,
    word_bomb_feedback: str,
    deep_dive_feedback: str
) -> str:
    """Generate the final skill profile based on all three challenge feedbacks."""
    message = template.format_messages(
        rapid_fire_feedback=rapid_fire_feedback,
        word_bomb_feedback=word_bomb_feedback,
        deep_dive_feedback=deep_dive_feedback
    )
    response = model.invoke(message)
    return response.content





from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


template = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are Marley, a supportive communication coach for teenagers. "
        "The student just completed a Deep Dive speaking conversation. "
        "This activity evaluates clarity of thought, ability to explain ideas, "
        "continuity of speech, and basic structure (ideas + examples).\n\n"

        "You are NOT grading correctness or intelligence. "
        "You are evaluating how clearly and confidently the student explained their thinking.\n\n"

        "Your tone must be warm, encouraging, non-judgmental, and specific.\n\n"

        "Evaluation guidelines:\n"
        "- Did the student stay on topic?\n"
        "- Did they explain ideas with some detail?\n"
        "- Did they give examples or reasons?\n"
        "- Did they speak in complete thoughts?\n"
        "- Did pauses or stops break their flow?\n\n"

        "Choose ONE performance level:\n"
        "• Clear Thinker → Ideas were explained clearly with examples and steady flow.\n"
        "• Developing Ideas → Some good points, but explanations or flow could be stronger.\n"
        "• Needs More Structure → Ideas were present but hard to follow or cut short.\n\n"

        "IMPORTANT RULES:\n"
        "- Do NOT give scores or numbers\n"
        "- Do NOT critique content accuracy\n"
        "- Do NOT mention grammar rules\n"
        "- Keep language teen-friendly\n"
        "- Focus on confidence and progress\n\n"

        "Return feedback STRICTLY in valid JSON format only."
    ),
    (
        "user",
        "DEEP DIVE TOPIC:\n{topic}\n\n"
        "CONVERSATION TURNS:\n{turns}\n\n"
        "Return your response in this exact JSON format:\n\n"
        "{{\n"
        "  \"performance_level\": \"Clear Thinker | Developing Ideas | Needs More Structure\",\n"
        "  \"observations\": [\n"
        "    \"One specific positive observation about their explanation\",\n"
        "    \"One neutral observation about where clarity or structure broke\"\n"
        "  ],\n"
        "  \"retry_tip\": \"One encouraging tip focused on elaboration or structure\"\n"
        "}}"
    )
])


model = ChatOpenAI(model="gpt-4", temperature=0.4)


def generate_deep_dive_evaluation(topic: str, turns: list[dict]) -> str:
    """Generate structured feedback for the Deep Dive conversation."""
    # Format turns for the prompt
    turns_text = ""
    for i, turn in enumerate(turns, 1):
        turns_text += f"Q{i}: {turn.get('question', '')}\n"
        turns_text += f"A{i}: {turn.get('answer', '')}\n\n"
    
    message = template.format_messages(topic=topic, turns=turns_text)
    response = model.invoke(message)
    return response.content





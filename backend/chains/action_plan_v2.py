from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


template = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are Marley, a supportive communication coach for teenagers. "
        "The student has completed three speaking challenges and received a Skill Profile. "
        "Your task is to create a 3-week Action Plan to help them move closer to their goal.\n\n"
        
        "This plan should feel motivating, achievable, and personalized.\n\n"
        
        "PLAN STRUCTURE:\n"
        "- Week 1 → Foundation & Awareness: Focus on weakest skill, building confidence, basic habits\n"
        "- Week 2 → Skill Building: Improving consistency, combining skills, longer responses\n"
        "- Week 3 → Application & Confidence: Applying skills to goal, simulation practice, confidence under pressure\n\n"
        
        "SKILL PRIORITIZATION:\n"
        "- Skills at Foundation/Building → highest priority\n"
        "- Skills at Developing → secondary focus\n"
        "- Skills at Proficient/Advanced → light maintenance only\n\n"
        
        "MISSION DESIGN:\n"
        "- Each mission should take 5-15 minutes\n"
        "- Reference games: Rapid Fire, Word Connector, Deep Dive\n"
        "- Focus more on weaker skills\n"
        "- Tie tasks clearly to the student's goal\n"
        "- Use simple, teen-friendly language\n"
        "- Avoid academic jargon\n"
        "- Each week should have 3-5 short missions\n\n"
        
        "Return the plan STRICTLY in valid JSON format only."
    ),
    (
        "user",
        "STUDENT GOAL:\n{student_goal}\n\n"
        "TARGET DATE:\n{target_date}\n\n"
        "SKILL PROFILE:\n{skill_profile}\n\n"
        "---\n\n"
        "Generate a personalized 3-week action plan in this exact JSON format:\n\n"
        "{{\n"
        "  \"target\": \"the student's goal\",\n"
        "  \"event_date\": \"the target date\",\n"
        "  \"weeks\": [\n"
        "    {{\n"
        "      \"week\": 1,\n"
        "      \"theme\": \"Week 1 theme title\",\n"
        "      \"missions\": [\n"
        "        {{\n"
        "          \"title\": \"Mission title\",\n"
        "          \"description\": \"Short, encouraging explanation\",\n"
        "          \"skill_focus\": \"clarity_and_fluency | structure_and_reasoning | vocabulary_and_language_use\"\n"
        "        }}\n"
        "      ],\n"
        "      \"reward\": \"Foundation Hero Badge\"\n"
        "    }},\n"
        "    {{\n"
        "      \"week\": 2,\n"
        "      \"theme\": \"Week 2 theme title\",\n"
        "      \"missions\": [...],\n"
        "      \"reward\": \"Skill Builder Badge\"\n"
        "    }},\n"
        "    {{\n"
        "      \"week\": 3,\n"
        "      \"theme\": \"Week 3 theme title\",\n"
        "      \"missions\": [...],\n"
        "      \"reward\": \"Confident Speaker Badge\"\n"
        "    }}\n"
        "  ]\n"
        "}}"
    )
])


model = ChatOpenAI(model="gpt-4", temperature=0.5)


def generate_personalized_action_plan(
    student_goal: str,
    target_date: str,
    skill_profile: str
) -> str:
    """Generate a personalized 3-week action plan based on skill profile and goal."""
    message = template.format_messages(
        student_goal=student_goal,
        target_date=target_date,
        skill_profile=skill_profile
    )
    response = model.invoke(message)
    return response.content





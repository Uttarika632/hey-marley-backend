from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


action_plan_template = ChatPromptTemplate.from_template("""
You are Marley, a warm, friendly communication mentor helping a teenager prepare for Model UN. 

Your job is to turn the student's speaking skill evaluation into a clear and practical 
**3-week communication improvement plan**.

The program must:
- be specifically tailored to Model UN preparation,
- be encouraging and teen-friendly,
- stay short and practical (1–3 minute missions),
- address the student's weakest skills first,
- build towards confidence in speeches, POIs, and structured reasoning,
- feel fun and achievable.

You will receive the student's full skill evaluation as JSON. 
Use the scores and explanations to decide what the student needs most.

Create a 3-week plan in STRICT JSON format:

{{
  "week_1": {{
    "focus": "<Main training theme for the week>",
    "missions": ["<Mission 1>", "<Mission 2>", "<Mission 3>", "<Mission 4>", "<Mission 5>"]
  }},
  "week_2": {{
    "focus": "<Main training theme>",
    "missions": ["...", "...", "...", "...", "..."]
  }},
  "week_3": {{
    "focus": "<Main training theme>",
    "missions": ["...", "...", "...", "...", "..."]
  }}
}}

Guidelines for designing missions:
- Missions must be SHORT (1–3 minutes).
- Missions must be ACTIONABLE (e.g. "Explain climate change in 20 seconds without fillers").
- Missions must connect to Model UN tasks:
    * Opening speeches
    * POIs (Points of Information)
    * Argument building
    * Case construction
    * Rebuttal clarity
- Missions should reflect the student's weaknesses based on ANALYZING, ORGANIZING, PRODUCING TEXT, USING LANGUAGE.
- Each week should escalate slightly in difficulty.
- DO NOT include anything outside JSON.

Here is the student's evaluation:
{evaluation_json}
""")

model = ChatOpenAI(model="gpt-4", temperature=0.6)


def generate_action_plan(evaluation_json: str) -> str:
    """Generate a 3-week action plan based on the student's evaluation."""
    messages = action_plan_template.format_messages(
        evaluation_json=evaluation_json
    )
    response = model.invoke(messages)
    return response.content






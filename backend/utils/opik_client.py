from opik import Opik
import os

def init_opik():
    return Opik(
        api_key=os.getenv("COMET_API_KEY"),
        workspace=os.getenv("COMET_WORKSPACE"),
        project_name=os.getenv("COMET_PROJECT_NAME", "hey-marley")
    )

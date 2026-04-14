from pathlib import Path
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from tests.fixtures.job_descriptions import ICEYE_SENIOR_DATA_ENGINEER
from langchain_core.messages import SystemMessage, HumanMessage
from .models import JobDescriptionParseResult

load_dotenv()

model = init_chat_model("claude-haiku-4-5")

SKILL_PATH = Path(__file__).parent / "skills" / "parse-job-description" / "SKILL.md"
SYSTEM_PROMPT = SKILL_PATH.read_text()

job_description_parser_agent = create_agent(
    model=model,
    system_prompt=SystemMessage(content=SYSTEM_PROMPT),
    name="job_description_parser",
    response_format=JobDescriptionParseResult,
    debug=True
)


def parse_job_description(job_description: str) -> JobDescriptionParseResult:
    """
    Parse a job description to extract 2-3 core technical skills.

    Args:
        job_description: The full job description text

    Returns:
        JobDescriptionParseResult with extracted skills
    """
    messages = [
        HumanMessage(content=f"Extract the core technical skills from this job description:\n\n{job_description}")
    ]

    response = job_description_parser_agent.invoke({"messages": messages}) # type: ignore
    return response["structured_response"]


if __name__ == "__main__":
    result = parse_job_description(ICEYE_SENIOR_DATA_ENGINEER)
    print(f"Skills: {result.skills}")
    print(f"Status: {result.status}")
    if result.reason:
        print(f"Reason: {result.reason}")

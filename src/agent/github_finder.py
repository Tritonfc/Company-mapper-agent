from pathlib import Path
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model # for web search                                                                                 
from langchain.tools import tool
from langchain.agents import create_agent
from .tools import web_search
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage

load_dotenv()

model = init_chat_model("claude-haiku-4-5")


SKILL_PATH = Path(__file__).parent / "skills" / "find-company-github" / "SKILL.md"
SYSTEM_PROMPT = SKILL_PATH.read_text()

tools = [web_search]

github_search_agent = create_agent(
    model=model,  # Default model
    tools=tools,
    system_prompt=  SystemMessage(content=SYSTEM_PROMPT),
     name="github_finder_assistant",
    debug= True
)


def find_company_github(company_name: str):
    """
    Find a company's GitHub account using the find-company-github skill.

    Args:
        company_name: The company to search for (e.g., "Anthropic", "Oura fitness watches")

    Returns:
        The GitHub username, or AMBIGUOUS/NOT_FOUND response
    """
    messages = [
       
        HumanMessage(content=f"Find the GitHub for: {company_name}")
    ]

    response = github_search_agent.invoke({"messages": messages}) # type: ignore
    
    final_message = response["messages"][-1]                                  
    return final_message.content  
   


if __name__ == "__main__":
    company = input("Enter company name: ")
    result = find_company_github(company)
    print(result)
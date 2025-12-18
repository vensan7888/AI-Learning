import requests
from langchain.tools import Tool
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType

def duckduckgo_search(query: str) -> str:
    """Performs a DuckDuckGo search and returns the abstract."""
    url = "https://api.duckduckgo.com/"
    params = {
        "q": query,
        "format": "json",
        "no_redirect": 1,
        "no_html": 1
    }
    try:
        res = requests.get(url, params=params)
        data = res.json()
        return data.get("Abstract", "No summary found.")
    except Exception as e:
        return f"Search error: {e}"

search_tool = Tool(
    name="DuckDuckGoSearch",
    func=duckduckgo_search,
    description="Searches the web for recent information. Use for current events or factual lookups."
)

llm = ChatOpenAI(
    openai_api_key="",  # Your OpenRouter key
    openai_api_base="https://openrouter.ai/api/v1",
    model_name="mistralai/mistral-7b-instruct",#"openchat/openchat-3.5",  # Great for tool use
    temperature=0.7
)

agent = initialize_agent(
    tools=[search_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors=True
)

response = agent.run("What is the latest news about Apple's Vision Pro?")

print(f"\nResponse::\n{response}\n")

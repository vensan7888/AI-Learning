import requests
from langchain_community.utilities import SerpAPIWrapper
from langchain.tools import Tool
from langchain_community.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType

from langchain_community.utilities import SerpAPIWrapper
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

search = SerpAPIWrapper(
    serpapi_api_key="") # your token from SerpAPI goes here.
#search.k = 5
#search.run("LangChain tools", k=5)
search_tool = Tool(
    name="SerpSearch",
    func=search.run,
    description="Searches the web for recent information. Use for current events or factual lookups."
)

prompt = PromptTemplate(
    input_variables=["snippets"],
    template="""
You are a research assistant summarizing news articles.

Here are some article snippets:
{snippets}

Please write a detailed, multi-paragraph summary covering:
- Key themes and trends
- Positive and negative sentiment
- Any technical or product updates
- Future outlook

Use clear, professional language.
"""
)

# From langchain community
llm = ChatOpenAI(
    openai_api_key="",  # Your OpenRouter key
    openai_api_base="https://openrouter.ai/api/v1",
    model_name="mistralai/mistral-7b-instruct",#"openchat/openchat-3.5",  # Great for tool use
    temperature=0.7
)

summarizer_chain = LLMChain(llm=llm, prompt=prompt)

def summarizer_tool_func(query: str) -> str:
    results = search.results(query)
    snippets = "\n".join([
        r.get("snippet", "") for r in results.get("organic_results", [])[:5]
    ])
    return summarizer_chain.run(snippets=snippets)

tool = Tool(
    name="SearchAndSummarize",
    func=summarizer_tool_func,
    description="Searches the web and returns a detailed summary of top articles."
)

agent = initialize_agent(
    tools=[tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors=True
)

response = agent.run("latest news about Apple Vision Pro")
print(f"\nResponse::\n{response}\n")

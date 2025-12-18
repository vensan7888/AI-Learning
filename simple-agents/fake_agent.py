from langchain_core.language_models.fake import FakeListLLM
from langchain.agents import AgentType, initialize_agent, AgentExecutor, Tool

# Define a mock tool
def fake_tool(input: str) -> str:
    return ""

tools = [
    Tool(
        name="MultiplyNumbers",
        func=fake_tool,
        description="Multiplies two numbers. Input format: '7 and 6'."
    )
]

# Mock LLM response that triggers the tool
llm = FakeListLLM(responses=[
    "Action: MultiplyNumbers\nAction Input: 7 and 6",
    "Final Answer: 55"
])

# Initialize agent
# Wrap with AgentExecutor to handle parsing errors
agent_executor = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors=True  # ✅ pass this here
)

# Run the agent
response = agent_executor.invoke({"input": "What is 7 times 6?"})
print(f"\nResponse::\n{response}\n")

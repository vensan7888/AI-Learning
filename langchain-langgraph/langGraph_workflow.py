from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

from langchain_community.tools import TavilySearchResults
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser

import re
from langchain.schema import StrOutputParser
from typing import TypedDict, Optional
from langgraph.graph import StateGraph

class WorkflowState(TypedDict):
    input: str
    router: str
    research: str
    write: str
    validate: str
    publish: str
    retry: bool

from pydantic import BaseModel

class ModerationResult(BaseModel):
    accuracy: int
    clarity: int
    completeness: int
    compliance: int
    overall: int

class NoThinkParser(StrOutputParser):
    def parse(self, text: str) -> str:
        # Remove <think> ... </think>
        cleaned = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
        return cleaned

class LangGraphWorkflowBot: 
    def __init__(self):
        self.tavily = TavilySearchResults(tavily_api_key= "asdasdasdasd", max_results=5)

        self.llama = Ollama(model="llama3.2")
        self.mistral = Ollama(model="mistral:7b")
        self.deepseek = Ollama(model="deepseek-r1")
        
        self.researcher = self.researchChain()
        self.moderater = self.moderationChain()
        self.writer = self.writerChain()
        self.validater = self.validatorChain()
        
        graph = self.buildGraph()
        self.agent = graph.compile()
        # Print workflow
        print(self.agent.get_graph().draw_mermaid())
    
    def researchChain(self):
        llm = self.mistral
        research_prompt = """
            Research the following topic using the given results:
            Topic: {topic}
            SearchResults: {results}

            Extract:
            - Key points
            - Trends
            - Contradictions
            - Stats
            """
        research_chain = (
            {
                "topic": lambda x: x["topic"],
                "results": lambda x: self.tavily.run(x["topic"])
            }
            | PromptTemplate.from_template(research_prompt)
            | llm)

        return research_chain
    
    def writerChain(self):
        llm = self.deepseek
        writer_prompt = """
            Using the researched insights below, write a {format} in {tone} tone.

            Insights:
            {insights}

            Rules:
            - Only return the article.
            - No analysis or internal thoughts.
            
            """

        writer_chain = PromptTemplate.from_template(writer_prompt) | llm | NoThinkParser()

        return writer_chain

    def validatorChain(self):
        llm = self.llama
        validator_prompt = """
            Validate the generated content for:
            - grammar issues
            - tone mismatch
            - hallucinations
            - factual errors

            Content:
            {content}

            Return: 
            - Only return the article.
            - No analysis or internal thoughts.
            """

        validator_chain = PromptTemplate.from_template(validator_prompt) | llm
        
        return validator_chain
    
    def moderationChain(self):
        llm = self.llama
        moderation_prompt = """
            You are a strict evaluator of a workflow system. 
            Return quality scores for the content below against the topic.

            Topic:
            {topic}
            
            Content:
            {content}

            Return ONLY JSON in this structure, all values should range from 1 to 10 interger data type, 
            incase of fractional parts, always round up to nearest integer:
            {{
                "accuracy": int,
                "clarity": int,
                "completeness": int,
                "compliance": int,
                "overall": int
            }}
            Do not include any text outside the JSON.
            """
        parser = PydanticOutputParser(pydantic_object=ModerationResult)

        moderator_chain = PromptTemplate.from_template(moderation_prompt) | llm | parser
        
        return moderator_chain

    def routerNode(self, state: WorkflowState):
        if bool(state.get("retry")):
            return {"router": "research"}
        elif bool(state.get("write")):
            return {"router": "publish"}
        elif bool(state.get("validate")):
            return {"router": "write"}
        elif bool(state.get("research")):
            return {"router": "validate"}
        else:
            return {"router": "research"}
    
    def moderatorNode(self, state):
        currentState = state.get("router")
        result = self.moderater.invoke({"content": state.get(currentState), "topic": state.get("input")})
        score = result.overall  # int 0–10
        print(f"\nModeration Score: {score}, State: {currentState}\n")
        return {"retry": score < 7}
    
    def researchNode(self, state: WorkflowState):
        result = self.researcher.invoke({"topic": state.get("input")})
        print(f"\n research result:: {result}\n")
        return {"research": result, "router": "research"}

    def validatorNode(self, state: WorkflowState):
        result = self.validater.invoke({"content": state["research"]})
        return {"validate": result}

    def writerNode(self, state: WorkflowState):
        result = self.writer.invoke({"insights": state["validate"], 
                                     "format": "article",
                                     "tone": "professional"})
        return {"write": result}
    
    def publishNode(self, state: WorkflowState):
        print(f"\n State:: {state}\n")
        return {"publish": f"{state['write']}"}
    
    def buildGraph(self):
        graph = StateGraph(WorkflowState)
        graph.add_node("router", self.routerNode)
        graph.add_node("research", self.researchNode)
        graph.add_node("write", self.writerNode)
        graph.add_node("validate", self.validatorNode)
        graph.add_node("publish", self.publishNode)
        graph.add_node("moderation", self.moderatorNode)
        
        graph.set_entry_point("research")

        graph.add_conditional_edges(
             "router",
             lambda state: (
                 state.get("router")
             ),
             {
                 "research": "research",
                 "write": "write",
                 "validate": "validate",
                 "publish": "publish"
             }
        )
        
        # End each path
        graph.add_edge("research", "moderation")
        graph.add_edge("write", "moderation")
        graph.add_edge("validate", "moderation")
        
        graph.add_edge("moderation", "router")

        graph.add_edge("publish", END)
        
        return graph

    def chat(self):
        print("=== LangGraph Workflow Agent Chatbot ===")
        print("Type 'exit' to quit.")
        while True:
            print("Waiting for User Input")
            user_input = input("\nUser: ")
            if user_input.lower() in ["exit", "quit"]:
                break

            response = self.agent.invoke({"input": user_input})
            print(f"\nAgent: {response['publish']}\n")

if __name__ == "__main__":
    bot = LangGraphWorkflowBot()
    bot.chat()


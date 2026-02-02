from langchain_community.tools import TavilySearchResults
from langchain.tools import StructuredTool
import requests

from langchain_core.prompts import PromptTemplate
from langchain_community.llms import Ollama
from langchain.chains.router import MultiPromptChain
from langchain_core.output_parsers import StrOutputParser

import re
from langchain.schema import StrOutputParser

class NoThinkParser(StrOutputParser):
    def parse(self, text: str) -> str:
        # Remove <think> ... </think>
        cleaned = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
        return cleaned

class LangChainWorkflowBot:
    def __init__(self):
        self.tavily = TavilySearchResults(tavily_api_key= "asdasdasdasdadasdasd", max_results=5)
        self.publisherTool = StructuredTool.from_function(name="publish_to_sheet",
                                                          func=self.push_to_sheet, 
                                                          description="Publish final content to an external sheet or DB")
        self.llama = Ollama(model="llama3.2")
        self.mistral = Ollama(model="mistral:7b")
        self.deepseek = Ollama(model="deepseek-r1")
        
    def routerChain(self):
        llm = self.llama

        router_prompt = """
            Decide the next action based on user request.

            User query: {input}

            Available tasks:
            1. research
            2. write
            3. validate
            4. publish

            Return ONLY the task name.
            """

        router_chain = PromptTemplate.from_template(router_prompt) | llm
        return router_chain
    
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
            - corrected version
            - list of issues fixed
            """

        validator_chain = PromptTemplate.from_template(validator_prompt) | llm
        
        return validator_chain
    
    def workflowChain(self, user_input):
        information = self.tavily.run(user_input)
        #print(f"\ninformation:: {information}\n")
        # Step 1 — research
        research_out = self.researchChain().invoke({"topic": user_input})
        print(f"\nresearch_out:: {research_out}\n")

        # Step 2 — validate
        valid_out = self.validatorChain().invoke({"content": research_out})
        print(f"\nvalid_out:: {valid_out}\n")

        # Step 3 — write
        writer_out = self.writerChain().invoke({
            "insights": valid_out,
            "format": "article",
            "tone": "professional"
        })
        print(f"\nwriter_out:: {writer_out}\n")
        return writer_out
        # Step 4 — publish
        #publish_out = self.publisherTool.run({"data": writer_out})
        #return publish_out

    def push_to_sheet(data: dict):
        # Example POST call
        return {
            "status": "success",
            "message": "Data processed locally (mocked publisher).",
            "stored_data": data
            }

    def chat(self):
        print("=== LangChain Workflow Agent Chatbot ===")
        print("Type 'exit' to quit.")
        while True:
            print("Waiting for User Input")
            user_input = input("\nUser: ")
            if user_input.lower() in ["exit", "quit"]:
                break

            response = self.workflowChain(user_input)
            print(f"\nAgent: {response}\n")

if __name__ == "__main__":
    chain = LangChainWorkflowBot()
    chain.chat()


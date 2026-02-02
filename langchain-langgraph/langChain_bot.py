
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA, ConversationChain, ConversationalRetrievalChain
from langchain.memory import VectorStoreRetrieverMemory, ConversationBufferMemory
from langchain.prompts import PromptTemplate

from faissHelper import FaissHelper

# Query → Embeddings → Vector Store Search → Retrieved Docs + Query → LLM → Final Answer
class LangChainBot:

    def __init__(self):
        manifestPath = "fileManifest"
        faissVectorDbPath = "faiss_vector_db"
        documentsDir = "documents"

        self.faissHelper = FaissHelper(manifestPath, faissVectorDbPath, documentsDir)
        
        # Build FAISS vectorstore
        self.vector_db = self.faissHelper.loadFaiss()
        
        # Run time memory, use 'history' for Example 2, & 'chat_history' for Example 3
        shortTermMemory = ConversationBufferMemory(memory_key="chat_history",
                                                   return_messages=True)

        # Local LLM
        llm = Ollama(model="llama3.2")

        # Example 1: RAG Chain with 'Document search' 
        # self.agent = RetrievalQA.from_chain_type(
        #    llm=llm,
        #    retriever=self.vector_db.as_retriever(),
        #    chain_type="stuff"
        # )
        
        # Example 2: Conversation works with short term memory 
        # self.agent = ConversationChain(llm=llm,
        #                                memory=shortTermMemory,
        #                                verbose=True)
        
        # Conversation works with long term memory (FAISS - VectorDB)
        template = """
            You are a helpful assistant.

            Use the chat history to maintain full conversation context.
            If the user asks a question referring to earlier conversation, 
            use chat_history to answer, 
            don't include addtioanl text other than what is asked in answer,

            Chat History:
            {chat_history}
            
            Retrieved Context:
            {context}

            User Question:
            {question}

            Answer:
            """

        prompt = PromptTemplate(
            input_variables=["chat_history", "context", "question"],
            template=template)
        # Example 3: RAG Agent with Short term + Long term memory
        self.agent = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=self.vector_db.as_retriever(),
            memory=shortTermMemory,
            combine_docs_chain_kwargs={"prompt": prompt})
    
    def chat(self):
        print("=== LangChain Agent Chatbot ===")
        print("Type 'exit' to quit.")
        while True:
            print("Waiting for User Input")
            user_input = input("\nUser: ")
            if user_input.lower() in ["exit", "quit"]:
                break

            # ****************************
            
            # Example 1
            # answer = self.agent.run(user_input) #for RetrieveQA
            
            # ****************************
            
            # Example 2
            # response = self.agent.invoke({"input": user_input})
            # answer = response['response']
            
            # ****************************
            
            # Example 3
            response = self.agent.invoke({"question": user_input})
            answer = response['answer']
            self.faissHelper.save(f"User: {user_input}", self.vector_db)
            self.faissHelper.save(f"Assistent: {answer}", self.vector_db)
            
            # ****************************
            
            print(f"\nAgent: {answer}\n")
            

if __name__ == "__main__":
    chain = LangChainBot()
    chain.chat()
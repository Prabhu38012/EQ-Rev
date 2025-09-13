from langchain.agents import initialize_agent, AgentType
from langchain_groq import ChatGroq
from agent.tools import allocate_stock_tool, low_stock_tool
import os
from dotenv import load_dotenv

load_dotenv()

def build_agent():
    """
    Build and return the LangChain agent with our custom tools using Groq and Llama.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables")
    
    # Initialize Groq with Llama model
    llm = ChatGroq(
        groq_api_key=api_key,
        model_name="llama-3.1-70b-versatile"
    )
    
    tools = [allocate_stock_tool, low_stock_tool]
    
    # Use STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    return agent
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain.llms import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

def create_chatbot(csv_file_path, user_question):
    try:
        openai_instance = OpenAI() 
        agent = create_csv_agent(openai_instance, csv_file_path, verbose=True)
        response = agent.run(user_question)
        return response

    except Exception as e:
        raise RuntimeError(f"Error creating OpenAI instance or running the agent: {e}")


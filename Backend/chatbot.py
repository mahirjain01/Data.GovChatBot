from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain.llms import OpenAI
import os

def create_chatbot(csv_file_path, user_question):
    # Set the OpenAI API key as an environment variable
    openai_api_key = "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"
    os.environ["OPENAI_API_KEY"] = openai_api_key

    try:
        openai_instance = OpenAI() 
        agent = create_csv_agent(openai_instance, csv_file_path, verbose=True)
        response = agent.run(user_question)
        return response

    except Exception as e:
        raise RuntimeError(f"Error creating OpenAI instance or running the agent: {e}")


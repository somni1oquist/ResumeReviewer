import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI


load_dotenv()

def get_llm(temperature: float = 0.2) -> AzureChatOpenAI:
    """
    Get the main LLM instance for the application.
    
    Args:
        temperature (float): The temperature setting for the LLM.
        
    Returns:
        AzureChatOpenAI: Configured LLM instance.
    """
    return AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        temperature=temperature
    )

# Main LLM for chatbot and reviewer
main_llm = get_llm(0.2)

# LLM for parsing resumes and job descriptions
parse_llm = get_llm(0)
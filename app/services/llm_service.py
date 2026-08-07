# reusable interface for interacting with the LLM.

from langchain_google_genai import ChatGoogleGenerativeAI
from app.utils.logger import logger
from app.core.config import GOOGLE_API_KEY,MODEL_NAME


class LLMService:
    def __init__(self):
        logger.info("Initializing Gemini Model....")
        self.llm=ChatGoogleGenerativeAI(model=MODEL_NAME,google_api_key=GOOGLE_API_KEY)
        
    
    def invoke(self,prompt:str):
        try:
            logger.info("Invoking the llm....")
            return self.llm.invoke(prompt)
        except Exception as e:
            raise Exception(f"LLM Error: {e}")
        
    
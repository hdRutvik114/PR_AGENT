from abc import ABC,abstractmethod

from app.services.llm_service import LLMService
from app.utils.logger import logger 


class BaseAgent(ABC):
    def __init__(self, llm_service:LLMService):
        self.llm =llm_service
        self.logger=logger
        
    
    @abstractmethod
    def run(self,state):
        pass 
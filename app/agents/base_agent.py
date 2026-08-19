from abc import ABC,abstractmethod

from app.services.llm_service import LLMService
from app.utils.logger import logger 


class BaseAgent(ABC):
    def __init__(self, llm_service:LLMService):
        self.llm_service = llm_service
        # expose the underlying chat model instance for agent operations
        self.llm = llm_service.llm
        self.logger = logger
        
    
    @abstractmethod
    def run(self,state):
        pass 
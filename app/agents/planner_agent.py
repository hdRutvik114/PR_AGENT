from .base_agent import BaseAgent
from app.prompts.planner_prompt import PLANNER_PROMPT

class PlannerAgent(BaseAgent):
    
    #Here there is no constructor defined,we have inherited the constructor from BaseAgent class which takes llm_service as an argument and initializes the llm and logger attributes.
    
    # but in main we have passed the llm serive as dependency injection to the PlannerAgent class which is then passed to the BaseAgent class constructor and initialized in the llm attribute of the BaseAgent class.
    def run(self,state):
        self.logger.info("Planner Agent Started")
        
        
        prompt=PLANNER_PROMPT.format(
            issue=state.issue,
            repository=state.repository_path
        )
        
        response = self.llm.invoke(prompt)
        # Planner doesn't return a separate object.
        # It updates the shared notebook.
        state.investigation_plan=response.content
        self.logger.info("Planner Agent Completed")
        return state
        

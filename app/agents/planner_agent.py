from .base_agent import BaseAgent
from app.prompts.planner_prompt import PLANNER_PROMPT

class PlannerAgent(BaseAgent):
    
    
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
        

from app.agents.base_agent import BaseAgent
from app.prompts.investigation_prompt import INVESTIGATION_PROMPT
from app.schemas.evidence import Evidence
from app.tools.repository_search_tool import RepositorySearchTool
from langchain_core.tools import tool
from langchain_core.messages import ToolMessage, HumanMessage, SystemMessage
from langchain_core.exceptions import OutputParserException

class InvestigationAgent(BaseAgent):

    def __init__(self, llm_service):
        super().__init__(llm_service)
        self.tools = [RepositorySearchTool]
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        # here we are calling the constructor of the BaseAgent class using super() and passing the llm_service argument to it. This ensures that the llm attribute is properly initialized in the BaseAgent class.
       
        
    def run(self, state):

        self.logger.info("Investigation started.")

        prompt = INVESTIGATION_PROMPT.format(
            issue=state.issue,
            plan=state.investigation_plan,
            repository_path=state.repository_path
        )
        
        response = self.llm_with_tools.invoke(prompt)
        self.logger.info(f"Investigation response: {response.content}")
        self.logger.info(f"Investigation response type: {type(response.content)}")
        self.logger.info(f"Investigation tool calls : {response.tool_calls}")
        
        # Create a map of tool names to tool functions
        tool_map = {tool.name: tool for tool in self.tools}
        
        messages = [
            SystemMessage(content="You are a software investigation agent"),
            HumanMessage(content=prompt)
        ]
        
        messages.append(response)
        
        # Agentic loop to handle tool calls
        while response.tool_calls:
            for tool_call in response.tool_calls:
                tool_id = tool_call.get('id') or tool_call.get('tool_call_id') 
                tool_name = tool_call['name']
                tool_args = tool_call['args']
                
                self.logger.info(f"Executing Tool: {tool_name} | {tool_id}")
                self.logger.info(f"Tool Arguments: {tool_args}")
                
                tool = tool_map[tool_name]
                
                # Call the tool with unpacked arguments
                tool_output = tool.invoke(tool_args)
                
                self.logger.info(f"Tool Results: {tool_output}")
                
                # Add tool result to messages
                messages.append(ToolMessage(
                    content=str(tool_output),
                    name=tool_name,
                    tool_call_id=tool_id
                ))
            
            # Get next response from LLM
            self.logger.info("🔥 Calling LLM with tool results")
            response = self.llm_with_tools.invoke(messages)
            self.logger.info(f"Response from LLM after tool call: {response}")
            
            # Append assistant response to messages for context
            if response.tool_calls:
                messages.append(response)
            
        # Extract final content and add to evidence
        if hasattr(response, 'content') and response.content:
            content_text = response.content
            if isinstance(content_text, list):
                content_text = "".join([
                    item if isinstance(item, str) else item.get("text", "")
                    for item in content_text
                ])
            
            # Add final investigation content to evidence
            new_evidence = Evidence(
                source="investigation_agent",
                content=str(content_text)
            )
            state.evidence.append(new_evidence)
            self.logger.info(f"Added investigation evidence: {new_evidence}")
        
        self.logger.info("Investigation completed.")
        
        return state
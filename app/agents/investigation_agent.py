from app.agents.base_agent import BaseAgent
from app.prompts.investigation_prompt import INVESTIGATION_PROMPT
from app.schemas.evidence import Evidence
from app.tools.repository_search_tool import RepositorySearchTool
from langchain_core.tools import tool
from langchain_core.messages import ToolMessage,HumanMessage,SystemMessage

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
        
        tool_map={
            tool.name:tool for tool in self.tools
        }
        messages=[SystemMessage(content="You are a software investigation agent")]
        
        
        messages.append(response)
        
        
        
        for tool_call in response.tool_calls:
            tool_call_id = tool_call.get('id') or tool_call.get('tool_call_id') 
            tool_name=tool_call['name']
            tool_args=tool_call['args']
            
            self.logger.info(f"Executing Tool:{tool_name}")
            self.logger.info(f"Tool Arguments:{tool_args}")
            
            tool=tool_map[tool_name]
            
            result=tool.invoke(tool_args)
            
            self.logger.info(f"Tool Results:{result}")
            
            messages.append(ToolMessage(content=str(result),tool_call_id=tool_call_id))
            
            response=self.llm_with_tools.invoke(messages)
            self.logger.info(f"Response from the LLM_after the tool call {response[0]}")
            
            # Only append if there are more tool calls to process
            if response.tool_calls:
                messages.append(response)
            else:
                self.log# Append the assistant's next tool call
            
        # # 1. Safely handle response.content whether it's a string or a list
        # if isinstance(response.content, list):
        #     content_text = "".join(
        #         [
        #             item if isinstance(item, str) else item.get("text", "")
        #             for item in response.content
        #         ]
        #     )
        # else:
        #     content_text = str(response.content)

        # # 2. Safely split into keywords
        # keywords = [
        #     word.strip()
        #     for word in content_text.split(",")
        #     if word.strip()
        # ]

        # # 3. Search using the extracted keywords
        # self.logger.info(f"Investigation keywords: {keywords}")
        # for keyword in keywords:
        #     files = self.search_tool.search(
        #         state.repository_path,
        #         keyword
        #     )

        #     # FOR EACH file we found during search
        #     for file in files:
            
        #       # 1. First, check if this file is ALREADY in state.evidence
        #       already_exists = False
            
        #       for evidence in state.evidence:
        #         if (
        #             evidence.content == file
        #             and evidence.source == "repository_search"
        #         ):
        #           already_exists = True
        #           break  # Found a duplicate, stop checking this file!
            
        #       # 2. If it's NOT a duplicate, create and append new Evidence
        #       if not already_exists:
        #         new_evidence = Evidence(source="repository_search", content=file)
        #         state.evidence.append(new_evidence)
                
                
        #         # This one is the same as the below code but in a more readable way and also it is more efficient because it breaks the loop when it finds a duplicate instead of checking all the evidence.
        #         '''for file in files:

        #              if not any(
        #                  evidence.content == file
        #                  and evidence.source == "repository_search"
        #                  for evidence in state.evidence
        #              ):
        #                  state.evidence.append(
        #                      Evidence(
        #                          source="repository_search",
        #                          content=file
        #                      )
        #                  )'''
            
            
            
            
        # self.logger.info("Investigation completed.")
        
        return state
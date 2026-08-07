from app.agents.base_agent import BaseAgent
from app.prompts.investigation_prompt import INVESTIGATION_PROMPT
from app.schemas.evidence import Evidence
from app.tools.repository_search_tool import RepositorySearchTool


class InvestigationAgent(BaseAgent):

    def __init__(self, llm_service):
        super().__init__(llm_service)

        self.search_tool = RepositorySearchTool()

    def run(self, state):

        self.logger.info("Investigation started.")

        prompt = INVESTIGATION_PROMPT.format(
            issue=state.issue,
            plan=state.investigation_plan
        )

        response = self.llm.invoke(prompt)

        # 1. Safely handle response.content whether it's a string or a list
        if isinstance(response.content, list):
            content_text = "".join(
                [
                    item if isinstance(item, str) else item.get("text", "")
                    for item in response.content
                ]
            )
        else:
            content_text = str(response.content)

        # 2. Safely split into keywords
        keywords = [
            word.strip()
            for word in content_text.split(",")
            if word.strip()
        ]

        # 3. Search using the extracted keywords
        for keyword in keywords:
            files = self.search_tool.search(
                state.repository_path,
                keyword
            )

            for file in files:

                state.evidence.append(
                    Evidence(
                        source="repository_search",
                        content=file
                    )
                )

        self.logger.info("Investigation completed.")

        return state
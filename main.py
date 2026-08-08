from app.agents.planner_agent import PlannerAgent
from app.agents.investigation_agent import InvestigationAgent
from app.schemas.state import WorkflowState
from app.services.llm_service import LLMService


def main():

    llm_service = LLMService()

    state = WorkflowState(
        issue="Login API returns 500 when email is missing.",
        repository_path="sample_repo"
    )

    planner = PlannerAgent(llm_service)
    investigator = InvestigationAgent(llm_service)

    state = planner.run(state)
    state = investigator.run(state)

    print("\n========== INVESTIGATION PLAN ==========")
    print(state.investigation_plan)

    print("\n========== EVIDENCE ==========")

    for evidences in state.evidence:
        print(evidences)


if __name__ == "__main__":
    main()
from typing import List , Optional
from pydantic import BaseModel
from app.schemas.evidence import Evidence



class WorkflowState(BaseModel):
    issue: str 
    repository_path:str
    investigation_plan:Optional[str]=None
    evidence:List[str] = []
    root_cause:Optional[str] = None
    patch:Optional[str] =None
    test_results: Optional[str] =None
    report: Optional[str]=None 
    evidence:List[Evidence] = []
# [
#     Evidence(
#         source="repository_search",
#         content="auth.py"
#     ),

#     Evidence(
#         source="git",
#         content="commit abc123"
#     ),

#     Evidence(
#         source="test_runner",
#         content="5 passed"
#     )
# ]
    
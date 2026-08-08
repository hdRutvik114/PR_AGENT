from typing import List , Optional
from pydantic import BaseModel
from app.schemas.evidence import Evidence


# In plain Python, a regular class doesn't enforce what kind of data goes into its variables.

# BaseModel comes from the Pydantic library, which is used for data validation and settings management using Python type annotations. When you define a class that inherits from BaseModel, Pydantic automatically validates the data types of the attributes when you create an instance of that class.
class WorkflowState(BaseModel):
    issue: str 
    repository_path:str
    investigation_plan:Optional[str]=None
  
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
    
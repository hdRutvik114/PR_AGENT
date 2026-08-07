from pathlib import Path 
#This file is used to search for repositories in a given directory. It can be used to find all repositories in a given directory and its subdirectories.
from app.core.constants import MAX_SEARCH_RESULTS
from app.tools.base_tool import BaseTool



class RepositorySearchTool(BaseTool):
    
    def search(self,repository_path:str,keyword:str):
        matches=[]
        
        for file in Path(repository_path).rglob("*.py"):
            try:
                content=file.read_text(encoding="utf-8")
                if keyword.lower() in content.lower():
                    matches.append(str(file))
                    
                if len(matches)>=MAX_SEARCH_RESULTS:
                    break
            except Exception as e:
                continue
            
        return matches
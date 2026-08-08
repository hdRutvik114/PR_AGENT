import keyword
from pathlib import Path 
#This file is used to search for repositories in a given directory. It can be used to find all repositories in a given directory and its subdirectories.
from app.core.constants import MAX_SEARCH_RESULTS
from app.tools.base_tool import BaseTool



class RepositorySearchTool(BaseTool):
    
    def search(self,repository_path:str,search_term:str):
        matches=[]
        self.logger.info(f"Searching repository: {repository_path}")
        # self.logger.info(f"Keyword: {keyword}"'file' is automatically assigned the path of the current .py file found by rglob)
        for file in Path(repository_path).rglob("*.py"):
            try:# 2. Automatically opens the file on disk, reads all its text, and closes it
                content=file.read_text(encoding="utf-8")
                if search_term.lower() in content.lower():
                    matches.append(str(file))
                    # Adds the file path string to matches list
                    
                if len(matches)>=MAX_SEARCH_RESULTS:
                    break
            except Exception as e:
                continue
        self.logger.info(f"Search matches: {matches}")
            
        return matches
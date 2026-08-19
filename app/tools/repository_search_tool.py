import keyword
from pathlib import Path 
#This file is used to search for repositories in a given directory. It can be used to find all repositories in a given directory and its subdirectories.
from app.core.constants import MAX_SEARCH_RESULTS
from app.tools.base_tool import BaseTool
from langchain_core.tools import tool 
from app.utils.logger import logger

@tool
def RepositorySearchTool(repository_path:str ,search_term:str):
    """
    Search a repository for Python files containing a given keyword.

    Args:
        repository_path: Path to the repository.
        search_term: Keyword or identifier to search for.

    Returns:
        List of matching file paths.
    """
    matches=[]
    logger.info(f"Searching repository: {repository_path}")
    logger.info(f"Keyword: {search_term}")
    
    # self.logger.info(f"Keyword: {keyword}"'file' is automaticallyassigned the path of the current .py file found by rglob)
    for file in Path(repository_path).rglob("*.py"):
        try:# 2. Automatically opens the file on disk, reads all itstext, and closes it
            content=file.read_text(encoding="utf-8")
            if search_term.lower() in content.lower():
                matches.append(str(file))
                # Adds the file path string to matches list
                
            if len(matches)>=MAX_SEARCH_RESULTS:
                break
        except Exception as e:
            continue
    logger.info(f"Search matches: {matches}")
        
    return matches
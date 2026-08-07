from git import Repo

from app.tools.base_tool import BaseTool


class GitTool(BaseTool):

    def __init__(self):
        super().__init__()

    def get_recent_commits(self, repository_path: str, limit: int = 5):
        repo = Repo(repository_path)

        commits = []

        for commit in repo.iter_commits(max_count=limit):
            commits.append({
                "hash": commit.hexsha[:7],
                "message": commit.message.strip(),
                "author": str(commit.author),
            })

        return commits
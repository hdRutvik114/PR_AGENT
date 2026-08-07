import subprocess

from app.tools.base_tool import BaseTool

class TestRunnerTool(BaseTool):
    
    def __init__(self):
        super().__init__()
        
    def run_tests(self, repository_path: str):
        self.logger.info("Running project tests...")

        result = subprocess.run(
               ["pytest"],
            cwd=repository_path,
            capture_output=True,
            text=True,
        )

        return {
            "passed": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
"""
Terminal programs always return a number.0 means
Success
Anything else means
Failure.
So
result.returncode == 0
becomes
True
    """
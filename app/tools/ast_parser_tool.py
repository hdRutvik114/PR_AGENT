import ast
from pathlib import Path


class ASTParserTool:

    def get_functions(self, file_path: str):
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File {file_path} does not exist.")

        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        functions = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)

        return functions
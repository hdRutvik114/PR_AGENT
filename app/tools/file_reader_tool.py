from pathlib import Path 

from app.core.constants import MAX_FILE_LINES




class FileReaderTool:
    
    def read(self,file_path:str):
        path=Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File {file_path} does not exist.")
        
        line=path.read_text(encoding="utf-8").splitlines()
        
        return "/n".join(line[:MAX_FILE_LINES])
from pathlib import Path

def GetParentDir(path) :
    path = Path(path)
    return path.parent

def safeOpen(path) :
    Path(path).mkdir(parents=True, exist_ok=True)
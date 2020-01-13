from pathlib import Path

def GetParentDir(path) :
    path = Path(path)
    return path.parent

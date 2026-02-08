
import subprocess
import shlex
from typing import List

def run_cmd(command: List[str], check: bool = False) -> bool:
    """
    Executes a shell command efficiently.
    Swallows stdout/stderr unless debugging is needed.
    """
    try:
        subprocess.run(
            command, 
            check=check, 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL
        )
        return True
    except subprocess.CalledProcessError:
        return False

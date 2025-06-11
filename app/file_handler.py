from enum import Enum
from pathlib import Path

home = Path.home()
FILENAME = f"{home}/server_status.txt"

class Status(Enum):
    EMPTY       = -1
    OFF         = 0
    TURNING_ON  = 1
    ON          = 2

def get_status_from_file():
    try:
        with open(FILENAME, "r") as status_file:
            readl=status_file.readline().strip()
            for st in Status:
                if str(st.value) == readl:
                    return st
            return Status.EMPTY
    except FileNotFoundError as fnf:
        print("File missing. Creating it.")
        with open(FILENAME, "x"):
            return Status.EMPTY


def write_status(value):
    with open(FILENAME, "w") as status_file:
        status_file.write(str(value))

import os
from pathlib import Path

NOTES_DIR = os.path.join(Path.home(), ".notes")

if __name__ == '__main__':
    print(NOTES_DIR)
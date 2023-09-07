from pathlib import Path
import os

path_main = Path(__file__).parent.parent
print(Path(__file__))
path_to_data = os.environ.get('PATH_TO_DATA', None)
if path_to_data is None:
    path_to_data = path_main / "data/"

from pathlib import Path

path_main = Path(__file__).parent.parent
print(Path(__file__))
path_to_data = path_main / "data/"
print(path_to_data)

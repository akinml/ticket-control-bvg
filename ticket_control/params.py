from pathlib import Path
import streamlit as st

path_main = Path(__file__).parent.parent
print(Path(__file__))
path_to_data = st.secrets.get('PATH_TO_DATA', None)
if path_to_data is None:
    path_to_data = path_main / "data/"

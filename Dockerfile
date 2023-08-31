FROM prefecthq/prefect:2-python3.9
COPY requirements.txt .
RUN pip install -r requirements.txt --trusted-host pypi.python.org --no-cache-dir
ADD flows flows

# Specify the command to execute when the container starts
CMD ["python", "app.py"]

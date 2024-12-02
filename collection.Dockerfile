FROM python:3.8-slim

COPY ./gptchess/ .
COPY ./stockfish/ ./stockfish/
COPY ./requirements.txt .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "gpt-experiments.py"]


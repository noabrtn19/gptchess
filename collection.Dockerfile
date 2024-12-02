FROM python:3.8-slim


COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./gptchess/ .
COPY ./stockfish/ ./stockfish/

ENTRYPOINT ["python", "gpt-experiments.py"]


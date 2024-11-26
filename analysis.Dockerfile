FROM python:3.10-slim

# docker build -f analysis.Dockerfile -t gpt_chess_analysis .
# docker run --rm -v "$(pwd):/app/volume" gpt_chess_analysis

# Working directory
WORKDIR /app
ENV WORKDIR="/app"
COPY requirements.txt /app

# Python packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install nbconvert

# Environment variable: games tar.gz file (use `-e GPTCHESS_GAMES_FILE = "myfile.tar.gz"` in docker run to change it)
ENV GPTCHESS_GAMES_FILE="games.tar.gz"

# Apt packages (pdf generation)
RUN apt-get update -y

# When the container is run: decompress to tar.gz games folder, and produce a pdf using the current version of the notebook
CMD ["sh", "-c", "tar -xvzf ./volume/$GPTCHESS_GAMES_FILE \
&& jupyter nbconvert --to html --execute ./volume/analysis.ipynb --output-dir ./volume/analysis_files --no-input"]
FROM python:3.10-slim

# Working directory
WORKDIR /app
ENV WORKDIR="/app"
COPY requirements.txt /app

# Python packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install nbconvert

# Environment variables: games tar.gz file and notebook to run
ENV GPTCHESS_GAMES_FILE="games.fftar.gz"
ENV NOTEBOOK="reproducibifflity_analysis.ipynb"

# When the container is run: decompress to tar.gz games folder, and produce a html using the current version of the notebook
CMD ["sh", "-c", "echo test/$GPTCHESS_GAMES_FILE && tar -xvzf ./volume/$GPTCHESS_GAMES_FILE \
&& jupyter nbconvert --to html --execute ./volume/$NOTEBOOK --output-dir ./volume/analysis_files --no-input"]
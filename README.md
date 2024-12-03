# GPT Chess todo

## Introduction

Can Large Language Models (LLM) like ChatGPT play chess? This topic has been the subject of much speculation lately. 
This projects aims at providing an answer, from two angles: the ability of these models to play legal chess moves, 
and the quality of their games. To do so, it collects data by making them play against Stockfish.

This repository has two goals:
- reproducing the results of this article (https://blog.mathieuacher.com/GPTsChessEloRatingLegalMoves/) in an automated way, using the same data (games between various LLM and Stockfish)
- extending the results of this experiment, by exploring several variability factors.

## Reproducibility

### How to Reproduce the Results

1. **Requirements**  
    Docker is required to run the collection/analysis of the data correctly.
    You also need to download Stockfish (we used the 16 version) from https://drive.google.com/drive/folders/1nzrHOyZMFm4LATjF5ToRttCU0rHXGkXI and put the source code in a `stockfish/stockfish` folder.

2. **Setting Up the Environment**  
  - To reproduce the collection of the data, use the `collection.Dockerfile`.
    ```bash
      docker build -f collection.Dockerfile -t chess
    ```

   - To reproduce the analysis of the data, simply build the `analysis.Dockerfile` and run the container with the following volume.
    
    On linux:
     ```bash
     docker build -f analysis.Dockerfile -t gpt_chess_analysis
     docker run --rm -v "$(pwd):/app/volume" gpt_chess_analysis
     ```

     By default, it will use the data in `games.tar.gz`, but you can add `-e GPTCHESS_GAMES_FILE = "myfile.tar.gz"` to docker run, in order to use a different tar.gz file.

3. **Reproducing Results**  
   - The container will automatically execute all the `analysis.ipynb` notebook and produce an html file in the analysis_files folder. You can read this file or the notebook itself, to see the results by yourself.
   - The container will provide a CLI-tool that allows you to reproduce experiments using the parameters you want. Exploration of a variability factor space can be done through scripting (eg. using Bash)

   Here is how you can use the CLI tool : 
    ```bash
    docker run \
    -e OPENAI_API_URL=<URL> \
    -e OPENAI_API_KEY=<KEY> \
    -v <output-folder>:/output \
    -v <pgn-folder>:/pgns \
    chess [-h] -s SKILL -d DEPTH [-t TIME] [-r] -m [MODEL] -o [TEMP]
                [-c] [-l [ROLEMESSAGE]] [-w] -n MOVES -p PGN
    ```
  List of parameters:
  | Parameter | Description                                  | Mandatory ?  |
  |-----------|----------------------------------------------|--------------|
  | --model   | LLM Model to use                             | Yes          |
  | --skill   | Stockfish skill level                        | Yes          |   
  | --depth   | Stockfish depth                              | Yes          |
  | --time    | Stockfish max time                           | no           |
  | --random  | Use random engine instead of Stockfish?      | no           |
  | --temp    | LLM temperature                              | Yes          |
  | --chat    | Chat mode enabled?                           | no           |
  | --rolemessage | Role message in prompt                   | no           |
  | --white   | Start with white pieces?                     | no           |
  | --moves   | Number of the next move to play in the provided PGN | yes   |
  | --pgn     | Path of the PGN file (in the docker container) to use | yes |

### Encountered Issues and Improvements
    Several small adaptations were made from the original article.
    - several pandas methods (like `DataFrame.append`) were deprecated in the latests versions; we replaced them.
    - the code for data collection (in `gpt-experiment.py`) and analysis (in `analysis.ipynb`) was greatly cleaned up and reduced, to focus only on the main results of the study (since a lot of digressions were made).
    - The script now takes cli parameters to adapt the experimentation.

### Is the Original Study Reproducible?
    The main results of the original study have been successfully reproduced: by comparing them quantitatively to those of the article, we can see that we obtain the exact same conclusions. To sum them up:
    - it seems that gpt-4, gpt-3.5-turbo and especially text-davinci-003 are unable to play a full legal chess game, while gpt-3.5-turbo-instruct makes an illegal move in 16% in the games (70% of which is just the model resigning with "1-0").
    - gpt-3.5-turbo-instruct also shows a much better chess understanding, by playing at 1742 elo level against stockfish (if we assume that making an illegal move makes you lose).
    - temperature and players mentioned in the PGN headers have no significant effect on the performances.

## Replicability

### Variability Factors
- **List of Factors**: Here we identified a subset of variations sources you can adjust with the CLI tool.
  
  List of factors:
  | Variability Factor | Possible Values       | Relevance                                                                             |
  |--------------------|-----------------------|---------------------------------------------------------------------------------------|
  | LLM Used           | Llama, Mistral, ...   | Are some LLM better at chess? Each have either a different architecture or training   |
  | Chess variants     | Standard, Chess960    | Are LLM fitted on standard games?    |
  | Stockfish level    | Skill [0-20]          | Which level can the llm beat?              |
  | Prompt format      | PGN, natural language | Formatting of the moves affects the ability to play?   |
  | LLM Temperature    | between 0 and N (llm dependant) | Can temperature enhance the ability to play? |

- **Constraints Across Factors**:  
    - Using third party-api LLM or closed source LLM do not guarantee reproducibility.
    - Due to the way temperature affects the LLM mechanism, using a temperature different of zero require
    the use of statistical analysis techniques and many iterations for each experiment to guarantee results.
    - Due to Stockfish using some randomness & parallel computing, results can vary between different machines or even runs on a single machine.


### Replication Execution
1. **Instructions**  
   We replicated the study to test two new factors : 
   - using different LLM
   - playing chess960

    Example of command to play a game using Groq LLama3-70b & Base PGN
    ```bash
    docker run \
    -e OPENAI_API_URL="https://api.groq.com/openai/v1" \
    -e OPENAI_API_KEY=<KEY> \
    -v ./output:/output \
    -v ./pgns:/pgns \
    chess \
    -s 6 \
    -d 15 \
    -m 'llama-3.1-70b-versatile' \
    -o 0.0 \
    -n 1 \
    -c \
    -p /pgns/base.txt
    ```

    Example of command to play a game using ChatGPT & Chess960 PGN
    ```bash
    docker run \
    -e OPENAI_API_KEY=<KEY> \
    -v ./output:/output \
    -v ./pgns:/pgns \
    chess \
    -s 6 \
    -d 15 \
    -m 'gpt-3.5-turbo-instruct' \
    -o 0.0 \
    -n 1 \
    -p /pgns/chess960.txt
    ```

2. **Presentation and Analysis of Results**  
   - Include results in text, tables, or figures.
   - Analyze and compare with the original study's findings.

### Does It Confirm the Original Study?
- Summarize the extent to which the replication supports the original study’s conclusions.
- Highlight similarities and differences, if any.

## Conclusion
- Recap findings from the reproducibility and replicability sections.
- Discuss limitations of your

-----

# README of the original repo behind

# Debunking the Chessboard: Confronting GPTs Against Chess Engines to Estimate Elo Ratings and Assess Legal Move Abilities

Source code supporting experiments presented in https://blog.mathieuacher.com/GPTsChessEloRatingLegalMoves/ 
I've started with the GPT-3 chess experiment from https://github.com/clevcode/skynet-dev 
and explore the variability space of experiments (GPT variants, number of games, Stockfish skills, temperature, prompt, etc.)

## Install Python dependencies

```pip install openai chess stockfish```

for the analysis part, you'll also need libraries like `pandas` and `matplotlib`

## Install Stockfish

See https://stockfishchess.org/download/
I'm using the Linux `stockfish-ubuntu-x86-64-avx2` binary (version 16). 

## Run Chess experiment

```
export OPENAI_KEY=<your-openai-API-key>
python ./gptchess/gpt-experiments.py 
```

or if you want to run multiple games, you can use a loop like:

```
for i in {1..20}; do python gptchess/gpt-experiments.py; done
```

Edit the source code to change the GPT version, the number of games, the number of moves per game, etc.
Something like this:

```python
chess_config = ChessEngineConfig(
    skill_level=4,
    engine_depth=15,
    engine_time=None,
    random_engine=False
)

gpt_config = GPTConfig(
    model_gpt="gpt-3.5-turbo-instruct",
    temperature=0.0,
    max_tokens=5,
    chat_gpt=False,
    system_role_message=None  
)

play_game(chess_config, gpt_config, base_pgn=BASE_PGN, nmove=1, white_piece=False)
```

The outcome is located in `output` folder and is a subfolder, with the PGN file of the game, the log of the game, and the session with GPT.
You can then analyze the data with the Jupyter notebook `analysis.ipynb`.

### Data and analysis

For convenience, we have released the data used as part of the experiment documented in the blog post. 
It has been saved into the `games.tar.gz` of this repo. 
I'm usually using zenodo, but the size of the data is manageable.  
Decompress the archive to get `games` folder.

``` 
> ls
game30da9c70-31ed-4489-9e93-9ef179661da4  game6a246b94-4511-4b34-908a-6f1fd5b838ac  game98a79424-b219-4764-a4d8-71f524454923  gamec9ba4fa3-b7a9-4953-b8d5-a25db0e10886  gameffa12232-8e93-4440-82d8-a0c8a6023c63
game3179c6e9-935e-4f59-b932-268fd10356fc  game6a34daf4-4820-4eb0-a7ad-6a472d6506a2  game99371010-b5af-48d4-adbc-4fcfda798304  gameca445cfd-0076-4146-ba1b-c263c8cd8707
```

with plenty of folders. Each folder contains:
 * `game.pgn`: the PGN file of the game
 * `metainformation.txt` about configuration of the experiments
 * `log.txt` the log of the game
 * `session.txt` the session with GPT 

`games_db.csv` contains almost all information about all the games, in a structured way. 

`analysis.ipynb` is a Jupyter notebook to analyze the data.

## Update/Misc

 * new experiments based on `Monsieur Phi` suggestion/experiments (X/Twitter thread in french: https://twitter.com/MonsieurPhi/status/1781260337754366265), as a follow-up of his excellent video (in french again!) https://www.youtube.com/watch?v=6D1XIbkm4JE where I was interviewed. The basic idea is to study the impact of the prompt on the GPTs' playing skill, on the very specific position `1. e4 e5 2. Bc4 Nc6 3. Qh5`. I have to wrap-up, but the tldr is that the prompt has indeed a significant impact on the GPTs' playing skill (at least on this position!), and that we can identify intuitive patterns of prompt leading to either g6 or Nf6. See `gptchess/gpt-experiments-prompt-variations.py` and `analysis_prompt_variations.ipyng` and `prompt_variations_phi.csv`. 
 * In parallel, Yosha Iglesias has made a fantastic video: https://www.youtube.com/watch?v=FBx95bdJzh8 further exploring prompt sensitivity and surprising skills of GPT as well as many interesting ideas worth replicating in the large. Fascinating! `analysis_yosha.ipynb` is one ongoing/modest attempt to study the impact of prompt on the GPTs' playing skill (see also `games_yosha.tar.gz` and `games_db_yosha.csv`). Stay tuned for more experiments and analysis! 
 



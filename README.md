# GPT Chess todo

## Introduction

Can Large Language Models (LLM) like ChatGPT play chess? This topic has been the subject of much speculation lately. 
This projects aims at providing an answer, from two angles: the ability of these models to play legal chess moves, 
and the quality of their games. To do so, it collects data by making them play against Stockfish.

This repository has two goals:
- reproducing the results of this article (https://blog.mathieuacher.com/GPTsChessEloRatingLegalMoves/) in an automated way, using the same data (games between various LLM and Stockfish). The main conclusions are as follow: while text-davinci-003 (completion model) is completly unable to play a full legal chess game, GPT 4 (chat model) and espacially GPT 3.5-turbo-instruct (completion model) make fewer illegal moves. The GPT 3.5-turbo-instruct is by far the most capable, achieving "only" 16% of illegal games against Stockfish, and a 1742 ELO performance (considering illegal games as lost).
- extending the results of this experiment, by exploring two variability factors: the LLM (we tested another Chat Model, llama-3.3-70b-versatile) and the chess variant (standard/chess960). First, we collected the data by making Llama play 20 games against Stockfish in standard chess, and 20 games against Stockfish in Chess960 (as well as 13 Chess960 games by GPT-3.5-turbo-instruct). Then, we conducted a similiar analysis on the ability the play legal moves, and we established that Llama was not able to play a full legal standard/960 chess game. Similarly, GPT 3.5-turbo-instruct doesn't even seem to notice the Chess960 header in the PGN, resulting in it generating moves as if it was playing standard chess.

## Reproducibility

### How to Reproduce the Results

1. **Requirements**  
    Docker is required to run the collection/analysis of the data correctly.
    You also need to download Stockfish (we used the 16 version) from https://drive.google.com/drive/folders/1nzrHOyZMFm4LATjF5ToRttCU0rHXGkXI and put the source code in a `stockfish/stockfish` folder, at the project root.

2. **Setting Up the Environment**  
  - To set up the collection of the data, use the `collection.Dockerfile`.
    ```bash
      docker build -f collection.Dockerfile -t chess
    ```

   - To set up the analysis of the data, build the `analysis.Dockerfile`.
     ```bash
     docker build -f analysis.Dockerfile -t gpt_chess_analysis .
     ```

3. **Reproducing Results**  
   - To reproduce the collection of the data :
   
   The container will provide a CLI-tool that allows you to reproduce experiments using the parameters you want. Exploration of a variability factor space can be done through scripting (eg. using Bash)

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
  
   - To reproduce the analysis of the data :
   
   Run the analysis container with the following volume:
   ```bash
   docker run --rm -v "$(pwd):/app/volume" gpt_chess_analysis
   ```
   
   The container will automatically execute all the `reproducibility_analysis.ipynb` notebook and export is as an HTML file in the analysis_files folder. You can read this file or the notebook itself, to see the results by yourself.

### Encountered Issues and Improvements
   Several small adaptations were made from the original article.
   - several pandas methods (like `DataFrame.append`) were deprecated in the latests versions; we replaced them.
   - the code for data collection (in `gpt-experiment.py`) and analysis (in `reproducibility_analysis.ipynb`) was greatly cleaned up and reduced, to focus only on the main results of the study (since a lot of digressions were made).
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
    - Using third party-api LLM or closed source LLM does not guarantee reproducibility.
    - Due to the way temperature affects the LLM mechanism, using a temperature different of zero require
    the use of statistical analysis techniques and many iterations for each experiment to guarantee results.
    - Due to Stockfish using some randomness & parallel computing, results can vary between different machines or even runs on a single machine.


### Replication Execution
1. **Instructions**  
   We replicated the study to test two new factors : 
   - using another LLM: Llama (we generated 20 games against Stockfish, in similiar fashion to the original study)
   - playing chess960 (we generated 20 games against Stockfish with Llama, and 18 against Stockfish with GPT 3.5-turbo-instruct, with the same parameters as the original study).

    Here is the parameters we used to generate 20 standard games between Groq LLama3-70b and Stockfish:
    ```bash
    docker run \
    -e OPENAI_API_KEY=<API_KEY> \
    -e OPENAI_API_URL='https://api.groq.com/openai/v1' \
    -v .\output_3:/output \
    -v .\pgns:/pgns \
    chess \
    -s 6 \
    -d 15 \
    -m 'llama-3.3-70b-versatile' \
    -o 0.0 \
    -n 1 \
    -c \
    -p /pgns/base.txt \
    -l "Play a chess game completing one move of the PGN"
    ```

    Here is the parameters we used to generate 20 chess960 games between Groq LLama3-70b and Stockfish:
    ```bash
    docker run \
    -e OPENAI_API_KEY=<API_KEY> \
    -e OPENAI_API_URL='https://api.groq.com/openai/v1' \
    -v .\output_3:/output \
    -v .\pgns:/pgns \
    chess \
    -s 6 \
    -d 15 \
    -m 'llama-3.3-70b-versatile' \
    -o 0.0 \
    -n 1 \
    -c \
    -p /pgns/chess960.txt \
    -l "Play a chess960 game completing one move of the PGN"
    ```

    All the generated games, for the replication phase, were gathered in the "games_replication.tar.gz" file. To run the corresponding analysis notebook and export it as HTML:
   ```bash
    docker build -f analysis.Dockerfile -t gpt_chess_analysis .
    ```
   ```bash
    docker run --rm -v "$(pwd):/app/volume" \
    -e GPTCHESS_GAMES_FILE="games_replication.tar.gz" \
    -e NOTEBOOK="replication_analysis.ipynb" \
    gpt_chess_analysis
    ```
    This will automatically execute all the `replication_analysis.ipynb` notebook and export is as an HTML file in the analysis_files folder. You can read this file or the notebook itself, to see the results by yourself. This command also generates a CSV file compiling all the games and their parameters.


3. **Presentation and Analysis of Results**  
   - llama-3.3-70b-versatile against Stockfish (normal chess):
   20 total games, with an average length of 10 moves.
Out of 20 games, 0 were legal games and 20 were illegal games, hence 100% of illegal games.

Illegal moves are:

| illegal_move   |   count |
|:---------------|--------:|
| Qe7            |      10 |
| bxc6           |       2 |
| b5             |       1 |
| Be7            |       1 |
| Kxe2           |       1 |
| Nxb4           |       1 |
| Bxe2           |       1 |
| Kd8            |       1 |
| Nxc5           |       1 |
| Qxe2           |       1 |

These games seem to indicate that Llama is not able to play a full legal chess game.

Contrary to GPT 3.5-turbo-instruct, the Llama model doesn't make an illegal move by "resigning" the game (1-0), but seems to produce "real" illegal moves. Interestingly, the "Qe7" illegal move is particularly recurrent in our (small!) dataset (the recurrent pattern here is that the LLM didn't acknowledge the black bishop on e7, obstructing black's queen from going to that square).

- **llama-3.3-70b-versatile against Stockfish (chess960):**

20 total games, with an average length of 0.5 move.

Illegal moves are:

| illegal_move   |   count |
|:---------------|--------:|
| Since          |      12 |
| A              |       5 |
| The            |       3 |

As you can see, despite indicating clearly what we want in the role given to the model, Llama doesn't even try to complete the PGN.

   - GPT 3.5-turbo-instruct against Stockfish (chess960):
  13 total games, with an average length of 3.5 moves.
  
  Out of 13 games, 1 were legal games and 12 were illegal games, hence 92% of illegal games.
Illegal moves are:
| illegal_move   |   count |
|:---------------|--------:|
| Nf6            |       2 |
| Nc6            |       2 |
| Qxd4           |       1 |
| Nf8            |       1 |
| Bg7            |       1 |
| 1.             |       1 |
| -O             |       1 |
| Bg4            |       1 |
| O-O            |       1 |
| Kxd8           |       1 |

It appears that, among the few games that were generated, only the following one was totally legal: 1. h4 g6 2. h5 gxh5 3. b3 Nf6 4. Rh3 d5 5. Bxf6 exf6 6. Rg3# 1-0.
However, we can notice that no move would have been illegal in regular chess either: this game does not really prove the LLM can detect that it is Fischer Random.


### Does It Confirm the Original Study?
This small experiment supports the original's study observation: the ability of GPT 3.5-turbo-instruct to play legal chess games at a high level, seems quite unique among LLMs.
Indeed, the Llama chat model "llama-3.3-70b-versatile" is far from being able to generate a full game: on average, it only plays 10 moves before suggesting an illegal move. In that regard, it does even worse than the "text-davinci-003" completion model (12 legal moves on average). As in the original study, the limited number of generated games and the large variability space make it difficult to establish with any great certainty Llama's inherent inability to understand chess. In particular, since it is a chat model, the role it is given is critical.

## Conclusion
- The reproduction of the original study confirms that gpt-4, gpt-3.5-turbo and especially text-davinci-003 are unable to play a full legal chess game, while gpt-3.5-turbo-instruct makes an illegal move in 16% in the games (70% of which is just the model resigning with "1-0"). This model also shows a much better chess understanding, by playing at 1742 elo level against stockfish (if we assume that making an illegal move makes you lose). Temperature and players mentioned in the PGN headers have no significant effect on the performances.
- As for the replication phase, this small experiment supports the original's study observation: the ability of GPT 3.5-turbo-instruct to play legal chess games at a high level, seems quite unique among LLMs.
Indeed, the Llama chat model "llama-3.3-70b-versatile" is far from being able to generate a full game: on average, it only plays 10 moves before suggesting an illegal move. In that regard, it does even worse than the "text-davinci-003" completion model (12 legal moves on average). As in the original study, the limited number of generated games and the large variability space make it difficult to establish with any great certainty Llama's inherent inability to understand chess. In particular, since it is a chat model, the role it is given is critical.
- In addition, we tried to make Llama and GPT 3.5-turbo-instruct play Chess960, which they were unable to do successfully: neither model was able to distinguish Chess960 from standard chess. There are, at least, two different reasons that could explain this: firsly, it could be that the Chess960 PGN headers, the role (for the chat model) and the other parameters we used were not adapted, or not sufficient to use the full potential of these 2 LLMs. Secondly, they may not actually be able to play this variant, for example due to the predominance of standard chess games, in the majority of available databases that might have been used for their training (in particular, the training of GPT 3.5-turbo-instruct).

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
 



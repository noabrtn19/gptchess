import chess.pgn
import ipywidgets as widgets
from IPython.display import clear_output
from ipywidgets import Button, HBox, VBox
from IPython.display import SVG, display
import chess.svg 

BOARD_SIZE = 400

class JupyterChessPGN:
    
    board = None
    nm = 0
    
    moves = []
    pos = None 
    out = None # widgets.Output(layout={'border': '1px solid black'})
    out_position = None # widgets.Output(layout={'border': '1px solid red'})
    pgnfile = None
    game = None
    wgames = None
      
    def __init__(self, pgnfile):
        self.pgnfile = pgnfile
    
        
    def read_ith_game(self, i):
        pgn = open(self.pgnfile)
        game_number = 0
        while game_number <= i:
            ga = chess.pgn.read_game(pgn)
            if ga is None:
                return None
            else:
                if (game_number == i):
                    return ga
            game_number = game_number + 1
        return None
    
    def set_ith_game(self, i):
        self.game = self.read_ith_game(i)
        
    def undo_button(self, b):
        
        if (self.nm is not 0):
            self.nm = self.nm - 1
            self.board.pop()

        with self.out_position:
            clear_output(wait=True) 
            display(SVG(chess.svg.board(board=self.board, size=BOARD_SIZE)))
    
    

    def redo_button(self, b):     

        if (self.nm < len(self.moves)):
            m = self.moves[self.nm]
            self.board.push(m)

            with self.out_position:
                clear_output(wait=True) 
                display(SVG(chess.svg.board(board=self.board, size=BOARD_SIZE)))
            self.nm = self.nm + 1
        else:
            return # print("end of the game")
    
    def showUI(self):    
        clear_output()
        self.board = chess.Board()
        self.moves = list(self.game.mainline_moves())
        self.nm = 0
        if (self.out_position is not None):
            self.out_position.clear_output()
        display(self.wgames)

        self.out_position = widgets.Output() # layout={'border': 'px solid red'})
        display(self.out_position)
        with self.out_position:
            display(SVG(chess.svg.board(board=self.board, size=BOARD_SIZE)))
        self.out = widgets.Output()
        with self.out:
            clear_output() 
            self.undo_b = widgets.Button(description="<")
            self.redo_b = widgets.Button(description=">")
            self.undo_b.on_click(self.undo_button)
            self.redo_b.on_click(self.redo_button)
            display(HBox([self.undo_b, self.redo_b]))

        display(self.out)


    def mk_games_information(self, pgnfile):
        games_information = [] 
        pgn = open(self.pgnfile)
        game_number = 1
        while True:
            game = chess.pgn.read_game(pgn)
            if game is None:
                break
            else:
                games_information.append((game.headers.get("White") + "-" + game.headers.get("Black") + " " + game.headers.get("Result") + " (g " + str(game_number) + ")", game_number - 1))
                game_number = game_number + 1
        return games_information
    
    def on_change(self, change):
        ngame = change['new']
        print("NGAME", ngame)
        self.set_ith_game(int(ngame))
        self.showUI()
    
    def make_gamelist_menu(self):
        self.wgames = widgets.Dropdown(
            options=self.mk_games_information(self.pgnfile),
            description='Game:',
            disabled=False    
        )
        self.wgames.observe(self.on_change, names='value')
        display(self.wgames)
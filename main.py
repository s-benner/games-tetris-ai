# import needed packages
import tkinter as tk
import random

# define global variables
APPL_SIZE_X = 500
APPL_SIZE_Y = 750
GRID_UNIT = 30
GRID_SIZE_X = 10
GRID_SIZE_Y = 20
BASE_X = 100
BASE_Y = 120
ROOT = [int(GRID_SIZE_X//2), GRID_SIZE_Y-1]
SPAWNOFFSETS=[[0,-1,-1,0,-1,-1],[0,-1,0,1,-1,-1],[0,-1,0,1,-1,1],[0,-1,0,-2,0,1],[0,-1,0,1,-1,0],[0,-1,-1,-1,-1,-2],[0,1,-1,1,-1,2]]

COLORS = ["black", "red", "green", "yellow", "orange", "blue", "pink", "gray", "white"]

# main application class
# ----------------------
class Application(tk.Tk):
    """This class is the main tkinter object. It inherits from tk.Tk and adds the functionality needed specifically for
    this application"""

    #attributes
    canvases = []
    active_canvas = None

    # constructor method
    def __init__(self, *args, **kwargs):
        # call the Tk constructor from tkinter
        tk.Tk.__init__(self, *args, **kwargs)
        # create canvases
        self.canvases.append(Menu(self))
        self.canvases.append(Tetris(self))

        self.show_canvas(1)
        self.canvases[1].run_game()

    # method to display the desired canvas
    def show_canvas(self, canvas_id):
        if not self.active_canvas == None: self.active_canvas.pack_forget()
        self.active_canvas = self.canvases[canvas_id]
        self.active_canvas.pack()

# parent class for all canvases
# -----------------------------
class GeneralCanvas(tk.Canvas):
    # attributes
    appl = None

    def __init__(self, application):
        super().__init__(width=APPL_SIZE_X, height=APPL_SIZE_Y, background="black", highlightthickness=0)
        self.appl = application

"""class for the menu, extending the general canvas class"""
"""------------------------------------------------------"""
class Menu(GeneralCanvas):

    def __init__(self, application):
        super().__init__(application)

"""class for the actual game, extending the general canvas class"""
"""-------------------------------------------------------------"""
class Tetris(GeneralCanvas):
    # attributes
    gameover = False #game status tracker
    score = 0 #score variable
    squares = [[0 for i in range(GRID_SIZE_X)] for j in range(GRID_SIZE_Y)] #container for all squares of the playing field
    squareobjects = [] #srotes all canvas elements that make up the playing pieces
    boardobjects = [] #stores all canvas elements that make up the playing board
    thispiece = [] #stores where the current moving piece is located
    nextpiece = random.randrange(1,8) #id od the next piece to be spawned

    """constructor method"""
    """------------------"""
    def __init__(self, application):
        super().__init__(application)

    """method that runs the game"""
    """-------------------------"""
    def run_game(self):
        # show the board
        self.show_board()
        # run the actual game loop
        self.game_loop()

    """class for the actual game loop"""
    """------------------------------"""
    def game_loop(self):
        # check if the game is over

        # check if a new piece needs to be generated, if not, the called function will do nothing
        self.nextpiece = self.new_piece(self.thispiece, self.nextpiece)

        # display all pieces on the board
        self.show_squares()

        #loop tail call
        self.after(75,self.game_loop)

    """class that checks if a new piece needs to be spawned and if so executes the spawn"""
    """---------------------------------------------------------------------------------"""
    def new_piece(self, this, next):
        if not this:
            #generate thispiece varibale, storing the locations of the current moving piece
            self.thispiece = [[ROOT[1],ROOT[0]], [ROOT[1]+SPAWNOFFSETS[next-1][0],ROOT[0]+SPAWNOFFSETS[next-1][1]], [ROOT[1]+SPAWNOFFSETS[next-1][2],ROOT[0]+SPAWNOFFSETS[next-1][3]], [ROOT[1]+SPAWNOFFSETS[next-1][4],ROOT[0]+SPAWNOFFSETS[next-1][5]]]
            #set the squares variables, where the current moving piece is located
            for i in range(4): self.squares[self.thispiece[i][0]][self.thispiece[i][1]] = next
            #generate the if of the next new piece to be spawned and return it
            return random.randrange(8)
        else:
            #if no new piece is spawned, just return the current value for nextpiece
            return next

    def show_board(self):
        self.boardobjects.append(self.create_line(BASE_X-1,BASE_Y-1,BASE_X+GRID_SIZE_X*GRID_UNIT+1,BASE_Y-1,BASE_X+GRID_SIZE_X*GRID_UNIT+1,BASE_Y+GRID_SIZE_Y*GRID_UNIT+1,BASE_X-1,BASE_Y+GRID_SIZE_Y*GRID_UNIT+1,BASE_X-1,BASE_Y-1,fill=COLORS[8]))
        for i in range(1,GRID_SIZE_X):
            for j in range(1,GRID_SIZE_Y):
                self.boardobjects.append(
                    self.create_rectangle(BASE_X+GRID_UNIT*i-1, BASE_Y+GRID_UNIT*j-1,BASE_X+GRID_UNIT*i+1, BASE_Y+GRID_UNIT*j+1,fill=COLORS[8]))

    def show_squares(self):
        for row_index, row in enumerate(self.squares):
            for col_index, square in enumerate(row):
                if not square == 0:
                    x1 = BASE_X+(GRID_SIZE_X-col_index-1)*GRID_UNIT
                    y1 = BASE_Y+(GRID_SIZE_Y-row_index-1)*GRID_UNIT
                    self.squareobjects.append(self.create_rectangle(x1,y1,x1+GRID_UNIT-1,y1+GRID_UNIT-1,fill=COLORS[square]))


# Create the root window
root = Application()

# Run the tkinter application
root.mainloop()
# import needed packages
import tkinter as tk
import random

# define global variables
APPL_SIZE_X = 500 #size of the window in x direction
APPL_SIZE_Y = 750 #size of the window in y direction
GRID_UNIT = 30 #size of one board grid unit
GRID_SIZE_X = 10 #number of board grid units in x direction
GRID_SIZE_Y = 20 #numbe of board grid units in y direction
BASE_X = 100 #beginning of actual game board in x direction
BASE_Y = 120 #beginning of actual game board in y direction
ROOT = [int(GRID_SIZE_X//2), GRID_SIZE_Y-1] #indices of the root cell where new pieces spawn
SPAWNOFFSETS=[[0,-1,-1,0,-1,-1],[0,-1,0,1,-1,-1],[0,-1,0,1,-1,1],[0,-1,0,-2,0,1],[0,-1,0,1,-1,0],[0,-1,-1,-1,-1,-2],[0,1,-1,1,-1,2]] #offsets from the root cell of a piece for the other squares
ROOTOFFSETS = [] #used to determine the squares of a piece relative to the root square
ROOTOFFSETS.append([[0,-1,-1,0,-1,-1],[0,-1,0,1,-1,-1],[0,-1,0,1,-1,1],[0,-1,0,-2,0,1],[0,-1,0,1,-1,0],[0,-1,-1,-1,-1,-2],[0,1,-1,1,-1,2]])
ROOTOFFSETS.append([[0,-1,-1,0,-1,-1],[0,-1,0,1,-1,-1],[0,-1,0,1,-1,1],[0,-1,0,-2,0,1],[0,-1,0,1,-1,0],[0,-1,-1,-1,-1,-2],[0,1,-1,1,-1,2]])
ROOTOFFSETS.append([[0,-1,-1,0,-1,-1],[0,-1,0,1,-1,-1],[0,-1,0,1,-1,1],[0,-1,0,-2,0,1],[0,-1,0,1,-1,0],[0,-1,-1,-1,-1,-2],[0,1,-1,1,-1,2]])
ROOTOFFSETS.append([[0,-1,-1,0,-1,-1],[0,-1,0,1,-1,-1],[0,-1,0,1,-1,1],[0,-1,0,-2,0,1],[0,-1,0,1,-1,0],[0,-1,-1,-1,-1,-2],[0,1,-1,1,-1,2]])
COLORS = ["black", "red", "green", "yellow", "orange", "blue", "pink", "gray", "white"] #list of colors the game uses
FRAMERATE = 60 #intended frames per second
HOLD = 1000//FRAMERATE #holdtime for the intended framerate in milliseconds
SPEEDFACTOR = 3 #is multiplied with the current gamespeed to determine the number of frames between drops
ROWCOMPLETESCORES = [0,10,50,250,1000] #scores for completed rows

"""main application class"""
"""----------------------"""
class Application(tk.Tk):

    #attributes
    canvases = [] #list for the canvases the application uses
    active_canvas = None #index of the currently active canvas

    #constructor method
    def __init__(self, *args, **kwargs):
        #call the Tk constructor from tkinter
        tk.Tk.__init__(self, *args, **kwargs)
        #create canvases
        self.canvases.append(Menu(self))
        self.canvases.append(Tetris(self))
        #show the game canvas, run the game
        self.show_canvas(1)
        self.canvases[1].run_game()

    #method to display the desired canvas
    def show_canvas(self, canvas_id):
        if not self.active_canvas == None: self.active_canvas.pack_forget()
        self.active_canvas = self.canvases[canvas_id]
        self.active_canvas.pack()

"""parent class for all canvases"""
"""-----------------------------"""
class GeneralCanvas(tk.Canvas):
    #attributes
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
    #attributes
    gameover = False #game status tracker
    score = 0 #score variable
    squares = [[0 for i in range(GRID_SIZE_X)] for j in range(GRID_SIZE_Y)] #container for all squares of the playing field
    squareobjects = [] #srotes all canvas elements that make up the playing pieces
    boardobjects = [] #stores all canvas elements that make up the playing board
    thispiece = [] #stores where the current moving piece is located
    thispieceid = 0 #stores the type of the current moving piece
    thispiecerotation = 0 #stores the rotation of the current moving piece
    nextpiece = random.randrange(1,8) #id od the next piece to be spawned
    speed = 10 #speed of the game in 'drop every speed*SPEEDFACTOR frames', therefore 10 is slowest and 1 is fastest
    framecounter = 1 #used to count the frames until the next drop
    legalinputs = ["Left","Right","Down","Up"] #input for event handling
    rowscleared = 0 #keeps track of the number of rows cleared

    """constructor method"""
    """------------------"""
    def __init__(self, application):
        super().__init__(application)
        self.bind_all("<Key>", self.key_press) #for the keyboard event handling
    """method that runs the game"""
    """-------------------------"""
    def run_game(self):
        self.nextpiece = self.new_piece(self.thispiece, self.nextpiece)
        self.game_loop()
        #after game_loop is completed, call the game over screen

    """method for the actual game loop"""
    """------------------------------"""
    def game_loop(self):
        #check if the game is over, if so, return out of the game_loop
        if self.gameover: return
        #check if a drop needs to be executed, if so, call the function
        if self.framecounter % (SPEEDFACTOR*self.speed) == 0:
            self.framecounter = 0
            self.drop()
        #display all pieces on the board
        self.show_squares()
        #increment framecounter
        self.framecounter += 1
        #loop tail call
        self.after(HOLD,self.game_loop)

    """method for keyboard input handling"""
    """----------------------------------"""
    def key_press(self, e):
        if not e.keysym in self.legalinputs: return
        newposition = []
        #if the right key has been pressed, the piece is supposed to move in negative x direction
        if e.keysym == "Right": newposition = [[self.thispiece[i][0], self.thispiece[i][1] - 1] for i in range(4)]
        #if the left key has been pressed, the piece is supposed to move in positive x direction
        if e.keysym == "Left": newposition = [[self.thispiece[i][0], self.thispiece[i][1] + 1] for i in range(4)]
        #if the up key has been pressed, the piece is supposed to rotate by 90 degrees
        if e.keysym == "Up":
            self.thispiecerotation = (self.thispiecerotation + 1) % 4
        #if the down key has been pressed, the piece is supposed to move down
        if e.keysym == "Down":
            self.drop()
            return
        collision = self.check_collision(newposition)
        if not collision: self.update_position(newposition)

    """method that executes a drop of 1 unit down"""
    """------------------------------------------"""
    def drop(self):
        #calculate the new position
        newposition = [ [self.thispiece[i][0]-1,self.thispiece[i][1]] for i in range(4) ]
        #check for collision, if so, then do not drop, but rather convert the moving peace to static. if there is not collision then update position
        collision = self.check_collision(newposition)
        if collision: self.make_piece_static()
        else: self.update_position(newposition)

    """method that checks for collision with a newposition provided"""
    """------------------------------------------------------------"""
    def check_collision(self,newposition):
        #check if the bottom or top is reached
        if min(newposition[i][0] for i in range(4)) == -1 or max(newposition[i][0] for i in range(4)) == GRID_SIZE_Y: return True
        #check for collision with left or right wall
        if min(newposition[i][1] for i in range(4)) == -1 or max(newposition[i][1] for i in range(4)) == GRID_SIZE_X: return True
        #check for collisions with existing pieces
        for i in range(4):
            if not newposition[i][1] in range(GRID_SIZE_X): continue
            if not self.squares[newposition[i][0]][newposition[i][1]] == 0: return True
        #return default
        return False

    """method that makes the moving piece static after a collision on the bottom"""
    """-------------------------------------------------------------------------"""
    def make_piece_static(self):
        #add thispiece data to squares
        for i in range(4):
            self.squares[self.thispiece[i][0]][self.thispiece[i][1]] = self.thispieceid
        #remove this piece data, such that a new piece will be spawned
        self.thispiece = []
        self.thispieceid = 0
        #increase the score
        self.score += (11-self.speed)
        self.check_and_remove_complete_rows()
        self.nextpiece = self.new_piece(self.thispiece, self.nextpiece)

    """method that checks if rows are completed and removes them if so"""
    """---------------------------------------------------------------"""
    def check_and_remove_complete_rows(self):
        #check for completed rows and return if none
        rows_complete = []
        for i in range(GRID_SIZE_Y):
            if self.squares[i].count(0) == 0: rows_complete.append(i)
        if not rows_complete: return
        leng = len(rows_complete)
        #add score for complete rows and increase rows complete counter
        self.score += ROWCOMPLETESCORES[leng]
        self.rowscleared += leng
        #remove the cleared rows
        squares_new = []
        for i in range(GRID_SIZE_Y):
            if not i in rows_complete: squares_new.append(self.squares[i])
        filler = [0 for i in range(GRID_SIZE_X)]
        for j in range(leng): squares_new.append(filler)
        self.squares = squares_new
        if self.rowscleared > (11 - self.speed) * 10: self.speed = max(self.speed - 1,1)

    """method that updates the position of the moving piece (used for drop and rotate)"""
    """-------------------------------------------------------------------------------"""
    def update_position(self, newposition):
        self.thispiece = newposition

    """method that checks if a new piece needs to be spawned and if so executes the spawn"""
    """---------------------------------------------------------------------------------"""
    def new_piece(self, this, next):
        if not this:
            #generate thispiece varibale, storing the locations of the current moving piece
            self.thispiece = [[ROOT[1],ROOT[0]], [ROOT[1]+SPAWNOFFSETS[next-1][0],ROOT[0]+SPAWNOFFSETS[next-1][1]], [ROOT[1]+SPAWNOFFSETS[next-1][2],ROOT[0]+SPAWNOFFSETS[next-1][3]], [ROOT[1]+SPAWNOFFSETS[next-1][4],ROOT[0]+SPAWNOFFSETS[next-1][5]]]
            self.thispieceid = next
            self.thispiecerotation = 0
            #check for collisions
            collision = self.check_collision(self.thispiece)
            if collision: self.gameover = True
            #generate the id of the next new piece to be spawned and return it
            return random.randrange(1,8)
        else:
            #if no new piece is spawned, just return the current value for nextpiece
            return next

    """method that displays the board on the screen"""
    """--------------------------------------------"""
    def show_board(self):
        self.boardobjects.append(self.create_line(BASE_X-1,BASE_Y-1,BASE_X+GRID_SIZE_X*GRID_UNIT+1,BASE_Y-1,BASE_X+GRID_SIZE_X*GRID_UNIT+1,BASE_Y+GRID_SIZE_Y*GRID_UNIT+1,BASE_X-1,BASE_Y+GRID_SIZE_Y*GRID_UNIT+1,BASE_X-1,BASE_Y-1,fill=COLORS[8]))
        for i in range(1,GRID_SIZE_X):
            for j in range(1,GRID_SIZE_Y):
                self.boardobjects.append(self.create_rectangle(BASE_X+GRID_UNIT*i-1, BASE_Y+GRID_UNIT*j-1,BASE_X+GRID_UNIT*i+1, BASE_Y+GRID_UNIT*j+1,fill=COLORS[8]))
        self.boardobjects.append(self.create_text(20,20, text=f"Score: {self.score}", fill="white", font="TkDefaultFont"))
        self.boardobjects.append(self.create_text(200,20, text=f"Level: {11-self.speed}", fill="white", font="TkDefaultFont"))
        self.boardobjects.append(self.create_text(400, 20, text=f"Rows Cleared: {self.rowscleared}", fill="white", font="TkDefaultFont"))

    """method that display all the squares making up the pieces and also other dynamic content like the score and the next piece"""
    """-------------------------------------------------------------------------------------------------------------------------"""
    def show_squares(self):
        self.delete("all")
        self.squareobjects = []
        self.show_board()
        #show static pieces
        for row_index, row in enumerate(self.squares):
            for col_index, square in enumerate(row):
                if not square == 0:
                    x1 = BASE_X+(GRID_SIZE_X-col_index-1)*GRID_UNIT
                    y1 = BASE_Y+(GRID_SIZE_Y-row_index-1)*GRID_UNIT
                    self.squareobjects.append(self.create_rectangle(x1,y1,x1+GRID_UNIT-1,y1+GRID_UNIT-1,fill=COLORS[square]))
        #show moving piece
        for loc in self.thispiece:
            x1 = BASE_X + (GRID_SIZE_X - loc[1] - 1) * GRID_UNIT
            y1 = BASE_Y + (GRID_SIZE_Y - loc[0] - 1) * GRID_UNIT
            self.squareobjects.append(self.create_rectangle(x1,y1,x1+GRID_UNIT-1,y1+GRID_UNIT-1,fill=COLORS[self.thispieceid]))

#create the root window
root = Application()

#run the tkinter application
root.mainloop()
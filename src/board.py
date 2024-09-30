import random
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d



#given an int, return a string colour
def getColor(color):
    colorString = ""
    match color:
        case 0: # Red
            colorString = "r"
        case 1: # Blue
            colorString = "b"
        case 2: # Cyan
            colorString = "c"
        case 3: # Yellow
            colorString = "#c99100"
        case 4: # Brown/green
            colorString = "#3cc900"
        case 5: # Pink
            colorString = "#ff00ef"
        case 6: # Purple
            colorString = "#c50cba"
        case _: #Unknown (Black)
            colorString = "k"

    return colorString


class Board:
    def __init__(self, tokenList, userMoves = None, radius = 0.5):
        self.tokenCount = 7 # there are x of each token, in x types
        self.radius = radius # Used for plotting only

        self.tokenList_initial = tokenList # Where all the game pices were at the start
        self.tokenList_active = tokenList # Where all the game pieces are now

        # user data
        self.userMoves = userMoves
        self.userPieces = np.zeros((2, self.tokenCount))
    
    # Interact with the game
    def placeUserToken(self):
        '''Add one of the users pieces, 
        remove the two colinear tokens and give them to the user.'''
        pass

    # Calculate game features
    def findPotentialMoves(self):
        '''Analyse the active tokens and return a list of moves'''
        pass

    def calculateWinner(self) -> int:
        '''return the game winner, either player 1 or 2. 
            Negative value if not finished'''
        pass

    # Display, visualisation methods
    def viewBoard(self):
        # Draw voranoi diagram and user moves
        if self.userMoves is not None:
            pointsXY = np.array([[x, y] for x,y,i in self.userMoves])
            v = Voronoi(pointsXY)
            voronoi_plot_2d(v)

        # Add tokens
        for t in self.tokenList:
            plt.plot(t[0], t[1], color=getColor(t[2]), marker='x')
        
        boardCircle = plt.Circle((0, 0), self.radius, color='k', fill=False, linewidth=1, linestyle='-' )
        plt.gca().add_patch(boardCircle)

        plt.title("Lacuna Image")
        plt.gca().set_aspect('equal')

        ax = plt.gca()
        ax.set_xlim([-(self.radius+0.05), (self.radius+0.05)])
        ax.set_ylim([-(self.radius+0.05), (self.radius+0.05)])

        plt.show()



# Methods to process the image and create a board
def newBoard(filename):
    pass

# new Board with random data
def newBoard(size = 7, radius=0.50):
    tokenList = []
    for i in range(size): # how many colours
        for _ in range(size): # how many of each colour
            inCircle = False

            while not inCircle:
                x = random.uniform(-radius, radius)
                y = random.uniform(-radius, radius)
                
                inCircle = radius > math.sqrt(math.pow(x,2) + math.pow(y,2))

            tokenList.append([x,y,i])

    return tokenList






if __name__ == "__main__":
    radius = 0.5
    tokens = newBoard()

    board = Board(tokens)
    board.viewBoard()

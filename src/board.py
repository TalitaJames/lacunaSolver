'''
Made By: Talita James
Last Edited: 2024-10

This code interacts with a "Board" of lacuna tiles.
A token is a tupple of the form (x,y,type)
- Where type is the integer representing 0-6 its colour

Notes:
Its unlikely the token list will stay exact each time the CV algorithm runs
'''

import random
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
import networkx as nx
import time
import itertools

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
        '''Create a board'''

        self.tokenCount = int(math.sqrt(len(tokenList))) # there are x of each token, in x types
        self.radius = radius # Used for plotting only

        self.tokenGraph = nx.Graph()
        self.tokenGraph.add_nodes_from(tokenList)

        # self.tokenList_initial = tokenList # Where all the game pices were at the start
        # self.tokenList_active = tokenList # Where all the game pieces are now

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
        '''Analyse the active tokens and return a list of all valid moves'''

        # Attach an edge to each node of the same colour:
        for i in range(self.tokenCount):
            nodeIDs = [node for node, atribute in self.tokenGraph.nodes().items() if atribute['type'] == i]
            edges = itertools.combinations(nodeIDs, 2)
            self.tokenGraph.add_edges_from(edges)

        # Sort nodes by x,y
        # then check which is smaller (x or y)
        # then check nodes in the the x1 to x2 range (or y if smaller)
        # if nodes intersect
        # get list [x sort]
        # get y then pick

        # Check if the node is uninterupted colliniar (aka valid)
        for edge in self.tokenGraph.edges:
            collision = False
            # the position of each node (x,y)
            (x1,y1) = self.tokenGraph.nodes[edge[0]]['pos']
            (x2,y2) = self.tokenGraph.nodes[edge[1]]['pos']

            # Brute force, check all nodes approach:
            m = (y2-y1)/(x2-x1)
            c = (y1-m*x1)

            print(f"checking edge {edge} at ({x1},{y1}), ({x2},{y2})")
            for node, attribute in self.tokenGraph.nodes().items():            #TODO speed up
                (xn,yn) = attribute['pos']
                # print(f"checking edge {edge} at ({x1},{y1}) and ({x2},{y2}) compared to node ({xn},{yn})")
                if node in edge:
                    print(f"skipped self")
                    continue

                print(f"({xn},{yn})")
                lineformula = abs(m*xn+c-yn)

                if(min(x1,x2) <= xn <= max(x1,x2) and min(y1,y2) <= yn <= max(y1,y2) and lineformula <= 0.04):
                    # print(f"\tRemoved edge {edge}")
                    self.tokenGraph.remove_edge(*edge)
                    collision = True
                    break
            print(f"\tKept edge {edge}") if not collision else ""


    def calculateWinner(self) -> int:
        '''return the game winner, either player 1 or 2.
            Negative value if not finished'''
        pass

    # Display, visualisation methods
    def getGraph(self):
        return self.tokenGraph

    def viewBoard(self):
        # # Draw voranoi diagram and user moves
        # if self.userMoves is not None:
        #     pointsXY = np.array([[x, y] for x,y,i in self.userMoves])
        #     v = Voronoi(pointsXY)
        #     voronoi_plot_2d(v)

        # # Add tokens
        # for t in self.tokenList:
        #     plt.plot(t[0], t[1], color=getColor(t[2]), marker='x')

        # boardCircle = plt.Circle((0, 0), self.radius, color='k', fill=False, linewidth=1, linestyle='-' )
        # plt.gca().add_patch(boardCircle)

        # plt.title("Lacuna Image")
        # plt.gca().set_aspect('equal')

        # ax = plt.gca()
        # ax.set_xlim([-(self.radius+0.05), (self.radius+0.05)])
        # ax.set_ylim([-(self.radius+0.05), (self.radius+0.05)])

        nx.draw(self.tokenGraph)  # networkx draw()
        plt.draw()  # pyplot draw()
        plt.show()


# Methods to process the image and create a board

# new Board with random data
def newRandomBoard(size = 7, radius=0.50):
    '''Get a list of complete rangomly generated tokens '''
    tokenList = []
    for i in range(size): # how many colours
        for j in range(size): # how many of each colour
            inCircle = False

            while not inCircle:
                x = round(random.uniform(-radius, radius),3)
                y = round(random.uniform(-radius, radius),3)

                inCircle = radius > math.sqrt(math.pow(x,2) + math.pow(y,2))

            nodeAttribute = {"pos": (x,y), "type": i}
            newData=(i*size+j, nodeAttribute)
            tokenList.append(newData)
    return tokenList


if __name__ == "__main__":
    print("-----\n")
    timestamp = time.strftime("%Y%m%d-%H%M%S",time.localtime())

    tokens = newRandomBoard()
    board = Board(tokens)
    board.findPotentialMoves()
    # board.viewBoard()

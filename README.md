# Lacuna solver
> Solving the board game [Lacuna](https://boardgamegeek.com/boardgame/386937/lacuna) using computer vision (CV) and game theory.
This project compares three CV approaches of template matching, colour manipulation and machine learning

## Image Pre-proscessing
### Circle crop
> Takes a full coloured image and crops it by the game boards circle

**Errors in sample images**: 1, 13, 14
- one error is due to the mat not allways being centered in img
- potential good idea to first crop to square

**Good examples**: 5



## Approach to the game:
```txt
Get initial image:
    Clasify the image
	    Method to extract the circle
	    perform CV on rest of image

Work out potential moves
Simulate the game with [a min-max algorithn (+ alpha beta pruning)](https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/)

Return return best move

Get new image (move taken)
- work out what was taken (and record who it belongs to)
- calculate new potential moves as above
- calculate and return best 

When all moves are taken (ie each user has placed 6 tokens)
- Calculate the voranoi diagram
- and which remaining tokens are whos
```

## Structure:
### File plan
```txt
.
├── images/
│   ├── templates/
│   │   └── # all template images
│   └── initalGame/
│       └── # all images of the board (no turns)
├── out/
│   ├── progress/
│   │   ├── README.md
│   │   └── # update images, graphs, plots ect
│   └── logs/
│       └── # all log files
├── src/
│   ├── board.py # Classes ect to make the board
│   └── imageProsessingSuit # Input: image,  output: Board
└── requirements.txt
└── README.md
```
Made with [tree by Nathan Friend](https://tree.nathanfriend.io/)

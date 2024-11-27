# DS5100-finalproject: Monte Carlo Module Simulator
This is the GitHub repo containing the Monte Carlo Module Simulator I created as the final project for DS5100 course.


## Metadata: 
Name: Hai Liu \
Project Name: Monte Carlo Simulator \


## Synopsis:
Show brief demo code of how the classes are used, i.e. code snippets showing how to install, import, and use the code to (1) create dice, (2) play a game, and (3) analyze a game. You can use preformatted blocks for the code.
```
# Install the package in terminal


# Import libraries and classes
import numpy as np
import pandas as pd
from montecarlo.montecarlo import Die, Game, Analyzer

# Create two dice
die1 = Die()
die2 = Die()

# Modify weights
die1.change_weight(1, 5.0)

# Play a game with two dice
game = Game([die1, die2])
game.play(rolls=10)

# Analyze the results of a game
analyzer = Analyzer(game)
print("Number of jackpots:", analyzer.jackpot())
print("Face counts per roll:\n", analyzer.face_count())
print("Combination counts:\n", analyzer.combo_count())
```


## API description: A list of all classes with their public methods and attributes. Each item should show their docstrings. All parameters (with data types and defaults) should be described. All return values should be described. Do not describe private methods and attributes.

### 1. `Die` Class
Represents a die that can have any number of sides with customizable weights.

- **Methods**:
  `__init__(sides=np.arange(1,7))`
  Initializes the die with sides (default: a six-sided die) and assigns equal weights to all sides.
    - Parameters:
         - sides: A NumPy array of distinct values representing the die faces.
    - Raises:
         - TypeError: If sides is not a NumPy array.
         - ValueError: If sides contains duplicate values.
    
  `change_weight(face, weight)`
  Updates the weight of a specific side of the die.
    - Parameters:
         - face: The face of the die to modify.
         - weight: The new weight (must be numeric).
    - Raises:
         - IndexError: If face is not a valid side.
         - TypeError: If weight is not numeric.

roll_die(n=1)
Rolls the die n times and returns the results as a list.
Parameters:

n: Number of rolls (default: 1).
die_status()
Returns the current state of the die as a pandas DataFrame.

### 2. Game Class
Represents a game consisting of rolling multiple similar dice.

Methods:
__init__(dicelist)
Initializes the game with a list of Die objects.
Raises:

TypeError: If any element in dicelist is not a Die.
ValueError: If the dice do not have the same faces.
play(rolls)
Rolls all dice a specified number of times and stores the results.
Parameters:

rolls: Number of rolls for the game.
show_result(form='wide')
Displays the results of the most recent play.
Parameters:

form: The format of the results ('wide' or 'narrow', default: 'wide').
Raises:
ValueError: If an invalid format is provided.

### 3. Analyzer Class
Provides statistical analysis tools for the results of a Game.

Methods:
__init__(game)
Initializes the analyzer with a Game object.
Raises:

ValueError: If the argument is not a Game object.
jackpot()
Calculates the number of rolls where all dice show the same face.
Returns:

An integer representing the number of jackpots.
face_count()
Computes how often each face is rolled per roll.
Returns:

A pandas DataFrame of counts.
combo_count()
Computes the distinct combinations of faces rolled and their frequencies.
Returns:

A pandas DataFrame with combination counts.
permu_count()
Computes the distinct permutations of faces rolled and their frequencies.
Returns:

A pandas DataFrame with permutation counts.

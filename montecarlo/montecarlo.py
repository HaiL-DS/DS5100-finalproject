import numpy as np
import pandas as pd

class Die:
    """
    This is a “Die” class that can be any discrete random variable associated with a stochastic process, 
    such as using a deck of cards, flipping a coin, rolling an actual die, or speaking a language.
    """
    
    def __init__(self, sides=np.arange(1,7)):
        """Initalize the object by defining the number of faces and the default die weights.
           The initalizer takes a single argument of a NumPy array as the number of faces.
           The NumPy array’s data type may be strings or numbers, but the values must be distinct.
           By default, it internally initializes a die with 6 faces and weights of 1.0 for each face.
        """
        
        if not isinstance(sides, np.ndarray):     #check if argument is a NumPy array
            raise TypeError("Die sides must be a NumPy array!")
        elif len(sides) != len(set(sides)):       #check if array values are distinct 
            raise ValueError("Die side values must be distinct!")            
        else:
            self.sides = sides
            
        self.weights = np.ones(len(sides))
        self.die = pd.DataFrame({'sides': self.sides, 'weights': self.weights}).set_index('sides')
        
    def change_weight(self, face, weight):
        """A method to change the weight of a single side or face.
           It takes two arguments: the face value to be changed and its new weight.
        """
        
        if face not in list(self.die.index):     #check if the face passed is valid
            raise IndexError("This side of the die does not exist!")
        elif not isinstance(weight, (int, float)):     #check if the weight is a valid value type (integer or float)
            raise TypeError("Weight can only be numeric (integer or float)!")
        else:
            self.die.weights[self.die.index == face] = weight
            
    def roll_die(self, n=1):
        """A method to roll the die one or more times. Returning a Python list of outcomes
           It takes a parameter of how many times the die is to be rolled (defaults to 1).
           The function returns a Python list of outcomes (from random sampling with replacement by weights).
        """
        
        return list(pd.Series(self.die.index).sample(n, replace=True, weights=list(self.die.weights)).values)
    
    def die_status(self):
        """A method to show the die’s current state. It returns a copy of the private die data frame."""
        
        return self.die.copy()
        
        
class Game:
    """
    This is a "Game" class that consists of rolling of one or more similar dice (Die objects) one or more times.
    The class initalizer takes a single parameter, a list of already instantiated similar dice.
    The Game objects have a behavior to play a game, i.e. to roll all of the dice a given number of times, and
    only keep the results of their most recent play.
    """
    
    def __init__(self, dicelist):
        """
        Game initializer that takes a single parameter, a list of already instantiated similar dice.
        """
        
        for d in dicelist:
            if not isinstance(d, Die):    #check if parameter elements are Die objects                          
                raise TypeError("The list must contain Die objects!")    
            elif list(d.die.index) != list(dicelist[0].die.index):   #check if all Die objects have the same faces
                raise ValueError("Dice must have the same faces!") 
                
        self.dicelist = dicelist 
    
    def play(self, rolls):
        """
        A play method that takes an integer parameter to specify how many times the dice should be rolled.
        Results are saved to a private data frame in wide format, with the roll number as a named index, 
        columns for each die number (dice list index as column names), and the face rolled in that instance in each cell.
        """
        
        self.result = pd.DataFrame({'RollNo.': list(range(1, rolls+1))})
        for i in range(len(self.dicelist)):
            self.result[i+1] = self.dicelist[i].roll_die(rolls)
         
        self.resultdf = self.result.set_index("RollNo.")
    
    def show_result(self, form="wide"):
        """
        A method to show the user the results of the most recent play. It takes a parameter to return the data frame
        in "narrow" or "wide" form (defaults to "wide" for the form argument).
        """
        
        if form == "wide":
            return self.resultdf.copy()
        elif form == "narrow":
            narrowed = self.resultdf.copy().stack().to_frame('FaceRolled')
            narrowed.index.names = ['RollNo.', 'DieNo.']
            return narrowed
        else:
            raise ValueError("Passed an invalid option for the form of narrow or wide!")
            
    
class Analyzer:
    """
    An Analyzer object takes the results of a single game and computes various descriptive statistical properties about it.
    """
    
    def __init__(self, game):
        """
        Analyzer initializer that takes a game object as its input argument.
        """
        
        if not isinstance(game, Game):    #check if argument is a Game objects   
            raise ValueError("The argument must be a Game object!")  
        self.game = game
    
    def jackpot(self):
        """
        A jackpot method that computes how many times the game resulted in all faces being the same.
        It returns an integer as the number of jackpots.
        """
        
        gameresult = self.game.show_result(form = "wide")
        jps = 0
        for roll in range(len(gameresult)):
            if len(set(list(gameresult.iloc[roll, :]))) == 1:
                jps += 1
                
        return jps
            
    def face_count(self):
        """
        A face counts per roll method that computes how many times a given face is rolled in each event.
        It returns a data frame of results.
        """
        
        gameresultnarrow = self.game.show_result(form = "narrow")
        face_count = gameresultnarrow.reset_index().groupby("RollNo.")["FaceRolled"].value_counts().to_frame("Counts").unstack("FaceRolled")
        return face_count.fillna(0)
    

    def combo_count(self):
        """
        A combo count method that computes the distinct combinations of faces rolled, along with their counts.
        It returns a data frame of results.
        """
        
        gameresultnarrow = self.game.show_result(form = "narrow")
        facecombos = gameresultnarrow.groupby('RollNo.')["FaceRolled"].apply(list).to_frame("FaceCombos")["FaceCombos"].apply(sorted).reset_index()
        return facecombos["FaceCombos"].value_counts().to_frame('ComboCounts').sort_index()
    

    def permu_count(self):
        """
        An permutation count method that computes the distinct permutations of faces rolled, along with their counts.
        It returns a data frame of results.
        """
        
        gameresultnarrow = self.game.show_result(form = "narrow")
        facepermus = gameresultnarrow.groupby('RollNo.')["FaceRolled"].apply(list).to_frame("FacePermutations").reset_index()
        return facepermus["FacePermutations"].value_counts().to_frame("PermuCounts").sort_index()
    
    
    

import unittest
import numpy as np
import pandas as pd
from montecarlo.montecarlo import Die, Game, Analyzer


class MontecarloTestSuite(unittest.TestCase):
   
    def test_01_Die_init_if_error_raised(self): 
        """
        Test if Die's __init__() method successfully raises TypeError or ValueError
        if the input parameter is not a NumPy array or contains nondistinct values.
        """
        self.assertRaises(TypeError, Die, [1,2,3,4,5,6])   #check if TypeError raised
        self.assertRaises(ValueError, Die, np.array([1,1,1,4,5,6]))   #check if ValueError raised
    
    def test_02_Die_change_weight(self): 
        """
        Test if change_weight() method successfully changes the weight of a specific
        face of a die.
        """
        test_die = Die()
        test_die.change_weight(6, 9.0)  #change the weight of face 6 from 1.0 to 9.0.
        expected = 9.0
        self.assertEqual(test_die.die.weights[6], expected)     
                                 
    def test_03_Die_roll_die(self): 
        """
        Test if roll_die() method successfully genereates Python list of correct number of elements as outcomes.
        """
        test_die = Die()
        actual = test_die.roll_die(n=5)  #roll a die five times.
        expected = 5
        message = "roll_die() function did not return a list."
        self.assertTrue(isinstance(actual, list), message)   #check if the function returns a list
        self.assertEqual(len(actual), expected)   #check if the function returns correct number of results
        
    def test_04_Die_roll_die(self): 
        """
        Test if roll_die() method successfully genereates Python list of correct number of elements as outcomes.
        """
        test_die = Die()
        actual = test_die.roll_die(n=5)  #roll a die five times.
        expected = 5
        message = "roll_die() function did not return a list."
        self.assertTrue(isinstance(actual, list), message)   #check if the function returns a list
        self.assertEqual(len(actual), expected)   #check if the function returns correct number of results    
                                        
    def test_05_Die_die_status(self): 
        """
        Test if die_status() method successfully returns a Python Pandas DataFram showing the die’s current state.
        """
        test_die = Die()
        actual = test_die.die_status()
        message = "die_status() function did not return a data frame."
        self.assertTrue(isinstance(actual, pd.DataFrame), message)                               
    
    
    def test_06_Game_init_if_error_raised(self): 
        """
        Test if Game's __init__() method successfully raises TypeError or ValueError if the input parameter is not
        a list of instantiated die objects or not all of the dice have the same faces.
        """
        test_die1 = Die()  #instantiate three dice, first two dice have 6 faces, third one has 16.
        test_die2 = Die()
        test_die3 = Die(sides=np.arange(1,17))     
        self.assertRaises(TypeError, Game, ["Die1", "Die2", "Die3"])   #check if TypeError raised
        self.assertRaises(ValueError, Game, [test_die1, test_die2, test_die3])   #check if ValueError raised.
        
    def test_07_Game_play(self): 
        """
        Test if play() method successfully returns a Python Pandas DataFram showing correct game results.
        """
        test_die1 = Die()  #instantiate three dice
        test_die2 = Die()
        test_die3 = Die()
        test_game = Game([test_die1, test_die2, test_die3])  #instantiate a game object
        test_game.play(10)  #roll the three dice 10 times
        actual = test_game.resultdf
        expected_rolls = 10
        expected_dice = 3
        self.assertEqual(len(actual), expected_rolls)   #check if all roll reuslts are stored
        self.assertEqual(len(actual.columns), expected_dice)  #check if all die reuslts are stored                              
                                 
    def test_08_Game_show_result(self): 
        """
        Test if show_result() method returns correct forms of result data frames.
        """
        test_die1 = Die()  #instantiate three dice
        test_die2 = Die()
        test_die3 = Die()
        test_game = Game([test_die1, test_die2, test_die3])  #instantiate a game object
        test_game.play(10)  #roll the three dice 10 times
        actual_wide = test_game.show_result(form="wide")
        actual_narrow = test_game.show_result(form="narrow")
        message = "show_result() function did not return a data frame."
        self.assertTrue(isinstance(actual_wide, pd.DataFrame), message) 
        self.assertTrue(isinstance(actual_narrow, pd.DataFrame), message)           
        self.assertRaises(ValueError, test_game.show_result, " ")    #check if ValueError raised
  

    def test_09_Analyzer_init_if_error_raised(self): 
        """
        Test if Analyzer's __init__() method successfully raises a ValueError
        if the passed value is not a Game object.
        """
        self.assertRaises(ValueError, Analyzer, "Game")   #check if ValueError raised   
        
    def test_10_Analyzer_jackpot(self): 
        """
        Test if jackpot() method returns a integer.
        """
        test_die1 = Die()  #instantiate three dice
        test_die2 = Die()
        test_die3 = Die()
        test_game = Game([test_die1, test_die2, test_die3])  #instantiate a Game object
        test_game.play(10)  #roll the three dice 10 times
        test_analyzer1 = Analyzer(test_game)  #instantiate an Analyzer object                         
        actual = test_analyzer1.jackpot()  
        message = "jackpot() function did not return an integer."
        self.assertTrue(isinstance(actual, int), message)                         

    def test_11_Analyzer_face_count(self): 
        """
        Test if face_count() method returns a data frame with correct structure.
        """
        test_die1 = Die()  #instantiate three dice
        test_die2 = Die()
        test_die3 = Die()
        test_game = Game([test_die1, test_die2, test_die3])  #instantiate a Game object
        test_game.play(10)  #roll the three dice 10 times
        test_analyzer1 = Analyzer(test_game)  #instantiate an Analyzer object                         
        actual = test_analyzer1.face_count()
        expected_rolls = 10
        expected_faces = len(test_die1.die.index)                         
        self.assertEqual(len(actual), expected_rolls)   #check if all roll events are stored                        
        self.assertEqual(len(actual.columns), expected_faces)  #check if all roll faces are stored                       
                                 
                                                                                               
    def test_12_Analyzer_combo_count(self):
        """
        Test if combo_count() method returns a data frame with correct structure.
        """
        test_die1 = Die()  #instantiate three dice
        test_die2 = Die()
        test_die3 = Die()
        test_game = Game([test_die1, test_die2, test_die3])  #instantiate a Game object
        test_game.play(10)  #roll the three dice 10 times
        test_analyzer1 = Analyzer(test_game)  #instantiate an Analyzer object                         
        actual = test_analyzer1.combo_count()
        message = "combo_count() function did not return a data frame."
        self.assertTrue(isinstance(actual, pd.DataFrame), message)  #check if data frame returned

    
    def test_13_Analyzer_permu_count(self):
        """
        Test if combo_count() method returns a data frame with correct structure.
        """
        test_die1 = Die()  #instantiate three dice
        test_die2 = Die()
        test_die3 = Die()
        test_game = Game([test_die1, test_die2, test_die3])  #instantiate a Game object
        test_game.play(10)  #roll the three dice 10 times
        test_analyzer1 = Analyzer(test_game)  #instantiate an Analyzer object                         
        actual = test_analyzer1.permu_count()
        message = "permu_count() function did not return a data frame."
        self.assertTrue(isinstance(actual, pd.DataFrame), message)  #check if data frame returned 
         
 
                                 
if __name__ == '__main__':
    
    unittest.main(verbosity=3)
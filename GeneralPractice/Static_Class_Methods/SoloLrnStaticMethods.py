"""
Static Methods

Static methods are similar to class methods, except they don't 
receive any additional arguments; they are identical to normal 
functions that belong to a class. 

They are marked with the staticmethod decorator.
Example:
"""

class Pizza():
    def __init__(self,toppings):
        self.toppings = toppings
        
    @staticmethod
    def validate_topping(topping):
        if topping == "pineapple":
            raise ValueError("No pineapples! ")
        else:
            return True
ingredients = ["cheese","olives","broccoli"]
if all(Pizza.validate_topping(i) for i in ingredients):
    pizza =Pizza(ingredients)
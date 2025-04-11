# Spaghetti to test
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from cats.cat import Cat
import yaml

"""
The Engine will run a set of cats and let them play
with their toys.

TODO: Support Higher level configuration of the engine
i.e. concurrent cats running
"""
class Engine:
    def __init__(self):
        self.__cats    = [ ]
        self.__reports = { }
    """
    Add a set of cats, of a pre-defined configuration with pre-defined 
    data to be used by the cat.  Ideally used with a pre-defined set of 
    like tests to be ran.
    """
    def add_cats(self, cats : list[Cat], data : list[object]):
        if len(cats) != len(data):
            raise ValueError("cats and data must be of equal length, for cats without data, please add None")

        #TODO: Add support for "run attributes" i.e. cats that can be ran concurrently, 
        # or  a specific run order (i.e. This cat must be run first)   
        for i in range(len(cats)):
            self.add_cat(cats[i], data[i])
    
    """
    Add a singular cat to the engine.  For now, if a cats must only play in a 
    specific order, the cat must be added in a specific order and not using the
    add_cats() method
    """    
    def add_cat(self, cat : Cat, data : object):
        if not isinstance(cat, Cat):
            raise TypeError("cat must be of type Cat")
        
        if data is not None:
            cat.prepare(data)
        else:
            cat.prepare()
        
        self.__cats.append(cat)
    
    """
    Run all the cats in the engine
    """
    def run(self):
        for cat in self.__cats:
            cat.run()
            self.__reports[cat.name] = cat.report()
    
    def report(self):
        #TODO: Parse results for an overall Results summmary for passes / fails
        return yaml.dump(self.__reports)
    
if __name__ == "__main__":
    from _examples.Brutus import Brutus
    engine = Engine()
    engine.add_cat(Brutus("Brutus1"), None)
    engine.add_cat(Brutus("Brutus2"), None)
    engine.add_cats([Brutus("Brutus3"), Brutus()], [None, None])
    engine.run()
    print(engine.report())
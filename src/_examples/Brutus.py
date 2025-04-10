# Spaghetti to test
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from cats.cat import Cat, Toy
import subprocess

class Pinger(Toy):
    def __init__(self):
        super().__init__("Pinger")
    
    def run(self):
        self.write("I'm gonna ping google.com")
        self.test("pinging google.com", subprocess.run(["ping", "-c", "1", "google.com"]).returncode == 0)
        self.test("I'm also gonna test that 1 == 1!", 1 == 1)

class Brutus(Cat):
    def __init__(self):
        super().__init__("Brutus")
    
    def prepare(self):
        self.toybox["Pinger"] = Pinger()

if __name__ == "__main__":
    brutus = Brutus()
    brutus.prepare()
    brutus.run()
    report_str = brutus.report()
    print(report_str)
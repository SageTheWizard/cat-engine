from enum import Enum
from datetime import datetime

"""
Parent class that all CATs will inherit from
contains base functionality to load test cases
from a directory, execute test cases, and generate
a YAML report.

The Cat will act as a basic engine for the unit test
allowing, higher level complicated functionality / 
utility functions can be provided from children classes
or if desired, modules at a higher level runner layer 
_this runner layer is TBD and yet to be designed_
"""
class Cat():
    class Result(Enum):
        PASS       = 0
        FAIL       = 1
        INCONUSIVE = 2

    class ReportField(Enum):
        RESULT          = "Result"
        PASSES          = "Passes"
        FAILURES        = "Failures"
        INCONUSIVE      = "Inconclusive"
        CRASHES         = "Crashes"
        PASS_FAIL_RATIO = "Pass:Fail Ratio"
        LOGS            = "Logs"
    
    """ Init just initializes the default object members """
    def __init__(self, name : str = "Meow"):
        """ 
        The name of the cat, maybe name it something useful, or
        cute, I don't care 
        """
        self.name   = name
        
        """
        Dictionary report, will contain the results of the tests
        """
        self.__report = { }
        
        """
        Toybox all the tests will be stored here and ran sequentially
        """
        self.toybox = { }
         
    """
    Load up the cat's toybox with tests to run here
    """
    def prepare(self):
        pass
    
    """
    Let the cats play with their toys, loads the toy's report too the final
    report
    """
    def run(self):
        for toy in self.toybox:
            current_toy = self.toybox[toy]
            current_toy.run()
            result, log = current_toy.report()
            self.__report[current_toy.get_name()] = { 
                Toy.ReportField.RESULT: result, 
                Toy.ReportField.LOG: log 
            }
    
    def report(self):
        full_report = {
            Cat.ReportField.RESULT.value           : Cat.Result.PASS,
            Cat.ReportField.PASSES.value           : 0,
            Cat.ReportField.FAILURES.value         : 0,
            Cat.ReportField.INCONUSIVE.value       : 0,
            Cat.ReportField.CRASHES.value          : 0,
            Cat.ReportField.PASS_FAIL_RATIO.value  : 0.0,
            Cat.ReportField.LOGS.value             : []
        } 
        
        for report in self.__report:
            result = self.__report[report][Toy.ReportField.RESULT]
            if result == Toy.Result.PASS:
                full_report[Cat.ReportField.PASSES.value] += 1
            elif result == Toy.Result.FAIL:
                full_report[Cat.ReportField.FAILURES.value] += 1
            elif result == Toy.Result.INCONUSIVE:
                full_report[Cat.ReportField.INCONUSIVE.value] += 1
            elif result == Toy.Result.Toy_Broke:
                full_report[Cat.ReportField.CRASHES.value] += 1
            
            full_report[Cat.ReportField.LOGS.value].append({
                report : {
                    Cat.ReportField.RESULT.value : self.__report[report][Toy.ReportField.RESULT].value,
                    Cat.ReportField.LOGS.value :self.__report[report][Toy.ReportField.LOG]
                }
            })
        
        full_report[Cat.ReportField.PASS_FAIL_RATIO.value] = full_report[self.ReportField.PASSES.value] / (full_report[self.ReportField.PASSES.value] + full_report[self.ReportField.FAILURES.value])
        full_report[Cat.ReportField.RESULT.value] = Cat.Result.PASS.value if full_report[self.ReportField.FAILURES.value] == 0 else Cat.Result.FAIL.value
        
        return full_report

class Toy():
    class LogLine():
        def __init__(self, line : str):
            self.__line = line
            self.__time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        def __str__(self):
            return f"[{self.__time}] {self.__line}"
    
    class Result(Enum):
        PASS       = "Pass"
        FAIL       = "Fail"
        INCONUSIVE = "Inconclusive"
        TOY_BROKE  = "Crash"
    
    class ReportField(Enum):
        RESULT    = "Result"
        LOG       = "Log"
    
    def __init__(self, name : str):
        self.__name    = name
        self.__passing = True
        self.__report  = { 
            Toy.ReportField.RESULT :  Toy.Result.PASS,
            Toy.ReportField.LOG    :  ['\n']
        }
    
    def get_name(self):
        return self.__name

    def run(self):
        pass
    
    def report(self) -> tuple[Result, str]:
        # Generate the report line by line
        final_report = ""
        for line in self.__report[Toy.ReportField.LOG]:
            final_report += str(line) + "\n"
        return self.__report[Toy.ReportField.RESULT], final_report
        
    def write(self, line : str):
        self.__report[Toy.ReportField.LOG].append(Toy.LogLine(line))
    
    def test(self, line : str, to_assert : bool):
        if to_assert:
            self.write(f"{line} | PASS")
        else:
            self.write(f"{line} | FAIL")
            self.__passing = False
        
        if not self.__passing:
            self.__report[Toy.ReportField.RESULT] = Toy.Result.FAIL
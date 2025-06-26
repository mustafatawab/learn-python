from dataclasses import dataclass

@dataclass
class Runner:
    x : int = 10

    #classmethod can only be called directly with the class name which is Runner. THere will be no instance
    @classmethod
    def run(cls, input , * , arg1 , arg2) -> str:
        """ This is pydocs and documentation will be automatically generated """
        print(arg1)
        print(arg2)
        print(cls.x) # 10
        print(input) 
        return "Class Method"
    

run = Runner.run("Hello", arg1="Argument 1" , arg2="Argument 2")
print(run)
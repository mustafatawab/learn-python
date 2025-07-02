from crewai.flow.flow import Flow , start , listen , router
import random

class RouterFlow(Flow):
    @start()
    def greetings(self):
        print("Assalam O Alaikum")
        cities = ["karachi" , "islamabad" , "lahore" , "rawalpindi" , "swat"]
        

    @router(greetings)
    def select_city(self):
        cities = ["karachi" , "islamabad" , "lahore" , "rawalpindi" , "swat"]
        select_city = random.choice(cities)
        if select_city == "karachi":
            return "karachi"
        elif select_city == "islamabad":
            return "islamabad"
        elif select_city == "lahore":
            return "lahore"
        elif select_city == "rawalpindi":
            return "rawalpindi"
        elif select_city == "swat":
            return "swat"
        
        print(select_city)
        
    

    @listen("karachi")
    def krchi(self , city):
        message = f"write some fun fact about {city}"
        print(message)
        return message


    @listen("islamabad")
    def isb(self , city):
        message = f"write some fun fact about {city}"
        print(message)
        return message

    @listen("rawalpindi")
    def rwlpndi(self , city):
        message = f"write some fun fact about {city}"
        print(message)
        return message

    @listen('swat')
    def swt(self , city):
        message = f"write some fun fact about {city}"
        print(message)
        return message
    

    @listen('lahore')
    def lhr(self , city):
        message = f"write some fun fact about {city}"
        print(message)
        return message




def kickoff():
    obj = RouterFlow()
    obj.kickoff()


def plot():
    obj  = RouterFlow()
    obj.plot()
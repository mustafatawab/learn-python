from crewai.flow.flow import FLow , start , listen # type: ignore
from litellm import completion # type: ignore

API_KEY = "AIzaSyCMFGv2WjpKNNQul1XzFDaVGUNlYBLwv4U"
# this method is called prompt chaining. First output of the function will the the input of the second function, second output will be the third input of the third function and vice versa. 

class CityFunFact(FLow):

    @start()
    def generate_random_city(self):
        result  = completion(
            model='gemini-flash-2.0-flash',
            api_key=API_KEY,
            messages=[
                {"content" : "Retun any random city name", "role" : "user"}
            ]
        )
        city = result['choices'][0]['message']['content']
        print(city)
        return city


    @listen(generate_random_city)
    def generate_fun_fact(self , city : str):
        result  = completion(
            model='gemini-flash-2.0-flash',
            api_key=API_KEY,
            messages=[
                {"content" : f"Gemerate fun fact about {city}", "role" : "user"}
            ]
        )
        fun_fact = result['choices'][0]['message']['content'] 
        print(fun_fact)
        self.state['fun_fact'] = fun_fact
    

    @listen(generate_fun_fact)
    def save_fun_fact(self):
        with open("fun_fact.md" , "w") as file:
            file.write(self.state["fun_fact"])
            return self.state['fun_fact']



def kickoff():
    obj = CityFunFact()
    obj.kickoff()
    
from dataclasses import dataclass
from typing import ClassVar

@dataclass
class American:
  #static Variable because English use all the americans
  national_language : ClassVar[str] = 'English'  # the Type of the language is Generic

  #static varible because Humberger eat all americans
  national_food : ClassVar[str] = "Humberger"

  #static variable
  normal_temperature  :ClassVar[float] = 98.6

  #instance varibale because this is for individual
  name : str
  age : int
  weight : float
  liked_food : str  

  

  def eat(self):
    print(f"{self.name} is eating")

  def sleep(self):
    print(f"{self.name} is sleeping")

  def speak(self):
    print(f"{self.name} is speaking {American.national_language}")
  
  @staticmethod
  def countryLanguage():
    print(f"{American.national_language} is the language of America")


person = American("John" , 24 , 56.6)

person.eat()
person.sleep()
person.speak()
American.countryLanguage()

  
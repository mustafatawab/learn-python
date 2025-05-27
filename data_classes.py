from dataclasses import dataclass
from typing import ClassVar

@dataclass
class American:
  name : str
  age : int
  weight : float

  language : ClassVar[str] = 'English'  # the Type of the language is Generic

  def eat(self):
    print(f"{self.name} is eating")

  def sleep(self):
    print(f"{self.name} is sleeping")

  def speak(self):
    print(f"{self.name} is speaking {American.language}")
  
  @staticmethod
  def countryLanguage():
    print(f"{American.language} is the language of America")


person = American("John" , 24 , 56.6)

person.eat()
person.sleep()
person.speak()
American.countryLanguage()

  
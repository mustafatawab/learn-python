class Animal(object): #every class automatically extends the object class
    public : int
    _protected : int
    __private : int

    def __init__(self, public , _protected , __private):
        self.__private = __private
        self.public = public
        self._protected = _protected 
    
    



animal = Animal("Public" , "Protected" , "Private")
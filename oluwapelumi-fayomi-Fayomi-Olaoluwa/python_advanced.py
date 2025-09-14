# food=["rice","Fufu"]
# print(type(food))
#Classes and Object Oriented programming\

# class Car:
#     def __init__(self):
#         self.brand = "Toyota"
#         self.model = "Corolla"
#         self.color = "Black"
#         self.year  =  "2020"
# my_car= Car()
# print(my_car.color,my_car.year,my_car.brand)
#Whenever you have an init function you have to pass a parameter

class Person:
    def __init__(self,  name , age):
        self.name = name
        self.age = age
#String function controls what should be returned when the object is a string
    # def __str__(self):
    #     return f"My name is {self.name}\nI am {self.age}years old"
#Method is differentiated through the self parameter
    def welcome(self):
        dept = input("What department are you?:\n")
        print(f"My name is {self.name}\nI am {self.age} years old\nI am in {dept}class")
# p1 = Person("Adamu",17)
# p1.welcome()
#Parent class and Child class (child inherits functions and methods from parent)
class Student(Person):
    def __init__(self,name,age, gradyear):
#super function helps with adding to attributes inherited from parent class or else use pass
        super().__init__(name,age, )
        self.gradyear = gradyear
    def grad(self):
        print(f"I am graduating in {self.gradyear}")
x=Student("John",14,2025)
x.welcome()
x.grad()
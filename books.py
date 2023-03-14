import requests, csv,  io
from bs4 import BeautifulSoup
import pickle, string, random

# URl = 'https://www.passiton.com/inspirational-quotes'

# page  = requests.get(url=URl)
# soup = BeautifulSoup(page.content, 'html5lib')

class Student:
   
    def __init__(self, name:str, age:int):
      self.name = name,
      self.age  =age

    


stu = []


for i in range(3):
   name = string.ascii_lowercase[0:4]
   age = random.randint(18,30)
   student = Student(name=name, age=age)
   stu.append(student)

print(stu)


stread_data  = io.StringIO(stu)





# with open('quotes/quotes.html') as file:
#    result = pickle.loads(file)

#    print(file.read())

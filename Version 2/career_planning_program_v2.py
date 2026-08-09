#this is the second version of my program, which has more functions and features

#importing json and os modules
import json
import os

#creating class for careers
class Career:
       #initializing career attributes
       def __init__(self, name, sector, salary, description, education_required):
              self.name = name
              self.sector = sector
              self.salary = salary
              self.description = description
              self.education_required = education_required

       #function to display career information
       def display_info(self):
              print("================= Career Information ================")
              print(f"Career: {self.name}")
              print(f"Sector: {self.sector}")
              print(f"Salary: ${self.salary}")
              print(f"Description: {self.description}")
              print(f"Education Required: {self.education_required}")
              print("=====================================================\n\n")
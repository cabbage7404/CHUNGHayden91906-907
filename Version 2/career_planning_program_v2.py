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

#creating class for users and accounts
class User:
    def __init__(self, username, password, email, education, career_interest):
        self.username = username
        self.password = password
        self.email = email
        self.education = education
        self.career_interest = career_interest
        self.quiz_results = None

    def display_profile(self):
        print("================= User Profile =====================")
        print(f"Username: {self.username}")
        print(f"Email: {self.email}")
        print(f"Education: {self.education}")
        print(f"Career Interest: {self.career_interest}")
        if self.quiz_results:
            print(f"Quiz Results: {self.quiz_results}")
        else:
            print("Quiz Results: Not taken yet")
        print("=====================================================\n\n")

    def save_to_file(self):
        return = {
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "education": self.education,
            "career_interest": self.career_interest,
        }
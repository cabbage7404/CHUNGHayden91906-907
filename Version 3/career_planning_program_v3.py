#this is the third version of my program, which has more functions and features as well as built in GUI

import json
import os
import hashlib
import tkinter as tk
from tkinter import messagebox, ttk

def load_careers():
    with open("careers.json", "r") as file:
        data = json.load(file)
    return data

def load_questions():
    try:
        with open("quiz_questions.json", "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        messagebox.showerror("Error", "quiz_questions.json not found")
        return []
    except json.JSONDecodeError:
        messagebox.showerror("Error", "quiz_questions.json is corrupted")
        return []

careers_data = load_careers()
questions_data = load_questions()

class Career:
    #initialising career attributes
    def __init__(self, name, sector, salary, description, education_required):
            self.name = name #career name attribute
            self.sector = sector #career sector attribute
            self.salary = salary #career salary attribute
            self.description = description #career description attribute
            self.education_required = education_required #career education attribute

def load_careers():
    careers = []
    for item in careers_data:
        careers.append(Career(
            item["name"]
            item["sector"]
            item["salary"]
            item["description"]
            item["education_required"]
        ))
    return careers
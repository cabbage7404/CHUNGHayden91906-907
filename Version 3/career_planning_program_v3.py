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
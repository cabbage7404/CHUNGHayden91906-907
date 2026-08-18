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

class User:
    def __init__(self, username, email, password, education):
        self.username = username
        self.email = email
        self.password = password
        self.education = education
        self.quiz_results = None

    def save_to_file(self):
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "education": self.education,
            "quiz_results": self.quiz_results
        }

class Question:
    #initialising question attributes
    def __init__(self, question_text, options, sector_assign):
        self.question_text = question_text #question text attribute
        self.options = options #question options attribute
        self.sector_assign = sector_assign #sector assigned to question attribute

class Quiz:
    def __init__(self):
        self.questions = []
        for question in questions_data:
            self.questions.append(Question(
                question["question_text"],
                question["options"]
                question["sector_assign"]
            ))

    def get_current_question(self):
        return self.question[self.current_index]

    def submit_answer(self, answer_index):
        question = self.get_current_question()
        sector = question.sector_assign[answer_index]
        if sector in self.sector_scores:
            self.sector_scores[sector] += 1
        else:
            self.sector_scores[sector] = 1
        self.current_index += 1

    def is_finished(self):
        return self.current_index >= len(self.questions)

    def get_result(self):
        return max(self.sector_scores, key = self.sector_scores.get)

def load_user():
    try:
        if os.path.exists("user_info.json") == False:
            return {}
        else:
            with open("user_info.json", "r") as file:
                content = file.read()
                if content.strip() == "":
                    return {}
                return json.loads(content)
    except json.JSONDecodeError:
        messagebox.showerror("Error", "User data file is corrupted")
        return {}

def save_users(users_dict):
    try:
        with open("user_info.json", "w") as file:
                json.dump(users_dict, file, indent = 4)
    except IOError:
        messagebox.showerror("Error", "Could not save user data")

def hash_password(password):
    return haslib.sha256(password.encode())

def validate_username(username):
    if username.strip() == "":
        return False, "Username cannot be empty"
    elif username.replace(" ", "").isalpha() == False:
        return False, "Username must contain letters only"
    else:
        return True, ""

def validate_email(email):
    if "@" not in email or "." not in email:
        return False, "Invalid email address"
    else:
        return True, ""

MIN_PASSWORD_LEN = 8

def validate_password(password):
    if len(password) < MIN_PASSWORD_LEN:
        return False, "Password must be at least 8 characters"
    if any(char.isdigit() for char in password) == False:
        return False, "Password must contain at least one number"
    else:
        return True, ""

class Career_Planner_App:
    def __init__(self, root):
        self.root = root
        self.roo.title("Career Planner")
        self.root.geometry("900x700")
        self.users_dict = load_users()
        self.current_user = None
        self.all_careers = Career.load_all()
        self.quiz = None
        self.show_start_screen()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


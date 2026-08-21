#this is the third version of my program, which has more functions and features as well as built in GUI

import json
import os
import hashlib
import tkinter as tk
from tkinter import messagebox, ttk

def load_careers_from_file():
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

careers_data = load_careers_from_file()
questions_data = load_questions()

class Career:
    #initialising career attributes
    def __init__(self, name, sector, salary, description, education_required):
            self.name = name #career name attribute
            self.sector = sector #career sector attribute
            self.salary = salary #career salary attribute
            self.description = description #career description attribute
            self.education_required = education_required #career education attribute

    def load_all_careers():
        careers = []
        for item in careers_data:
            careers.append(Career(
                item["name"],
                item["sector"],
                item["salary"],
                item["description"],
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
                question["options"],
                question["sector_assign"]
            ))
        self.current_index = 0
        self.sector_score = {}
        

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

def load_users():
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
    return hashlib.sha256(password.encode()).hexdigest()

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
        self.root.title("Career Planner")
        self.root.geometry("900x700")
        self.users_dict = load_users()
        self.current_user = None
        self.all_careers = Career.load_all_careers()
        self.quiz = None
        self.show_start_screen()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_start_screen(self):
        self.clear_window()
        tk.Label(self.root, text = "Career Planner", font = ("Arial", 24)).pack(pady = 40)
        tk.Label(self.root, text = "Welcome! please choose from an option below.", font = ("Arial", 12)).pack(pady = 10)
        tk.Button(self.root, text = "Login", width = 20, command = self.show_login).pack(pady = 10)
        tk.Button(self.root, text = "Sign up", width = 20, command = self.show_signup).pack(pady = 10)
        tk.Button(self.root, text = "Exit", width = 20, command = self.root.quit).pack(pady = 10)

    def show_login(self):
        self.clear_window()
        tk.Label(self.root, text = "Login", font = ("Arial", 20)).pack(pady = 30)

        tk.Label(self.root, text = "Email: ").pack()
        email_entry = tk.Entry(self.root, width = 30)
        email_entry.pack(pady = 5)

        tk.Label(self.root, text = "Password: ").pack()
        password_entry = tk.Entry(self.root, width = 30, show = "*")
        password_entry.pack(pady = 5)

        def login_attempt():
            email = email_entry.get().strip()
            password = password_entry.get().strip()

            if email not in self.users_dict:
                messagebox.showerror("Login Failed", "No account found with that email")
                return
            else:
                None

            hashed = hash_password(password)
            if self.users_dict[email]["password"] != hashed:
                messagebox.showerror("Login Failed", "Incorrect password.")
                return
            else:
                None

            data = self.users_dict[email]
            self.current_user = User(data["username"], data["email"], data["password"], data["education"])
            self.current_user.quiz_results = data.get("quiz_results", None)
            self.show_main_menu()

        tk.Button(self.root, text = "Login", width = 20, command = login_attempt).pack(pady = 15)
        tk.Button(self.root, text = "Back", width = 20, command = self.show_start_screen).pack()

    def show_signup(self):
        self.clear_window()
        tk.Label(self.root, text = "Sign Up", font = ("Arial", 20)).pack(pady = 20)

        tk.Label(self.root, text = "Name: ").pack()
        username_entry = tk.Entry(self.root, width = 30)
        username_entry.pack(pady = 5)

        tk.Label(self.root, text = "Email: ").pack()
        email_entry = tk.Entry(self.root, width = 30)
        email_entry.pack(pady = 5)

        tk.Label(self.root, text = "Password: ").pack()
        password_entry = tk.Entry(self.root, width = 30, show = "*")
        password_entry.pack(pady = 5)

        tk.Label(self.root, text = "Confirm password: ").pack()
        confirm_password_entry = tk.Entry(self.root, width = 30, show = "*")
        confirm_password_entry.pack(pady = 5)

        tk.Label(self.root, text = "Highest Education Level: ").pack()
        education_entry = tk.Entry(self.root, width = 30)
        education_entry.pack(pady = 5)

        def signup_attempt():
            username = username_entry.get().strip()
            email = email_entry.get().strip()
            password = password_entry.get().strip()
            confirm = confirm_password_entry.get().strip()
            education = education_entry.get().strip()

            validation_value, message = validate_username(username)
            if validation_value == False:
                messagebox.showerror("Invalid Input", message)
                return
            else:
                None

            validation_value, message = validate_email(email)
            if validation_value == False:
                messagebox.showerror("Invalid Input", message)
                return
            else:
                None

            if email in self.users_dict:
                messagebox.showerror("Invalid Input", "An account with this email already exists.")
                return

            validation_value, message = validate_password(password)
            if validation_value == False:
                messagebox.showerror("Invalid Input", message)
                return
            else:
                None

            if password != confirm:
                messagebox.showerror("Invalid Input", "Passwords do not match.")
                return
            else:
                None

            if education.strip() == "":
                messagebox.showerror("Invalid Input", "Education field cannot be empty.")
                return

            hashed = hash_password(password)
            new_user = User(username, email, hashed, education)
            self.users_dict[email] = new_user.save_to_file()
            save_users(self.users_dict)

            self.current_user = new_user
            messagebox.showinfo("Success!", f"Account created! Welcome, {username}!")
            self.show_main_menu()

        tk.Button(self.root, text = "Create Account", width = 20, command = signup_attempt).pack(pady = 15)
        tk.Button(self.root, text = "Back", width = 20, command = self.show_start_screen).pack()

    def show_main_menu(self):
        self.clear_window()
        tk.Label(self.root, text = f"Welcome, {self.current_user.username}!", font = ("Arial", 20)).pack(pady = 20)
        tk.Label(self.root, text = "What would you like to do?", font = ("Arial", 12)).pack(pady = 5)
        tk.Button(self.root, text = "Browse Careers", width = 25, command = self.show_career_browser).pack(pady = 10)
        tk.Button(self.root, text = "Take Career Quiz", width = 25, command = self.start_quiz).pack(pady = 10)
        tk.Button(self.root, text = "View my profile", width = 25, command = self.show_profile).pack(pady = 10)
        tk.Button(self.root, text = "Logout", width = 25, command = self.show_start_screen).pack(pady = 10)

    def show_career_browser(self):
        self.clear_window()
        tk.Label(self.root, text = "Browse Careers", font = ("Arial", 20)).pack(pady = 15)

        filter_frame = tk.Frame(self.root)
        filter_frame.pack(pady = 5)

        tk.Label(filter_frame, text = "Search: ").grid(row = 0, column = 0, padx = 5)
        search_variable = tk.StringVar()
        search_entry = tk.Entry(filter_frame, textvariable = search_variable, width = 20)
        search_entry.grid(row = 0, column = 1, padx = 5)

        tk.Label(filter_frame, text = "Sector: ").grid(row = 0, column = 2, padx = 5)
        sectors = ["All"] + sorted(set(c["sector"] for c in careers_data))
        sector_variable = tk.StringVar(value = "All")
        sector_menu = ttk.Combobox(filter_frame, textvariable = sector_variable, values = sectors, width = 15, state = "readonly")
        sector_menu.grid(row = 0, column = 3, padx = 5)

        tk.Label(filter_frame, text = "Sort by: ").grid(row = 0, column = 4, padx = 5)
        sort_variable = tk.StringVar(value = "Name (A-Z)")
        sort_menu = ttk.Combobox(filter_frame, textvariable = sort_variable, 
                                 values = ["Name (A-Z)", 
                                           "Name (Z-A)", 
                                           "Salary (High-Low)",
                                           "Salary (Low-High)"],
                                           width = 18, state = "readonly")
        sort_menu.grid(row = 0, column = 5, padx = 5)

        tk.Label(self.root, text = "Browse by Sector: ", font = ("Arial", 11)).pack(pady = (10, 0))
        grid_frame = tk.Frame(self.root)
        grid_frame.pack(pady = 5)

        unique_sectors = sorted(set(c["sector"] for c in careers_data))
        for i, sector in enumerate(unique_sectors):
            button = tk.Button(grid_frame, text = sector, width = 15, command = lambda s = sector: self.filter_by_sector(s, sector_variable, search_variable, sort_variable, listbox))
            button.grid(row = i // 4, column = i % 4, padx = 5, pady = 5)

        tk.Label(self.root, text = "Results: ", font = ("Arial", 11)).pack()
        listbox_frame = tk.Frame(self.root)
        listbox_frame.pack(fill = tk.BOTH, expand = True, padx = 20, pady = 5)

        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side = tk.RIGHT, fill = tk.Y)
        listbox = tk.Listbox(listbox_frame, yscrollcommand = scrollbar.set, font = ("Arial", 11), height = 8)
        listbox.pack(fill = tk.BOTH, expand = True)
        scrollbar.config(command = listbox.yview)

        self.filtered_careers = self.all_careers[:]

        def refresh_list(*args):
            query = search_variable.get().lower()
            sector = sector_variable.get()
            sort = sort_variable.get()

            results = []
            for career in self.all_careers:
                if query and query not in career.name.lower():
                    continue
                if sector != "All" and career.sector != sector:
                    continue
                results.append(career)

            if sort == "Name (A-Z)":
                results.sort(key = lambda career: career.name)
            elif sort == "Name (Z-A)":
                results.sort(key = lambda career: career.name, reverse = True)
            elif sort == "Salary (High-Low)":
                results.sort(key = lambda career: career.name, reverse = True)
            elif sort == "Salary (Low-High)":
                results.sort(key = lambda career: career.name)

            listbox.delete(0, tk.END)
            self.filtered_careers = results
            for career in results:
                listbox.insert(tk.END, f"{career.name}   |   {career.sector}   |   ${career.salary:,}/year")

            if results == False:
                listbox.insert(tk.END, "No careers found matching your search")

        search_variable.trace_add("write", refresh_list)
        sector_variable.trace_add("write", refresh_list)
        sort_variable.trace_add("write", refresh_list)
        refresh_list()

        def on_select(event):
            selection = listbox.curselection()
            if not selection:
                return
            index = selection[0]
            if index < len(self.filtered_careers):
                self.show_career_details(self.filtered_careers[index])

        listbox.bind("<<ListboxSelect>>", on_select)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady = 10)
        tk.Button(button_frame, text = "Home", width = 15, command = self.show_main_menu).pack(side = tk.LEFT, padx = 10)

    def filter_by_sector(self, sector, sector_variable, search_variable, sort_variable, listbox):
        sector_variable.set(sector)

    def show_career_details(self, career):
        self.clear_window()
        tk.Label(self.root, text = career.name, font = ("Arial", 22)).pack(pady = 20)

        detail_frame = tk.Frame(self.root)
        detail_frame.pack(padx = 40, pady = 10, anchor = "w")

        details = [
            ("Sector", career.sector),
            ("Average Salary", f"${career.salary:,} per year"),
            ("Education required", career.education_required),
            ("Description", career.description)
        ]

        for label, value in details:
            row = tk.Frame(detail_frame)
            row.pack(anchor = "w", pady = 4)
            tk.Label(row, text = f"{label}:", font = ("Arial", 11, "bold"), width = 20, anchor = "w").pack(side = tk.LEFT)
            tk.Label(row, text = value, font = ("Arial", 11), wraplength = 500, justify = "left").pack(side = tk.LEFT)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady = 20)
        tk.Button(button_frame, text = "Back to Careers", width = 18, command = self.show_career_browser).pack(side = tk.LEFT, padx = 10)
        tk.Button(button_frame, text = "Home", width = 18, command = self.show_main_menu).pack(side = tk.LEFT, padx = 10)

    def start_quiz(self):
        self.quiz = Quiz()
        if self.quiz.questions == False:
            messagebox.showerror("Error", "No quiz questions found.")
            return
        self.show_quiz_questions()

    def show_quiz_questions(self):
        self.clear_window()
        if self.quiz is None:
            messagebox.showerror("Error", "Quiz not initialised.")
            self.show_main_menu()
            return
        else:
            None

        if self.quiz.is_finished():
            self.show_quiz_results
            return
        else:
            None

        question = self.quiz.get_current_question()
        total = len(self.quiz.questions)
        current = self.quiz.current_index + 1

        tk.Label(self.root, text = f"Question {current} of {total}", font = ("Arial", 13)).pack(pady = 15)
        tk.Label(self.root, text = question.question_text, font = ("Arial", 13), wraplength = 700).pack(pady = 10)

        selected = tk.IntVar(value =- 1)

        for i, option in enumerate(question.options):
            tk.Radiobutton(self.root, text = option, variable = selected, value = i, font = ("Arial", 11)).pack(anchor = "w", padx = 80, pady = 4)

        def submit():
            if selected.get() == -1:
                messagebox.showwarning("No answer", "Please select an answer before continuing.")
                return
            try:
                self.quiz.submit_answer(selected.get())
                self.show_quiz_question()
            except KeyError:
                messagebox.showerror("Error", "Quiz data error. Please restart the quiz.")
                self.show_main_menu

            tk.Button(self.root, text = "Next", width = 20, command = submit).pack(pady = 20)
            tk.Button(self.root, text = "Cancel Quiz", width = 20, command = self.show_main_menu).pack()

    def show_quiz_results(self):
        self.clear_window()
        result = self.quiz.get_result()

        tk.Label(self.root, text = "Quiz Complete!", font = ("Arial, 22")).pack(pady = 20)
        tk.Label(self.root, text = "Based on your answerrs, your recommended sector is: ", font = ("Arial", 13)).pack(pady = 5)
        tk.Label(self.root, text = result, font = ("Arial", 18, "bold")).pack(pady = 10)

        tk.Label(self.root, text = "Careers in this sector: ", font = ("Arial", 12)).pack(pady = 5)
        matches = [career for career in self.all_careers if career.sector == result]
        for career in matches:
            tk.Label(self.root, text = f"- {career.name}", font = ("Arial", 11)).pack()

        self.current_user.quiz_results = result

        tk.Button(self.root, text = "Home", width = 20, command = self.show_main_menu).pack(pady = 20)

    def show_profile(self):
        self.clear_window()
        tk.Label(self.root, text = "My Profile", font = ("Arial", 20)).pakc(pady = 20)

        detail_frame = tk.Frame(self.root)
        detail_frame.pack(padx = 40, pady = 10, anchor = "w")

        details = [
            ("Name", self.curent_user.name),
            ("Email", self.current_user.email),
            ("Education", self.current_user.education),
            ("Quiz results", self.current_user.quiz_reults 
             if self.current_user.quiz_results
             else "Not yet taken")
        ]

        for label, value in details:
            row = tk.Frame(detail_frame)
            row.pack(anchor = "w", pady = 6)
            tk.Label(row, text = f"{label}:", font = ("Arial", 11, "bold"), width = 15, anchor = "w").pack(side = tk.LEFT)
            tk.Label(row, text = value, font = ("Arial", 11)).pack(side = tk.LEFT)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady = 20)
        tk.Button(button_frame, text = "Edit Profile", width = 18, command = self.show_edit_profile).pack(side = tk.LEFT, padx = 10)
        tk.Button(button_frame, text = "Retake Quiz", width = 18, command = self.start_quiz).pack(side = tk.LEFT, padx = 10)
        tk.Button(button_frame, text = "Home", width = 18, command = self.show_main_menu).pack(side = tk.LEFT, padx = 10)

    def show_edit_profile(self):
        self.clear_window()
        tk.Label(self.root, text = "Edit Profile", font = ("Arial", 20)).pack(pady = 20)

        tk.Label(self.root, text = "Name").pack()
        username_entry = tk.Entry(self.root, width = 30)
        username_entry.insert(0, self.current_user.username)
        username_entry.pack(pady = 5)

        tk.Label(self.root, text = "Education: ").pack()
        education_entry = tk.Entry(self.root, width = 30)
        education_entry.insert(0, self.current_user.education)
        education_entry.pack(pady = 5)

        def save_changes():
            new_username = username_entry.get().strip()
            new_education = education_entry.get().strip()

            valid, message = validate_username(new_username)
            if not valid:
                messagebox.showerror("Invalid Input", message)
                return
            else:
                None

            if new_education == "":
                messagebox.showerror("Invalid Input", "Education cannot be empty.")
                return
            else:
                None

            self.current_user.username = new_username
            self.current_user.education = new_education

            self.users_dict[self.current_user.username] = self.current_user.save_to_file()
            save_users(self.users_dict)

            messagebox.showinfo("Success", "Profile updated successfully!")
            self.show_profile()

        tk.Button(self.root, text = "Save Changes", width = 20, command = save_changes).pack(pady = 15)
        tk.Button(self.root, text = "Cancel", width = 20, command = self.show_profile).pack()

root = tk.Tk()
app = Career_Planner_App(root)
root.mainloop()
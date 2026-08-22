#this is the third version of my program, which has more functions and features as well as built in GUI

import json
import os
import hashlib
import tkinter as tk
from tkinter import messagebox, ttk

#function to load careers from external file
def load_careers_from_file():
    with open("careers.json", "r") as file: #reads external careers file
        data = json.load(file)
    return data #returns data to program

#function to load questions from external file
def load_questions():
    try:
        with open("quiz_questions.json", "r") as file: #reads external questions file
            data = json.load(file) #assigns data to variable
        return data #returns file contents to program
    except FileNotFoundError: #branch for if there is no file
        messagebox.showerror("Error", "quiz_questions.json not found") #displays error message
        return [] #returns empty list
    except json.JSONDecodeError: #branch for if file is corrupted
        messagebox.showerror("Error", "quiz_questions.json is corrupted") #displays error message
        return [] #returns empty list

careers_data = load_careers_from_file() #assigns career function to variable
questions_data = load_questions() #assigns question function to variable

#creating class for careers
class Career:
    #initialising career attributes
    def __init__(self, name, sector, salary, description, education_required):
            self.name = name #career name attribute
            self.sector = sector #career sector attribute
            self.salary = salary #career salary attribute
            self.description = description #career description attribute
            self.education_required = education_required #career education attribute

    #method to load career objects from variable after file has been read
    def load_all_careers():
        careers = [] #creates emtpy list
        for item in careers_data: #iterates over how many careers there are
            careers.append(Career( #creates career items from data
                item["name"],
                item["sector"],
                item["salary"],
                item["description"],
                item["education_required"]
            ))
        return careers #returns career list to program

#creating class for user and accounts
class User:
    #initialising user attributes
    def __init__(self, username, email, password, education):
        self.username = username #user name attribute
        self.email = email #user email attribute
        self.password = password #user password attribute
        self.education = education #user education attribute
        self.quiz_results = None #user quiz results attribute

    #method to return user data as a dictionary to be saved in other functions
    def save_to_file(self):
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "education": self.education,
            "quiz_results": self.quiz_results
        }

#creating class for questions
class Question:
    #initialising question attributes
    def __init__(self, question_text, options, sector_assign):
        self.question_text = question_text #question text attribute
        self.options = options #question options attribute
        self.sector_assign = sector_assign #sector assigned to question attribute

#creating class for quiz
class Quiz:
    #initialising quiz attributes
    def __init__(self):
        self.questions = [] #creates empty list assigned to self.questions
        for question in questions_data: #iterates over number of questions in external file
            self.questions.append(Question( #creates question items using data
                question["question_text"],
                question["options"],
                question["sector_assign"]
            ))
        self.current_index = 0 #sets index score to 0
        self.sector_scores = {} #creates empty dictionary assigned to self.sector_scores
        
    #method to get the correct question for the user
    def get_current_question(self):
        return self.questions[self.current_index] #returns the question according to the index

    #method to submit answers
    def submit_answer(self, answer_index):
        question = self.get_current_question() #calls function and assigns returned value to variable
        sector = question.sector_assign[str(answer_index)] #gets the sector that corresponds to users answer
        if sector in self.sector_scores: #checks if sector is already in dictionary
            self.sector_scores[sector] += 1 #adds one to score
        else: #if sector isn't in dictionary yet
            self.sector_scores[sector] = 1 #set score to one
        self.current_index += 1 #adds one to current index so that quiz can progress

    #method to check if quiz has finished
    def is_finished(self):
        return self.current_index >= len(self.questions) #returns a true or false value

    #method to get quiz results
    def get_result(self):
        return max(self.sector_scores, key = self.sector_scores.get) #checks for the highest score sector and returns it

#function for loading users from external file
def load_users():
    try: #try block
        if os.path.exists("user_info.json") == False: #if file does not exist
            return {} #returns empty dictionary
        else: #if file does exist
            with open("user_info.json", "r") as file: #reads external file
                content = file.read() #assigns data to variable
                if content.strip() == "": #checks if file is completely empty
                    return {} #returns empty dictionary
                return json.loads(content) #returns file data to program
    except json.JSONDecodeError: #except block if file is corrupted
        messagebox.showerror("Error", "User data file is corrupted")
        return {} #returns empty dictionary

#function to save users to external file
def save_users(users_dict):
    try: #try block
        with open("user_info.json", "w") as file: #opens external file with write
                json.dump(users_dict, file, indent = 4) #writes data from user dictionary to file with indents
    except IOError: #except error
        messagebox.showerror("Error", "Could not save user data")

#function to hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest() #uses hashlib sha256 to encrypt password and then converts it to useable string

#function to validate username when sign-up is called
def validate_username(username):
    if username.strip() == "": #if username is emtpy
        return False, "Username cannot be empty" #returns false value with error message
    elif username.replace(" ", "").isalpha() == False: #if username has numbers
        return False, "Username must contain letters only" #returns false value with error message
    else: #if usename is fine
        return True, "" #returns true value with no message

#function to validate email when sign-up is called
def validate_email(email):
    if "@" not in email or "." not in email: #if email is not in correct format
        return False, "Invalid email address" #returns false value with error message
    else: #if email is fine
        return True, "" #returns true value with no message

#sets minimum password length to 8 characters
MIN_PASSWORD_LEN = 8

#function to validate password when sign-up is called
def validate_password(password):
    if len(password) < MIN_PASSWORD_LEN: #if password is less than minimum 
        return False, "Password must be at least 8 characters" #returns false value with error message
    if any(char.isdigit() for char in password) == False: #if password has no digits
        return False, "Password must contain at least one number" #returns false value with error message
    else: #if password is fine
        return True, ""#returns true value with no message

#creating main class for the program
class Career_Planner_App:
    #initialising attributes
    def __init__(self, root):
        self.root = root #creates main window of program
        self.root.title("Career Planner") #sets title
        self.root.geometry("900x700") #sets size
        self.users_dict = load_users() #assigns returned values from function to self.users_dict
        self.current_user = None #leaves self.current_user empty
        self.all_careers = Career.load_all_careers() #assigns returned values from function to self.all_careers
        self.quiz = None #leaves self.quiz empty
        self.show_start_screen() #calls function to display start screen

    #method to remove all widgets in the window
    def clear_window(self):
        for widget in self.root.winfo_children(): #iterates over number of widgets there are
            widget.destroy() #destroys widgets

    #method for displaying start screen
    def show_start_screen(self):
        self.clear_window() #calls function to clear window
        tk.Label(self.root, text = "Career Planner", font = ("Arial", 24)).pack(pady = 40) #creates labels and buttons with corresponding functions
        tk.Label(self.root, text = "Welcome! please choose from an option below.", font = ("Arial", 12)).pack(pady = 10)
        tk.Button(self.root, text = "Login", width = 20, command = self.show_login).pack(pady = 10)
        tk.Button(self.root, text = "Sign up", width = 20, command = self.show_signup).pack(pady = 10)
        tk.Button(self.root, text = "Exit", width = 20, command = self.root.quit).pack(pady = 10)

    #method to show login screen
    def show_login(self):
        self.clear_window() #calls function to clear window
        tk.Label(self.root, text = "Login", font = ("Arial", 20)).pack(pady = 30) #creates title label

        #creates label and entry box for users to enter details
        tk.Label(self.root, text = "Email: ").pack()
        email_entry = tk.Entry(self.root, width = 30)
        email_entry.pack(pady = 5)
        tk.Label(self.root, text = "Password: ").pack()
        password_entry = tk.Entry(self.root, width = 30, show = "*")
        password_entry.pack(pady = 5)

        #nested function to execute login
        def login_attempt():
            email = email_entry.get().strip() #takes user input and assigns it a variable
            password = password_entry.get().strip() #takes user input and assigns it a variable

            if email not in self.users_dict: #if user's email is not already in database
                messagebox.showerror("Login Failed", "No account found with that email")
                return
            else: #if user email is in database
                None

            hashed = hash_password(password) #calls the hash password function for string
            if self.users_dict[email]["password"] != hashed: #if password doesn't match database
                messagebox.showerror("Login Failed", "Incorrect password.")
                return
            else: #if password does match
                None

            #updates current user details and continues to main menu
            data = self.users_dict[email]
            self.current_user = User(data["username"], data["email"], data["password"], data["education"])
            self.current_user.quiz_results = data.get("quiz_results", None)
            self.show_main_menu()

        #creates buttons widgets to login or go back
        tk.Button(self.root, text = "Login", width = 20, command = login_attempt).pack(pady = 15)
        tk.Button(self.root, text = "Back", width = 20, command = self.show_start_screen).pack()

    #method to show sign-up window
    def show_signup(self):
        self.clear_window() #calls function to clear window
        tk.Label(self.root, text = "Sign Up", font = ("Arial", 20)).pack(pady = 20) #creates title label

        #creates label and input widgets for all required user details
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

        #nested function to execute sign-up
        def signup_attempt():
            #gets all user inputs and assigns them to variables
            username = username_entry.get().strip()
            email = email_entry.get().strip()
            password = password_entry.get().strip()
            confirm = confirm_password_entry.get().strip()
            education = education_entry.get().strip()

            #calls the validation function to check if user inputs are valid
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

            if email in self.users_dict: #checks if account with entered email already exists
                messagebox.showerror("Invalid Input", "An account with this email already exists.")
                return

            validation_value, message = validate_password(password)
            if validation_value == False:
                messagebox.showerror("Invalid Input", message)
                return
            else:
                None

            if password != confirm: #checks if password and password confirmation match
                messagebox.showerror("Invalid Input", "Passwords do not match.")
                return
            else:
                None

            if education.strip() == "":
                messagebox.showerror("Invalid Input", "Education field cannot be empty.")
                return

            #saves new user account to external file and local dictionary
            hashed = hash_password(password)
            new_user = User(username, email, hashed, education)
            self.users_dict[email] = new_user.save_to_file()
            save_users(self.users_dict)

            #updates current user status and prints welcome message to main menu
            self.current_user = new_user
            messagebox.showinfo("Success!", f"Account created! Welcome, {username}!")
            self.show_main_menu()

        #creats button widgets to create account of go back
        tk.Button(self.root, text = "Create Account", width = 20, command = signup_attempt).pack(pady = 15)
        tk.Button(self.root, text = "Back", width = 20, command = self.show_start_screen).pack()

    #method to show the main menu
    def show_main_menu(self):
        self.clear_window() #calls function to wipe window
        tk.Label(self.root, text = f"Welcome, {self.current_user.username}!", font = ("Arial", 20)).pack(pady = 20) #creates label and button widgets for user to interact with
        tk.Label(self.root, text = "What would you like to do?", font = ("Arial", 12)).pack(pady = 5)
        tk.Button(self.root, text = "Browse Careers", width = 25, command = self.show_career_browser).pack(pady = 10)
        tk.Button(self.root, text = "Take Career Quiz", width = 25, command = self.start_quiz).pack(pady = 10)
        tk.Button(self.root, text = "View my profile", width = 25, command = self.show_profile).pack(pady = 10)
        tk.Button(self.root, text = "Logout", width = 25, command = self.show_start_screen).pack(pady = 10)

    #method to show the career browser
    def show_career_browser(self):
        self.clear_window() #calls function to wipe window
        tk.Label(self.root, text = "Browse Careers", font = ("Arial", 20)).pack(pady = 15) #creates title label

        #creates frame widget
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(pady = 5)

        #creates search bar widget for users to use
        tk.Label(filter_frame, text = "Search: ").grid(row = 0, column = 0, padx = 5)
        search_variable = tk.StringVar()
        search_entry = tk.Entry(filter_frame, textvariable = search_variable, width = 20)
        search_entry.grid(row = 0, column = 1, padx = 5)

        #creates drop down box for users to select sector for filters
        tk.Label(filter_frame, text = "Sector: ").grid(row = 0, column = 2, padx = 5)
        sectors = ["All"] + sorted(set(c["sector"] for c in careers_data))
        sector_variable = tk.StringVar(value = "All")
        sector_menu = ttk.Combobox(filter_frame, textvariable = sector_variable, values = sectors, width = 15, state = "readonly")
        sector_menu.grid(row = 0, column = 3, padx = 5)

        #creates drop down box for users to select differnt filters
        tk.Label(filter_frame, text = "Sort by: ").grid(row = 0, column = 4, padx = 5)
        sort_variable = tk.StringVar(value = "Name (A-Z)")
        sort_menu = ttk.Combobox(filter_frame, textvariable = sort_variable, 
                                 values = ["Name (A-Z)", 
                                           "Name (Z-A)", 
                                           "Salary (High-Low)",
                                           "Salary (Low-High)"],
                                           width = 18, state = "readonly")
        sort_menu.grid(row = 0, column = 5, padx = 5)

        #creates label and frame for sector buttons to go into
        tk.Label(self.root, text = "Browse by Sector: ", font = ("Arial", 11)).pack(pady = (10, 0))
        grid_frame = tk.Frame(self.root)
        grid_frame.pack(pady = 5)

        #iterates over number of total sectors and organises them into a grid as buttons
        unique_sectors = sorted(set(c["sector"] for c in careers_data))
        for i, sector in enumerate(unique_sectors):
            button = tk.Button(grid_frame, text = sector, width = 15, command = lambda s = sector: self.filter_by_sector(s, sector_variable, search_variable, sort_variable, listbox))
            button.grid(row = i // 4, column = i % 4, padx = 5, pady = 5)

        #creates a list widget to display all the careers available as a list
        tk.Label(self.root, text = "Results: ", font = ("Arial", 11)).pack()
        listbox_frame = tk.Frame(self.root)
        listbox_frame.pack(fill = tk.BOTH, expand = True, padx = 20, pady = 5)

        #creates scrollbar widget to scroll through career list
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side = tk.RIGHT, fill = tk.Y)
        listbox = tk.Listbox(listbox_frame, yscrollcommand = scrollbar.set, font = ("Arial", 11), height = 8)
        listbox.pack(fill = tk.BOTH, expand = True)
        scrollbar.config(command = listbox.yview)

        self.filtered_careers = self.all_careers[:] #creates a snapshot of the list of careers

        #nested function to refresh list of careers
        def refresh_list(*args): #*arg allows function to take any number of arguments
            #assigns user inputs to variables
            query = search_variable.get().lower()
            sector = sector_variable.get()
            sort = sort_variable.get()

            results = [] #creates empty list 
            #iterates over number of careers available
            for career in self.all_careers:
                if query and query not in career.name.lower():
                    continue
                if sector != "All" and career.sector != sector:
                    continue
                results.append(career)

            #carries out filters depending on what the user selected
            if sort == "Name (A-Z)":
                results.sort(key = lambda career: career.name)
            elif sort == "Name (Z-A)":
                results.sort(key = lambda career: career.name, reverse = True)
            elif sort == "Salary (High-Low)":
                results.sort(key = lambda career: career.salary, reverse = True)
            elif sort == "Salary (Low-High)":
                results.sort(key = lambda career: career.salary)

            #clears list box widget and adds filtered careers in
            listbox.delete(0, tk.END)
            self.filtered_careers = results
            for career in results:
                listbox.insert(tk.END, f"{career.name}   |   {career.sector}   |   ${career.salary:,}/year")

            #checks if users search doesn't match any careers
            if not results:
                listbox.insert(tk.END, "No careers found matching your search")

        #trace constantly checks variables for changes and as soon as changes are detected list will be refreshed
        search_variable.trace_add("write", refresh_list)
        sector_variable.trace_add("write", refresh_list)
        sort_variable.trace_add("write", refresh_list)
        refresh_list()

        #nested function to call when career is clicked
        def on_select(event):
            selection = listbox.curselection()
            if not selection:
                return
            index = selection[0]
            if index < len(self.filtered_careers):
                self.show_career_details(self.filtered_careers[index])

        listbox.bind("<<ListboxSelect>>", on_select) #calls function when item in list box is selected

        #creates button to return home
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady = 10)
        tk.Button(button_frame, text = "Home", width = 15, command = self.show_main_menu).pack(side = tk.LEFT, padx = 10)

    #method to filter careers by sector
    def filter_by_sector(self, sector, sector_variable, search_variable, sort_variable, listbox):
        sector_variable.set(sector)

    #method to display career information
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

    #method to start quiz
    def start_quiz(self):
        self.quiz = Quiz()
        if not self.quiz.questions: #if quiz is empty
            messagebox.showerror("Error", "No quiz questions found.")
            return
        self.show_quiz_questions() #calls function to display quiz

    #method to display quiz questions 
    def show_quiz_questions(self):
        self.clear_window()
        if self.quiz is None:
            messagebox.showerror("Error", "Quiz not initialised.")
            self.show_main_menu()
            return
        else:
            None

        if self.quiz.is_finished():
            self.show_quiz_results()
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

        #nested function to submit answers for quiz
        def submit():
            if selected.get() == -1:
                messagebox.showwarning("No answer", "Please select an answer before continuing.")
                return
            try:
                self.quiz.submit_answer(selected.get())
                self.show_quiz_questions()
            except KeyError:
                messagebox.showerror("Error", "Quiz data error. Please restart the quiz.")
                self.show_main_menu()

        tk.Button(self.root, text = "Next", width = 20, command = submit).pack(pady = 20)
        tk.Button(self.root, text = "Cancel Quiz", width = 20, command = self.show_main_menu).pack()

    #method to display results of quiz
    def show_quiz_results(self):
        self.clear_window()
        result = self.quiz.get_result()

        tk.Label(self.root, text = "Quiz Complete!", font = ("Arial", 22)).pack(pady = 20)
        tk.Label(self.root, text = "Based on your answers, your recommended sector is: ", font = ("Arial", 13)).pack(pady = 5)
        tk.Label(self.root, text = result, font = ("Arial", 18, "bold")).pack(pady = 10)

        tk.Label(self.root, text = "Careers in this sector: ", font = ("Arial", 12)).pack(pady = 5)
        matches = [career for career in self.all_careers if career.sector == result]
        for career in matches:
            tk.Label(self.root, text = f"- {career.name}", font = ("Arial", 11)).pack()

        self.current_user.quiz_results = result
        self.users_dict[self.current_user.email]["quiz_results"]= result
        save_users(self.users_dict)

        tk.Button(self.root, text = "Home", width = 20, command = self.show_main_menu).pack(pady = 20)

    #method to display user profile
    def show_profile(self):
        self.clear_window()
        tk.Label(self.root, text = "My Profile", font = ("Arial", 20)).pack(pady = 20)

        detail_frame = tk.Frame(self.root)
        detail_frame.pack(padx = 40, pady = 10, anchor = "w")

        details = [
            ("Name", self.current_user.username),
            ("Email", self.current_user.email),
            ("Education", self.current_user.education),
            ("Quiz results", self.current_user.quiz_results 
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

    #method to display edit profile page
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

        #nested function to save changes from user inputs
        def save_changes():
            new_username = username_entry.get().strip()
            new_education = education_entry.get().strip()

            #validation for username and education level
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

            #updates current user status
            self.current_user.username = new_username
            self.current_user.education = new_education

            #updates user dictionary and external file
            self.users_dict[self.current_user.username] = self.current_user.save_to_file()
            save_users(self.users_dict)

            #displays message and new profile
            messagebox.showinfo("Success", "Profile updated successfully!")
            self.show_profile()

        #creates buttons to save changes or cancel process
        tk.Button(self.root, text = "Save Changes", width = 20, command = save_changes).pack(pady = 15)
        tk.Button(self.root, text = "Cancel", width = 20, command = self.show_profile).pack()

#starts the program
root = tk.Tk()
app = Career_Planner_App(root)
root.mainloop()
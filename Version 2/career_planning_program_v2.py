#this is the second version of my program, which has more functions and features

#importing json and os modules
import json
import os

#creating class for careers
class Career:
    #initialising career attributes
    def __init__(self, name, sector, salary, description, education_required):
            self.name = name #career name attribute
            self.sector = sector #career sector attribute
            self.salary = salary #career salary attribute
            self.description = description #career description attribute
            self.education_required = education_required #career education attribute

    #method to display career information
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
    #initialising user attributes
    def __init__(self, username, email, password, education):
        self.username = username #user name attribute
        self.email = email #user email attribute
        self.password = password #user password attribute
        self.education = education #user education attribute
        self.quiz_results = None #user quiz results attribute

    #method to display user profile
    def display_profile(self):
        print("================= User Profile =====================")
        print(f"Username: {self.username}")
        print(f"Email: {self.email}")
        print(f"Education: {self.education}")
        if self.quiz_results: #checks if user has completed quiz
            print(f"Quiz Results: {self.quiz_results}")
        else: #if user hasn't completed quiz
            print("Quiz Results: Not taken yet")
        print("=====================================================\n\n")

    #method to return user data as a dictionary to be saved in another function
    def save_to_file(self):
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "education": self.education,
            "quiz_results": self.quiz_results
        }

#creating class for quiz and questions
class Question:
    #initialising question attributes
    def __init__(self, question_text, options, sector_assign):
        self.question_text = question_text #question text attribute
        self.options = options #question options attribute
        self.sector_assign = sector_assign #sector assigned to question attribute

    #method to print questions for user one by one
    def display_question(self):
        print(f"Question: {self.question_text}") #prints question
        for i, option in enumerate(self.options, 1): #for loop iterates over how many questions there are and assigns each option a number starting from 1
            print(f"{i}. {option}") #prints numbered options
        while True: #while loop to validate user inputs
             answer = input("Please select an option (1-4): ") #asks user for inputs
             if answer.isdigit() and 1 <= int(answer) <= len(self.options): #if statement to check if user input is within range of options available
                 return int(answer) - 1 #returns the user's input minus 1 to match index for sector recommendation
             else: #checks if user input is invalid
                print("Please enter a valid option number.")

#creating class for quiz
class Quiz:
    #initialising quiz attributes
    def __init__(self):
        #hardcodes the quiz questions into the quiz class using a list full of question objects
        self.questions = [
            Question(
                "What type of work environment do you prefer?", #question text
                ["Working with technology and computers", #list of options
                "Helping and  caring for people",
                "Working with numbers and data",
                "Being creative and making things"],
                {0: "Technology", 1: "Healthcare", 2: "Finance", 3: "Creative Arts"} #sector assignment for options
            ),
            Question(
                "Which activity sounds the most appealing to you?",
                ["Building or coding an app",
                "Teaching or mentoring someone",
                "Analysing a financial report",
                "Designing a logo or creating art"],
                {0: "Technology", 1: "Education", 2: "Finance", 3: "Creative Arts"}
            ),
            Question(
                "How do you prefer to solve problems?",
                ["Logically, step-by-step",
                "Talking it through with others",
                "By researching laws or rules",
                "Through creative thinking and brainstorming"],
                {0: "Technology", 1: "Healthcare", 2: "Law", 3: "Creative Arts"}
            ),
            Question(
                "What is most important to you in a career?",
                ["A high salary and financial security",
                "Making a difference in people's lives",
                "Stability and clear structure in work",
                "Freedom to express creativity and innovate"],
                {0: "Finance", 1: "Healthcare", 2: "Engineering", 3: "Creative Arts"}
            ),
            Question(
                "Which subject did you most enjoy at school?",
                ["Maths or Science",
                "English or Social Studies",
                "Arts or Music",
                "Physical Education or Sports"],
                {0: "Engineering", 1: "Law", 2: "Creative Arts", 3: "Healthcare"}
            )
        ]

    #method for running quiz
    def run(self):
        print("================= Career quiz =====================")
        print("Answer the following questions to find the best career path for you.")
        print("=====================================================\n\n")

        sector_scores = {} #defines dictionary for sector assignment and recommendation
        for question in self.questions: #for loop iterates over all question objects
            answer_index = question.display_question() #calls question method and assigns it a variable
            suggested_sector = question.sector_assign[answer_index] #uses the returned value from the question method to check which sector to mark
            if suggested_sector in sector_scores: #checks if sector already has a mark in dictionary
                sector_scores[suggested_sector] += 1 #adds 1 to sector score
            else: #checks if sector hasn't been added yet
                sector_scores[suggested_sector] = 1 #sets sector score to 1

        best_sector = max(sector_scores, key = sector_scores.get) #checks the dictionary for the sector with the highest numerical score and assigns it a variable
        return best_sector #returns the sector to where it was called from

#function to load users from external file
def load_user():
    if os.path.exists("user_info.json") == False: #checks if file does not exist
        return {} #returns empty dictionary
    else: #checks if file exists
        with open("user_info.json", "r") as file: #opens JSON file with read
            content = file.read() #reads and assigns file contents to variable
            if content.strip() == "": #checks if file is completely empty
                return {} #returns empty dictionary
            return json.loads(content) #loads JSON file data and returns it

#function to save user to external file
def save_user(users_dict):
    with open("user_info.json", "w") as file: #opens external file with write which wipes the file
        json.dump(users_dict, file, indent = 4) #load all data from dictionary to JSON file with indents

#function to validate usernames when entered
def validate_username(username):
    if username.strip() == "": #checks if username is completely empty
        return False #returns value False
    elif username.replace(" ", "").isalpha() == False: #checks if username is not all alphabetical
        return False #returns value False
    else: #if username is valid
        return True #returns value True

#function to validate emails when entered
def validate_email(email):
    if "@" not in email or "." not in email: #checks if username does not have proper symbols
        print("Invalid email address. Please check your input.") #tells user their input is invalid
        return False #returns value False
    else: #if email is valid
        return True #returns value True

#function to validate passwords when entered
def validate_password(password):
    if len(password) < 8: #checks if password is less than 8 characters
        print("Your password must be at least 8 characters long.") #tells user their input is invalid
        return False #returns value False
    if any(char.isdigit() for char in password) == False: #checks if password does not have any numbers by checking each character using for loop
        print("Your password must contain at least 1 number.") #tells user their input is invalid
        return False #returns value False
    else: #if password is valid
        return True #returns value True

#function to let users sign up
def sign_up(users_dict):
    print("====================== Sign-up ======================")
    username = input("Enter your name: ").strip() #asks user for their name and assigns it a variable, then strips leading and trailing spaces
    if validate_username(username) == False: #checks if username validation returns False
        return None #returns value None to where it was called from
    email = input("Enter your email address: ").strip() #asks user for their email and assigns it a variable, then strips leading and trailing spaces
    if validate_email(email) == False: #checks if email validation returns False
        return None #returns value None to where it was called from
    elif email in users_dict: #checks if email is alreayd in dictionary
        print("An account with this email has already been registered. \nPlease enter a different email or login") #tells user that account with this email already exists
        return None #returns value None to where it was called from
    else: #if email validation passed
        None
    password = input("Enter a password: ").strip() #asks user for their password and assigns it a variable, then strips leading and trailing spaces
    if validate_password(password) == False: #checks if password validation returns False
        return None #returns value None to where it was called from
    else: #if password validation passed
        None

    education = input("Enter your highest level of education: ").strip() #asks user for their education and assigns it a variable, then strips leading and trailing spaces

    new_user = User(username, email, password, education) #creates new user object using inputs and assigns object a variable
    users_dict[email] = new_user.save_to_file() #saves user by using email as key and then calls user method to return all user details as a dictionary
    save_user(users_dict) #adds new user to external file
    print(f"Account created successfully! Welcome to the career planner {username}!") #account confirmation for user
    return new_user #returns new user object to where it was called from

#function to let users login
def login(users_dict):
    print("====================== Login ======================")
    email = input("Enter your email: ").strip() #asks user for their email and assigns it a variable, then strips leading and trailing spaces
    password = input("Enter your password: ").strip() #asks user for their password and assigns it a variable, then strips leading and trailing spaces

    if email not in users_dict: #checks if email is not in database
        print("No account found with that email. Please try again.") #tells user no account with this email exists
        return None #returns value None to where it was called from
    elif users_dict[email]["password"] != password: #checks if user email does not matche the password in dictionary
        print("Incorrect password. Please try again.") #tells user the password is incorrect
        return None #returns value None to where is was called from
    else: #if login successful
        None

    data = users_dict[email] #uses email as key to take value from dictionary and assign it a variable
    user = User(data["username"], data["email"], data["password"], data["education"]) #creates new user object variable using information gathered from dictionary

    user.quiz_results = data.get("quiz_results", None) #gets user quiz results later since value is different to others
    print(f"Welcome back {user.username}!") #welcomes user back to program
    return user #returns user object to where it was called from

#list of careers hardcoded into the program
careers = [
       #creating career objects using attributes
       Career("Software Engineer", #career name attribute
              "Technology", #career sector attribute
              100000, #career salary attribute
              "Designs and develops software applications and systems.", #career info attribute
              "Bachelor's Degree in Computer Science or related field"), #career education attribute

        Career("Data Scientist", 
              "Technology", 
              120000, 
              "Analyzes and interprets complex datasets to help organizations make informed decisions and notice patterns.", 
              "Bachelor's or Master's Degree in Data Science or related field"),

       Career("Cybersecurity Analyst", 
              "Technology", 
              85000, 
              "Analyzes and protects an organization's computer systems and networks from cyber threats and attacks.", 
              "Bachelor's Degree in Cybersecurity or IT"),

       Career("Doctor", 
              "Healthcare", 
              150000, 
              "Diagnoses and treats illnesses and injuries in patients.", 
              "Medical Degree (MBChB) and residency training"),

       Career("Nurse", 
              "Healthcare", 
              65000, 
              "Provides and coordinates patient care in various healthcare settings.", 
              "Bachelor's Degree in Nursing"),

       Career("Pharmacist",
              "Healthcare",
              120000,
              "Dispenses medications and provides pharmaceutical care to patients.",
              "Bachelor's or Doctor of Pharmacy (PharmD) degree"),

       Career("Psychologist",
              "Healthcare",
              85000,
              "Studies human behavior and mental processes, and provides therapy and counseling.",
              "Master's or Doctoral Degree in Psychology and licensure"),

       Career("Accountant",
              "Finance",
              70000,
              "Prepares and examines financial records and reports.",
              "Bachelor's Degree in Accounting or related field"),

       Career("Financial Analyst",
              "Finance",
              80000,
              "Analyzes financial data and provides insights for investment decisions.",
              "Bachelor's Degree in Finance or Economics"),

       Career("Teacher",
              "Education",
              55000,
              "Educates students in specific subject areas, and develops lesson plans.",
              "Bachelor's Degree in Education or subject degree and teaching certification"),

       Career("Graphic Designer",
              "Arts & Design",
              60000,
              "Creates visual concepts and designs for various media and platforms.",
              "Bachelor's Degree in Graphic Design or related field"),

       Career("Architect",
              "Arts & Design",
              85000,
              "Designs buildings and structures, ensuring they are safe, functional, and aesthetically pleasing.",
              "Bachelor's or Master's Degree in Architecture and licensure"),

       Career("Civil Engineer",
              "Engineering",
              80000,
              "Designs and supervises the construction of infrastructure projects like roads and bridges.",
              "Bachelor's Degree in Civil Engineering and licensure"),

       Career("Marketing Manager",
              "Business",
              75000,
              "Develops and implements marketing strategies to promote products or services.",
              "Bachelor's Degree in Marketing or related field")
]

#function to browse careers
def browse_careers():
    while True: #while loop for validation
        print("====================== Available careers ======================")
        for i, career in enumerate(careers, 1): #iterates over each career in career list and assigns them all a number starting from 1
            print(f"{i}. {career.name} ({career.sector})") #prints numbered careers

        choice = input("Enter a number to view career details, or 0 to go back to the start menu : ").strip() #asks user for choice and assigns it a variable, then strips leading and trailing spaces

        if choice == "0": #if user choice is 0
            break #breaks out loop and returns to where it was called from
        elif choice.isdigit() and 1 <= int(choice) <= len(careers): #checks if user input is within range of career options available
            careers[int(choice) - 1].display_info() #uses user input minus 1 for default index input and then uses career method to display information
            input("\nPress enter to continue.") #waits for user input to continue with program
        else: #if user input is completely invalid
            print("Please enter a valid number for the list.")
            input("\nPress enter to continue.")

#function for the main menu of program
def main_menu(user, users_dict): #function accepts parameters user and user dictionary
    while True: #while loop for validation
        print(f"====================== Main menu | Account: {user.username} ======================") #prints main menu for user to view
        print("Please choose from the following options: ")
        print("1. Browse careers")
        print("2. Take career quiz")
        print("3. View my profile")
        print("0. Logout")
        print("===================================================================================\n")

        choice = input("Enter your option: ").strip() #asks user for their choice and assigns it a variable, then strips leading and trailing spaces

        if choice == "0": #if user choice is 0
            print(f"Logging out. See you next time {user.username}!") #prints log out message
            break #break out of loop and returns to where it was called
        elif choice == "1": #if user choice is 1
            browse_careers() #calls browse careers function
        elif choice == "2": #if user choice is 2
            quiz = Quiz() #creates new quiz object 
            results = quiz.run() #assigns variable to quiz method and waits for value returned
            print("====================== Quiz complete! ======================") #tells user quiz is complete
            print(f"Based on your answer from the quiz, your recommended sector is: {results}!") #prints recommended sector for user
            user.quiz_results = results #updates user object quiz result attribute
            users_dict[user.email]["quiz_results"] = results #updates user dictionary quiz result 
            save_user(users_dict) #calls save user function to update external file
        elif choice == "3": #if user choice is 3
            user.display_profile() #calls user method to display profile
        else: #if user input is completely invalid
            print("Please enter a valid option.")

#starting message
print("===================== Career planner ====================")
print("Welcome to the Career Planning Program! \nThis program will help you identify your career goals, assess your skills and interests, and create a personalized career plan.")
print("=========================================================\n")

#calls function to load data from external file as dictionary and assigns it to variable
users_dict = load_user()

#starting while loop
while True:
    print("=================================================") #prints options for user to choose from
    print("1. Login")
    print("2. Sign-up")
    print("0. Exit")
    print("=================================================\n")

    choice = input("Please choose an input: ").strip() #asks user for their choice and assigns it a variable, then strips leading and trailing spaces

    if choice == "0": #if user choice is 0
        print("Exiting the career planner. See you next time!") #prints exit message
        break #breaks out of while loop exiting program
    elif choice == "1": #if user choice is 1
        user = login(users_dict) #calls login function and assigns returned values to variable
        if user: #checks if user object has been returned
            main_menu(user, users_dict) #continues program and calls main menu function with arguments for user
    elif choice == "2":
        user = sign_up(users_dict) #calls sign in function and assigns returned values to variable
        if user:
            main_menu(user, users_dict) #continues program and calls main menu function with arguments for user
    else: #if user input is completely invalid
        print("Please enter a valid option.")
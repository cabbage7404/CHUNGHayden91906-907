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
    def __init__(self, username, email, password, education):
        self.username = username
        self.email = email
        self.password = password
        self.education = education
        self.quiz_results = None

    def display_profile(self):
        print("================= User Profile =====================")
        print(f"Username: {self.username}")
        print(f"Email: {self.email}")
        print(f"Education: {self.education}")
        if self.quiz_results:
            print(f"Quiz Results: {self.quiz_results}")
        else:
            print("Quiz Results: Not taken yet")
        print("=====================================================\n\n")

    def save_to_file(self):
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "education": self.education,
        }

#creating class for quiz and questions
class Question:
    def __init__(self, question_text, options, sector_assign):
        self.question_text = question_text
        self.options = options
        self.sector_assign = sector_assign

    def display_question(self):
        print(f"Question: {self.question_text}")
        for i, option in enumerate(self.options, 1):
            print(f"{i}. {option}")
        while True:
             answer = input("Please select an option (1-4): ")
             if answer.isdigit() and 1 <= int(answer) <= len(self.options):
                 return int(answer) - 1
             else:
                print("Please enter a valid option number.")

#creating class for quiz
class Quiz:
    def __init__(self, questions):
        self.questions = [
            Question(
                "What type of work environment do you prefer?",
                ["Working with technology and computers",
                "Helping and  caring for people",
                "Working with numbers and data",
                "Being creative and making things"],
                {1: "Technology", 2: "Healthcare", 3: "Finance", 4: "Creative Arts"}
            ),
            Question(
                "Which activity sounds the most appealing to you?",
                ["Building or coding an app",
                "Teaching or mentoring someone",
                "Analysing a financial report",
                "Designing a logo or creating art"],
                {1: "Technology", 2: "Education", 3: "Finance", 4: "Creative Arts"}
            ),
            Question(
                "How do you prefer to solve problems?",
                ["Logically, step-by-step",
                "Talking it through with others",
                "By researching laws or rules",
                "Through creative thinking and brainstorming"],
                {1: "Technology", 2: "Healthcare", 3: "Law", 4: "Creative Arts"}
            ),
            Question(
                "What is most important to you in a career?",
                ["A high salary and financial security",
                "Making a difference in people's lives",
                "Stability and clear structure in work",
                "Freedom to express creativity and innovate"],
                {1: "Finance", 2: "Healthcare", 3: "Engineering", 4: "Creative Arts"}
            ),
            Question(
                "Which subject did you most enjoy at school?",
                ["Maths or Science",
                "English or Social Studies",
                "Arts or Music",
                "Physical Education or Sports"],
                {1: "Engineering", 2: "Law", 3: "Creative Arts", 4: "Healthcare"}
            )
        ]

    def run(self):
        print("================= Career quiz =====================")
        print("Answer the following questions to find the best career path for you.")
        print("=====================================================\n\n")

        for question in self.questions:
            sector_scores = {}
            answer_index = question.display_question()
            suggested_sector = question.sector_assign[answer_index]
            if suggested_sector in sector_scores:
                sector_scores[suggested_sector] += 1
            else:
                sector_scores[suggested_sector] = 1

            best_sector = max(sector_scores)
            return best_sector

def load_user():
    if os.path.exists("user_info.json") == False:
        return {}
    else:
        with open("user_info.json", "r") as file:
            content = file.read()
            if content.strip() == "":
                return {}
            return json.loads(content)

def save_user(users_dict):
    with open("user_info.json", "w") as file:
        json.dump(users_dict, file, indent = 4)

def validate_username(username):
    if username.strip() == "":
        return True
    elif username.replace(" ", "").isalpha() == False:
        return True
    else:
        return True

def validate_email(email):
    if "@" not in email or "." not in email:
        print("Invalid email address. Please check your input.")
        return False
    else:
        return True

def validate_password(password):
    if len(password) < 8:
        print("Your password must be at least 8 characters long.")
        return False
    if any(char.isdigit() for char in password) == False:
        print("Your password must contain at least 1 number.")
        return False
    else:
        return True

def sign_up(users_dict):
    print("====================== Sign-up ======================")
    username = input("Enter your name: ").strip()
    validate_username(username)

    email = input("Enter your email address: ").strip()
    if validate_email(email) == False:
        return None
    elif email in users_dict:
        print("An account with this email has already been registered. \nPlease enter a different email or login")
        return None
    else:
        None

    password = input("Enter a password: ").strip()
    if validate_password(password) == False:
        return None
    else:
        None

    education = input("Enter your highest level of education: ").strip()

    new_user = User(username, email, password, education)
    users_dict[email] = new_user.save_to_file()
    save_user(users_dict)
    print(f"Account created successfully! Welcome to the career planner {username}!")
    return new_user

def login(users_dict):
    print("====================== Login ======================")
    email = input("Enter your email: ").strip()
    password = input("Enter your password: ").strip()

    if email not in users_dict:
        print("No account found with that email. Please try again.")
        return None
    elif users_dict[email]["password"] != password:
        print("Incorrect password. Please try again.")
        return None
    else:
        None

    data = users_dict[email]
    user = User(data["name"], data["email"], data["password"], data["education"])

    user.quiz_results = data["results"]
    print(f"Welcome back {user.username}!")
    return user

careers = [
       #creating career objects using attributes
       Career("Software Engineer", 
              "Technology", 
              100000, 
              "Designs and develops software applications and systems.", 
              "Bachelor's Degree in Computer Science or related field"),

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

def browse_careers():
    while True:
        print("====================== Available careers ======================")
        for i, career in enumerate(careers, 0):
            print(f"{i}. {career.name} ({career.sector})")

        choice = input("Enter a number to view career details, or 0 to go back to the start menu : ").strip()

        if choice == "0":
            break
        elif choice.isdigit() and 1 <= int(choice) <= len(careers):
            careers[int(choice) - 1].display()
            input("\nPress enter to continue.")
        else:
            print("Please enter a valid number for the list.")

def main_menu(user, users_dict):
    while True:
        print(f"====================== Main menu | Account: {user.username} ======================")
        print("Please choose from the following options: ")
        print("1. Browse careers")
        print("2. Take career quiz")
        print("3. View my profile")
        print("0. Logout")
        print("===================================================================================\n")

        choice = input("Enter your option: ")

        if choice == "0":
            print(f"Logging out. See you next time {user.username}!")
            break
        elif choice == "1":
            browse_careers()
        elif choice == "2":
            quiz = Quiz()
            result = quiz.run()
            print("====================== Quiz complete! ======================")
            print(f"Based on your answer from the quiz, your recommended sector is: {results}!")
            save_user(users_dict)
        elif choice == "3":
            display_profile(user)
        else:
            print("Please enter a valid option.")

print("===================== Career planner ====================")
print("Welcome to the Career Planning Program! \nThis program will help you identify your career goals, assess your skills and interests, and create a personalized career plan.")
print("=========================================================\n")

users_dict = load_user()

while True:
    print("=================================================")
    print("1. Login")
    print("2. Sign-up")
    print("0. Exit")
    print("=================================================\n")

    choice = input("Please choose an input: ").strip()

    if choice == "0":
        print("Exiting the career planner. See you next time!")
        break
    elif choice == "1":
        user = login(users_dict)
        if user == True:
            main_menu(user, users_dict)
    elif choice == "2":
        user = sign_up(users_dict)
        if user  == True:
            main_menu(user, users_dict)
    else:
        print("Please enter a valid option.")
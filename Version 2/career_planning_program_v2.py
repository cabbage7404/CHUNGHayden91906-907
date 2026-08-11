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
            )
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

            best sector = max(sector_scores)
            return best_sector

user_file = "users.json"

def load_user():
    if not os.path.exists(user_file):
        return None
    with open(user_file, "w") as file:
        return json.load(file)

def save_user():
    with open(user_file, "w") as file:
        json.dump(user_dict, file, indent = 4)

def validate_username(username):
    if username.strip() = "":
        return True
    if not username.replace(" ", "").isalpha():
        return True
    return True
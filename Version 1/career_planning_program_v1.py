#this is the first verion of my career planning program. It is designed to help users identify their career goals, assess their skills and interests, and create a personalized career plan.

#creating class for careers
class Career:
    def __init__(self, name, sector, salary, description, education_required):
        self.name = name
        self.sector = sector
        self.salary = salary
        self.description = description
        self.education_required = education_required

    def display_info(self):
        print("================= Career Information ================")
        print(f"Career: {self.name}")
        print(f"Sector: {self.sector}")
        print(f"Salary: ${self.salary}")
        print(f"Description: {self.description}")
        print(f"Education Required: {self.education_required}")
        print("=====================================================\n\n")

#adding career info to the program
careers = [
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

#prints introduction to the program
print("================= Career planner ================")
print("Welcome to the Career Planning Program! \nThis program will help you identify your career goals, assess your skills and interests, and create a personalized career plan.")
print("=================================================\n")

#main loop for program
while True:
    print("Available Careers:")
    for i, career in enumerate(careers, 1):
        print(f"{i}. {career.name}")

    print("Enter the number of a career to view more information, or type '0' to quit the program.")
    choice = input("Enter number: ")
    if choice == "0":
        print("Thank you for using the Career Planning Program!")
        break
    elif choice.isdigit() and 1 <= int(choice) <= len(careers):
        careers[int(choice) - 1].display_info()
        input("\nPress Enter to return to the main menu")
    else:
        print("Please enter a valid number from the list or '0' to quit.")
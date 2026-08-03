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


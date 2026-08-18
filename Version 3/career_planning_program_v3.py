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


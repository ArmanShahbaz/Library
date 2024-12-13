import json
import os

fileName = os.path.join(os.getcwd(), 'Library.json')

def load():
    try:
        with open(fileName, 'r') as J:
            return json.load(J)
            
    except FileNotFoundError:
        print("Something went wrong with the database\nTry again later ")

def Input(data): 
    try:
        with open(fileName, 'w') as J:
            json.dump(data, J, indent=4)
            print(f'{data['title']} is added successfully to the Library')
    except FileNotFoundError:
        print("Something went wrong with the database\nTry again later ")



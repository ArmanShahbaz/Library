import fileHandler as Library
import datetime 
import os
from random import randint
from tabulate import tabulate
import json


fieldNames = ['title ', 'author(s) ', 'ISBN ', 'publishing year ', 'price ','quantity', 'Date Added']

Library.Input([])

def addBook():
    title = input('Enter book title : ')
    author =input('Enter author name : ')
    yearPublished = input('Enter publishing year : ')
    while True:
        try:
            price = int(input('Enter price: '))
            if price < 0:
                raise ValueError("Price cannot be negative.")
            break
        except ValueError:
            print("Input a non-negative valid integer for price.")
    while True:
        try:
            quantity = int(input('Enter stock quantity: '))
            if quantity < 0:
                raise ValueError("Quantity cannot be negative.")
            break
        except ValueError:
            print("Input a non-negative valid integer for quantity.")

    timeStamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    ISBN = str(randint(10000,99999))
    
    book = {
        'title': title,
        'author(s)': author,
        'ISBN': ISBN,
        'publishing year': yearPublished,
        'price': price,
        'quantity': quantity,
        'Date Added': timeStamp
    }

    allBooks = Library.load()
    allBooks.append(book)
    Library.Input(allBooks)

def delete():
    allbooks = Library.load()
    title = input("Enter book title to delete")
    ISBN = input('Enter ISBN of the book : ')
    matchData = {
        'title': title,
        'ISBN': ISBN
    }
    updatedData = [row for row in allbooks if not all(row[field] == matchData[field] for field in matchData)]
    if len(allbooks) == len(updatedData):
        print("\n Found no match for deletion")
        return
    Library.Input(updatedData)
    print(f'\n{matchData} is Deleted ')

def Display():
    allBooks = Library.load()
    print("\nCurrent inventory:")
    print(tabulate(allBooks, headers="keys", tablefmt="grid"))

def search():
    allBooks = Library.load()
    while True:
        searchKey = input('Enter book title or ISBN : ').strip()
        results = [
            row for row in allBooks
            if searchKey.lower() in row['title'].lower() or searchKey == row['ISBN']
        ]
        if results:
            return results
        else: 
            print("Nothing matched with your query\nPlease try again")

def show_result():
    results = search()
    
    if results:
        print("\nSearch Results:")
        print(tabulate(results, headers="keys", tablefmt="grid"))


def update():
    allbooks = Library.load()
    matched = search()

    if not matched:
        print("No matching books found. Update aborted.")
        return

    print("\nMatched books:")
    for i, book in enumerate(matched):
        print(f"{i + 1}. {book}")


    choice = input("\nDo you want to update [1] a specific book or [2] all matching books? Enter 1 or 2: ").strip()
    if choice == "1":
        book_number = int(input("Enter the book number to update: ")) - 1
        if book_number < 0 or book_number >= len(matched):
            print("Invalid book number.")
            return
        books_to_update = [matched[book_number]]
    elif choice == "2":
        books_to_update = matched
    else:
        print("Invalid choice. Update aborted.")
        return

    for book in books_to_update:
        print("\nSelected books for update:")
        for key, value in book.items():
            print(f"{key}: {value}")

        while True:
            field_to_update = input("\nEnter the field to update (or type 'done' to finish): ").strip()
            if field_to_update.lower() == 'done':
                break

            if field_to_update not in book:
                print("Invalid field name. Try again.")
                continue

            new_value = input(f"Enter the new value for {field_to_update}: ")

            if field_to_update in ['price', 'quantity']:
                    try:
                        new_value = int(new_value)
                        if new_value < 0:
                            raise ValueError("Input cannot be negative.")
                    except ValueError as e:
                        print(f"Invalid input for {field_to_update}. {e}")
                        continue

            book[field_to_update] = new_value
            print(f"Updated {field_to_update} to {new_value}.")

    
    for updated_record in books_to_update:
        for i, book in enumerate(allbooks):
            if book == updated_record:
                allbooks[i] = updated_record
                break


    Library.Input(allbooks)
    print("\nRecords updated successfully!")



borrowed_file = os.path.join(os.getcwd(), 'borrowed.json')

def lend():
    allBooks = Library.load()
    Display()

    title = input("Enter the title of the book you want to borrow: ").strip()
    ISBN = input("Enter the ISBN of the book: ").strip()

    matched = next((book for book in allBooks if book['title'].lower() == title.lower() and book['ISBN'] == ISBN), None)

    if not matched or matched['quantity'] == 0:
        print(f"The book '{title}' with ISBN {ISBN} is not available for borrowing.")
        return

    
    matched['quantity'] -= 1
    Library.Input(allBooks)

   
    borrower_info = {
        'ISBN': ISBN,
        'title': title,
        'borrow_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'return_date': (datetime.datetime.now() + datetime.timedelta(days=14)).strftime("%Y-%m-%d %H:%M:%S")  # Assume 2 
    }

 
    borrowed_records = []
    if os.path.exists(borrowed_file):
        with open(borrowed_file, 'r') as file:
            borrowed_records = json.load(file)

    borrowed_records.append(borrower_info)

    with open(borrowed_file, 'w') as file:
        json.dump(borrowed_records, file, indent=4)

    print(f"You have borrowed '{title}' with ISBN {ISBN}. Please return it by {borrower_info['return_date']}.")

def return_book():
    borrowed_records = []
    if os.path.exists(borrowed_file):
        with open(borrowed_file, 'r') as file:
            borrowed_records = json.load(file)

    ISBN = input("Enter the ISBN of the book you want to return: ").strip()

    matched_index = -1
    for i, record in enumerate(borrowed_records):
        if record['ISBN'] == ISBN:
            matched_index = i
            break

    if matched_index == -1:
        print("No such borrowed book found.")
        return

    returned_record = borrowed_records.pop(matched_index)

    allBooks = Library.load()
    for book in allBooks:
        if book['ISBN'] == ISBN:
            book['quantity'] += 1
            break

    Library.Input(allBooks)

    with open(borrowed_file, 'w') as file:
        json.dump(borrowed_records, file, indent=4)

    print(f"Book with ISBN {ISBN} has been successfully returned.")




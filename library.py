import utility as u

def main():
    while True:
        print("\nLibrary Management System")
        print("1. Add a new book")
        print("2. Delete a book")
        print("3. Display all books")
        print("4. Search for a book")
        print("5. Update book information")
        print("6. Lend a book")
        print("7. Exit")
        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            u.addBook()
        elif choice == "2":
            u.delete()
        elif choice == "3":
            u.Display()
        elif choice == "4":
            u.show_result() 
        elif choice == "5":
            u.update()
        elif choice == "6":
            u.lend_book()
        elif choice == "7":
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()



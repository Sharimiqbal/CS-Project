import mysql.connector as sql
from os import system
from getpass import getpass
from time import sleep

BOLD_BLUE = '\033[1;34m'
BOLD_GREEN = "\033[1;32m"
RED = '\033[91m'
RE = '\033[0m'
STRAIGHT_LINE = f"+{'':-^5}+{'':-^20}+{'':-^30}+{'':-^13}+"
ROW = f"|{BOLD_BLUE}{'ID':^5}{RE}|{BOLD_BLUE}{'Name':^20}{RE}|{BOLD_BLUE}{'Email':^30}{RE}|{BOLD_BLUE}{'Phone':^13}{RE}|"


def clear_screen():
    system("cls")


def connect():
    return sql.connect(
        host="localhost",
        user="root",
        password="epicodus",
        database="address_book"
    )


def add_contact(cursor, name, email, phone):
    query = "INSERT INTO contacts (name, email, phone) VALUES (%s, %s, %s)"
    try:
        cursor.execute(query, (name, email, phone))
        return True
    except sql.errors.IntegrityError:
        return False


def format_table_data(actual, searched):
    if searched:
        stIdx = actual.lower().find(searched)
        endIdx = stIdx + len(searched)
        l = list(actual)
        l.insert(stIdx, BOLD_GREEN)
        l.insert(endIdx + 1, RE)
        return "".join(l)

    return actual


def view_contacts(cursor, name, email, phone):
    query = "SELECT * FROM contacts WHERE name LIKe %s AND email LIKE %s AND phone LIKE %s"
    cursor.execute(query, ("%" + name + "%", "%" +
                           email + "%", "%" + phone + "%"))
    contacts = cursor.fetchall()

    if not contacts:
        print("No contacts found.")
    else:

        print(STRAIGHT_LINE)
        print(ROW)
        print(STRAIGHT_LINE)

        for contact in contacts:
            print("|", str(contact[0]).center(5), "|", format_table_data(contact[1].center(20), name), "|", format_table_data(
                contact[2].center(30), email), "|", format_table_data(contact[3].center(13), phone), "|", sep="")

        print(STRAIGHT_LINE)


def delete_contact(cursor, contact_id):
    query = "DELETE FROM contacts WHERE id = %s"
    cursor.execute(query, (contact_id,))
    return cursor.rowcount > 0


def find_contact_by_email(cursor, email):
    query = "Select * FROM contacts WHERE LOWER(email) = %s"
    cursor.execute(query, (email,))
    return cursor.fetchone()  # Email is unique so it will only return one


def find_contacts_by_name(cursor, name):
    query = "Select * FROM contacts WHERE LOWER(name) LIKE %s"
    cursor.execute(query, ("%" + name + "%",))
    return cursor.fetchall()


def find_contact_by_phone(cursor, phone):
    query = "Select * FROM contacts WHERE LOWER(phone) = %s"
    cursor.execute(query, (phone,))
    return cursor.fetchone()  # Phone is unique so it will only return one


def main():
    try:
        print("Connecting to Database")
        connection = connect()
    except:
        print("Not able to connect to database, Trying Again...")
        try:
            connection = connect()
        except:
            print("Not able to connect to database, Please Check your details.")
            return

    cursor = connection.cursor()

    while True:
        print(r"""
  __  __
  |  \/  |
  | \  / | ___ _ __  _   _
  | |\/| |/ _ \ '_ \| | | |
  | |  | |  __/ | | | |_| |
  |_|  |_|\___|_| |_|\__,_|

    """)

        print(
            "\n1. Add Contact\n2. View/Search Contacts\n3. Delete Contact\n4. Intro\n5. Exit\n(or /c to clear screen)\n\n Use Choice -h for help \n eg: 2 -h")
        userInput = input(
            "Enter your choice (1/2/3/4): ").strip().lower().split(" ")
        print("\n\n")

        if userInput[0] == "1":
            if len(userInput) > 1 and userInput[1] == "-h":
                print(
                    """This one is to add the data in the database.\nIt will ask for 3 inputs, and add it to database""")
                getpass("Press ↵ Enter ")
                print(
                    """If you are getting Duplicate message then please provided the data with different phone number or email\n\nThis is it.""")
                getpass("Press ↵ Enter and wait 2 seconds...")

                sleep(2)

            else:
                name = input("Enter name (b for menu): ")
                if name.lower() == "b":
                    continue
                elif name.lower() == "q":
                    break
                email = input("Enter email (b for menu): ")
                if email.lower() == "b":
                    continue
                elif email.lower() == "q":
                    break
                phone = input("Enter phone (b for menu): ")
                if phone.lower() == "b":
                    continue
                elif phone.lower() == "q":
                    break

                elif add_contact(cursor, name, email, phone):
                    connection.commit()

                    print("Contact added successfully.")
                else:
                    print("Duplicate email or phone, Please try again!")

        elif userInput[0] == "2":
            if len(userInput) > 1 and userInput[1] == "-h":
                print("This one is to search and view the contact in database. \n")
                print("To view whole data just input '2' Or\nTo search You can use")
                getpass("Press ↵ Enter")
                print(
                    "\t1. n:<nameOfUserHere> to search for a person with name,\n\t\tExample: 2 n:Abc")
                getpass("Press ↵ Enter")
                print(
                    "\t2. e:<emailOfContactHere> to search for a person with his email,\n\t\tExample: 2 e:xyz@gmail.com")
                getpass("Press ↵ Enter")
                print(
                    "\t3. p:<phoneOfContactHere> to search for a person with his phone number,\n\t\tExample: 2 e:1234567890")
                getpass("Press ↵ Enter")
                print(
                    "You can also combine all of these together to search\n\tFor Example\n\t\t2 n:Xyz e:xyz@mail.com p:9899\n\t\t\t This will return the table with contacts that contains these details.\n")
                getpass("Press ↵ Enter")
                print(
                    "Just make sure first value has to be 2 and rest can be in any order\nFor Example\n\t\t2 p:9899 n:Xyz e:xyz@mail.com\n\n This is it.")
                getpass("Press ↵ Enter and wait 2 seconds...")
                sleep(2)

            else:
                name = ""
                email = ""
                phone = ""
                for data in userInput[1:]:
                    if data.startswith("n:"):
                        name = data[2:]
                    elif data.startswith("e:"):
                        email = data[2:]
                    elif data.startswith("p:"):
                        phone = data[2:]
                    elif name and email and phone:  # No need to loop of all data is collected
                        break
                view_contacts(cursor, name, email, phone)
                sleep(2)
        elif userInput[0] == "3":
            if len(userInput) > 1 and userInput[1] == "-h":
                print("""This one is to delete a contact from Database.""")
            else:
                contact_id = input(
                    "Enter the ID of the contact to delete (Don't know the ID? enter n OR b for MENU OR q to quite): ")

                if contact_id.lower() == "b":
                    continue

                elif contact_id.lower() == "n":
                    print(
                        "1. Find ID by Name\n2. Find ID by Email\n3. Find ID by Phone.\nb. MENU\nq to quite.")

                    dChoice = input("Enter your choice: 1/2/3/b/q: ").lower()

                    if dChoice == "1":
                        print(RED,
                              "Note: Name is not Unique so there might me more than 1 value", RE, sep="")

                        name = input("Enter the name of Person: ")
                        if name.lower() == "b":
                            continue
                        elif name.lower() == "q":
                            break

                        contacts = find_contacts_by_name(cursor, name)

                        print(STRAIGHT_LINE)
                        print(ROW)
                        print(STRAIGHT_LINE)

                        for contact in contacts:
                            print("|", str(contact[0]).center(5), "|", contact[1].center(
                                20), "|", contact[2].center(30), "|", contact[3].center(13), "|", sep="")
                        print(STRAIGHT_LINE)

                        print("\n\n")
                        contact_id = input(
                            "Enter the ID of the contact to delete (q to quite or b for MENU): ")

                    elif dChoice == "2":
                        email = input("Enter the email of Person: ")
                        if email.lower() == "b":
                            continue
                        elif email.lower() == "q":
                            break
                        contact = find_contact_by_email(cursor, email)

                        print(f"Contact with {email=} is this")
                        print(STRAIGHT_LINE)
                        print(ROW)
                        print(STRAIGHT_LINE)
                        print("|", str(contact[0]).center(5), "|", contact[1].center(
                            20), "|", contact[2].center(30), "|", contact[3].center(13), "|", sep="")

                        print(STRAIGHT_LINE)

                        if input("DO YOU WANT TO DELETE THIS ACCOUNT. y/n ").lower() == "y":
                            contact_id = str(contact[0])
                        else:
                            continue
                    elif dChoice == "3":

                        phone = input("Enter the phone of Person: ")
                        if phone.lower() == "b":
                            continue
                        elif phone.lower() == "q":
                            break
                        contact = find_contact_by_phone(cursor, phone)

                        if contact is not None:
                            print(f"Contact with {phone=} is this")

                            print(STRAIGHT_LINE)
                            print(ROW)
                            print(STRAIGHT_LINE)
                            print("|", str(contact[0]).center(5), "|", contact[1].center(
                                20), "|", contact[2].center(30), "|", contact[3].center(13), "|", sep="")

                            print(STRAIGHT_LINE)

                            if input("DO YOU WANT TO DELETE THIS ACCOUNT. y/n ").lower() == "y":
                                contact_id = str(contact[0])
                            else:
                                continue
                        else:
                            print(f"No Contact with {phone=}")
                            continue

                    elif dChoice.lower() == "q":
                        break
                    else:
                        continue

                if contact_id.lower() == 'q':
                    break
                elif contact_id.lower() == 'b':
                    continue

                elif delete_contact(cursor, contact_id):
                    connection.commit()
                    print("\n****Contact deleted successfully.****")
                else:
                    print(f"No Contact found with {contact_id=}")
        elif userInput[0] == "4":
            print("""This is Address book application using Python.
                  \rYou can Add Search and Delete Contacts\nYou can use b to back to Menu and q to quite in any Input\n\n""")
            sleep(1)

        elif userInput[0] == "5" or userInput[0] == "q":
            break

        elif userInput[0] == "/c":
            clear_screen()
        else:
            print("Invalid choice. Please try again.")

    connection.close()


main()

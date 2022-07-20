from datetime import datetime
import sqlite3

conection = sqlite3.connect("todolist.db")
cursor = conection.cursor()

# მონაცემთა ბაზის სტრუქტურის შექმნა
cursor.execute("""CREATE TABLE IF NOT EXISTS tasks(
                task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                create_date TEXT NOT NULL,
                deadline_date TEXT,
                task TEXT NOT NULL)""")


# შესასრულებელი დავალების კომპონენტების შექმნა
class Todo:

    def __init__(self, text, deadline):
        self.text = text
        self.deadline = deadline
        self.date = datetime.now()

    def __str__(self):
        if self.deadline == None:
            return f'Create/edit Date: {self.date.strftime("%d/%m/%Y %H:%M")}\nDeadline: None\nTodo: {self.text}'

        else:
            return f'Create/edit Date: {self.date.strftime("%d/%m/%Y %H:%M")}\nDeadline: {self.deadline.strftime("%d/%m/%Y %H:%M")}\nTodo: {self.text}'


# ოპერაციები მონაცემთა ბაზაზე
class Database:

    def __init__(self):
        self.date = datetime.now()

    def add_db(self, todo):
        if todo.deadline == None:
            cursor.execute("""INSERT INTO tasks (create_date, deadline_date, task)
                            VALUES
                            (?,?,?)""",(str(self.date.strftime("%d/%m/%Y %H:%M")),
                                        "None",
                                        todo.text))
        else:
            cursor.execute("""INSERT INTO tasks (create_date, deadline_date, task)
                            VALUES
                            (?,?,?)""",(str(self.date.strftime("%d/%m/%Y %H:%M")),
                                        str(todo.deadline.strftime("%d/%m/%Y %H:%M")),
                                        todo.text))
        conection.commit()

    def getALL(self):
        cursor.execute("""SELECT * FROM tasks""")
        all_tasks = cursor.fetchall()
        return all_tasks


    def update_db(self, oldTodo, newTodo):
        if newTodo.deadline == None:
            cursor.execute(f'''UPDATE tasks
                                SET
                                    create_date = "{self.date.strftime("%d/%m/%Y %H:%M")}",
                                    deadline_date = "None",
                                    task = "{newTodo.text}"
                                WHERE
                                    task_id = {oldTodo}''')
        else:
            cursor.execute(f'''UPDATE tasks
                                SET
                                    create_date = "{self.date.strftime("%d/%m/%Y %H:%M")}",
                                    deadline_date = "{newTodo.deadline.strftime("%d/%m/%Y %H:%M")}",
                                    task = "{newTodo.text}"
                                WHERE
                                    task_id = {oldTodo}''')
        conection.commit()


    def check_db(self):
        cursor.execute("""SELECT * FROM tasks""")
        checker = cursor.fetchall()
        checker_num = 0
        for i in checker:
            checker_num +=1
        return bool(checker_num)

    def delete_db(self, todoIndex):
        cursor.execute(f'''DELETE FROM tasks
                            WHERE task_id = {todoIndex}''')
        conection.commit()


# შუამავალი კლასი ბაზაში ოპერაციების შესასრულებლად
class Manager:

    def __init__(self, db):
        self.db = db

    def add(self, todo):
        self.db.add_db(todo)

    def update(self, oldTodo, newTodo):
        self.db.update_db(oldTodo, newTodo)

    def len_data(self):
        return self.db.getALL()[-1][0]

    def id_check(self):
        check_list = []
        for i in range(len(self.db.getALL())):
            check_list.append(self.db.getALL()[i][0])
        return check_list

    def showALL(self):
        data = self.db.getALL()
        for item in data:
            print(item)
            print("-" * 50)

    def check_data(self):
        return self.db.check_db()

    def delete(self, todoIndex):
        return self.db.delete_db(todoIndex)


#დუბლირების თავიდან ასაცილებლად
def check_inputs(manager):
    if not manager.check_data():
        print("\n")
        print("XXXXX","Database is Empty!","XXXXX")

    else:
        while True:
            manager.showALL()

            print("\n")
            print("Type 'exit' to go back to main manu, or enter the task num to continue")
            index = input("Task_id: ")

            if index == 'exit':
                return index

            if not index.isdigit():
                print("\n")
                print("Please enter the digit!")
                continue

            if int(index) > manager.len_data():
                print("XXXXX","Out of range!","XXXXX")
                print("\n")
                continue

            if int(index) not in manager.id_check():
                print("XXXXX","Indicated index num is incorrect!","XXXXX")
                print("\n")
                continue

            todoIndex = int(index)

            return todoIndex

#კოდის დუბლირების შესამცირებლად
def date_format():
    date_input = input("Deadline date (ex. YYYY,MM,DD,HH,MM): ")
    date_components = date_input.split(",")
    deadline = datetime(int(date_components[0]),int(date_components[1]),int(date_components[2]),int(date_components[3]),int(date_components[4]),0)
    return deadline

def date_check():
    check = True
    while check:
        try:
            deadline = date_format()
            check = False
            return deadline
        except (ValueError, IndexError):
            print("Date value is invalid, please enter the relevant deadline date!")

#ძირითადი ოპერაციები რაც მომხმარებელმა უნდა აკეთოს
#add, edit, delete, show
def menu():
    choice = None

    db = Database()
    manager = Manager(db)

    #q ს აკრეფისას რომ გამოვიდეს პროგრამიდან
    while choice != "Q":
        print("\n")
        print("ToDo List Menu:")
        print("1. Create new task")
        print("2. Edit task")
        print("3. Delete task from list")
        print("4. Show all tasks")
        print("Type 'Q' for Exit")
        print("\n")

        choice = input("Action: ").upper()

        if choice == "1":
            print("Type 'exit' to go back to main manu, or enter the text for task")
            text = input("Text: ")
            if text == 'exit':
                continue

            has_deadline = input("If the task has a deadline, type 'Y'. Otherwise click just Enter/Return button.\nDeadline: --- ").upper()
            if has_deadline == 'Y':
                deadline = date_check()
            else:
                deadline = None

            todo = Todo(text, deadline)
            manager.add(todo)

        elif choice == "2":
            oldTodo = check_inputs(manager)

            if oldTodo == 'exit':
                continue
            else:
                text = input("Enter new text: ")

                has_deadline = input("If the task has a deadline, type 'Y'. Otherwise click just Enter/Return button.\nDeadline: --- ").upper()
                if has_deadline == 'Y':
                    deadline = date_check()
                else:
                    deadline = None

                newTodo = Todo(text, deadline)
                manager.update(oldTodo, newTodo)

        elif choice == "3":
            todoIndex = check_inputs(manager)

            if todoIndex == 'exit':
                continue
            else:
                manager.delete(todoIndex)

        elif choice == "4":

            if manager.check_data():
                manager.showALL()
            else:
                print("Database is Empty!")

        elif choice == "Q":
            print("Bye bye!")
            print("\n")

        else:
            print("-"*50)
            print("Wrong choice! please enter: 1/2/3/4 or Q!")


menu()

#################
cursor.close()
conection.close()
#################

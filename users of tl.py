import sqlite3 as sql
import os
from task_list2 import Tasks, Options, Opt_json, Opt_csv, Opt_txt

con = sql.connect('users.db')
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS `users` (
            `id` INT, `name` TEXT, `list_of_tasks` TEXT, `password` TEXT, `strategy` TEXT)''')
zerro_user = (0, 'register new user', False, False, False)
cur.execute("""INSERT OR IGNORE INTO users VALUES(?, ?, ?, ?, ?);""", zerro_user)
con.commit()

def print_list_of_users():
    cur = con.cursor()
    cur.execute("SELECT * FROM `users`")
    rows = cur.fetchall()
    for row in rows:
        print(row[0], row[1])
    con.commit()

def delete_user(del_numb):
    cur = con.cursor()
    cur.execute("DELETE FROM `users` WHERE id={del_numb};")
    print_list_of_users()
    con.commit()

def search_user(numb):
    cur = con.cursor()
    sql = "SELECT * FROM `users` WHERE id=?"
    cur.execute(sql, numb)
    row = cur.fetchone()
    return row

def user_menu():
    while True:
        print_list_of_users()
        menu_numb = input('Greetings. Choose your account, enter profile number. ')
        row = search_user(menu_numb)
        if not row:
            print("Not found.")
            continue
        you_user = User(menu_numb)
        menu_password = input('Enter a password - ')
        if menu_password == row[3]:
            print(f'Hello, {you_user.user_name}')
            os.getcwd()
            try:
                os.chdir(f'task_folder/{you_user.user_name}')
            except FileNotFoundError:
                os.mkdir(f'task_folder/{you_user.user_name}')
            file_lis = os.listdir()
            menu_dict = {
                '1': (you_user.strategy.print_task_list, 'open task list'),
                '2': (you_user.strategy.print_add, 'add a new task'),
                '3': (you_user.strategy.print_delete, 'delete a task'),
                '4': (you_user.strategy.print_edit, 'edit a task'),
                '5': (you_user.strategy.print_mark, 'mark a task as completed'),
                '6': (you_user.strategy.print_highlight_all, 'highlight all tasks'),
                '7': (you_user.strategy.print_show_completed, 'show only completed tasks'),
                '8': (you_user.strategy.print_show_uncompleted, 'show only uncompleted tasks'),
                '9': (you_user.strategy.print_search, 'search by text'),
                '10': (you_user.strategy.print_save, 'save this task list'),
                '0': (you_user.strategy.exit_from, 'exit')
            }
            while menu_dict:
                print("Menu: ")
                for i in menu_dict:
                    print(i, menu_dict[i][1], sep=' ', end='\n')
                menu_numb = input('Choose, what should we do. ')
                if menu_numb not in menu_dict.keys():
                    print("Incorrect. Try again")
                    continue
                menu_dict[menu_numb][0]()
            return True
        else:
            if menu_numb == '0':
                print(f'User {you_user.user_name} was created.')
            else:
                print('Incorrect password. Try again')
            continue

class User:
    def __init__(self, user_id):
        if user_id == '0':
            self.new_user = True
            self.commmit()
        else:
            self.new_user = False
            self._populate_user(user_id)

    def strategy_choice(self):
        while True:
            choice = input("How you ant to save your task list? 1 - in json file, 2 - in csv file, 3 - in txt file? ")
            if int(choice) == 1:
                return Opt_json
            elif int(choice) == 2:
                return Opt_csv
            elif int(choice) == 3:
                return Opt_txt
            else:
                print('Incorrect choice.')
                continue

    def commmit(self):
        if self.new_user == True:
            self.user_name = input('Enter your name - ')
            self.password = input('Enter your password - ')
            self.strategy = self.strategy_choice()
            cur = con.cursor()
            row_numbs = cur.execute("SELECT COUNT(*) FROM `users`").fetchone()
            self.user_id = row_numbs[0]
            new_user = (self.user_id, self.user_name, False, self.password, self.strategy)
            cur.execute("""INSERT OR IGNORE INTO users VALUES(?, ?, ?, ?, ?);""", new_user)
            con.commit()

    def _populate_user(self, user_id):
        row = search_user(user_id)
        self.user_id = user_id
        self.user_name = row[1]
        self.strategy = row[4]
        self.password = row[3]
        self.tasklist = row[2]

user_menu()

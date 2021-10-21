import json
import csv
import os

class Tasks:
    def __init__(self, task):
        self.task = task
        self.task_status = "In process"

    def __repr__(self):
        return f'{self.task} - {self.task_status}'

class Options:
    task_list = []

    @staticmethod
    def print_periodic_task_list():
        if len(Options.task_list) == 0:
            print("You haven't any tasks yet.")
        else:
            i = 1
            print('Your tasks:')
            while i < (len(Options.task_list) + 1):
                for el in Options.task_list:
                    print(i, el)
                    i += 1

    def success_dec(func):
        def wrapper(*args, **kwargs):
            while True:
                result = func(*args, **kwargs)
                Options.print_periodic_task_list()
                answer = input('Shall we repeat? (y/n) ')
                if answer.lower() not in ('y', 'yes'):
                    break
                continue
            return result
        return wrapper

    @staticmethod
    @success_dec
    def print_add():
        Options.task_list.append(Tasks(input('Enter a new task - ')))
        return Options.task_list

    def valid_number(number):
        return number.isdigit() and 0 < int(number) <= len(Options.task_list)

    @staticmethod
    @success_dec
    def print_delete():
        while True:
            Options.print_periodic_task_list()
            del_task = input('What task do you want to delete? Enter a number - ')
            if not Options.valid_number(del_task):
                print('Non valid task number! ')
                Options.print_periodic_task_list()
                continue
            del [Options.task_list[int(del_task) - 1]]
            break
        return Options.task_list

    @staticmethod
    @success_dec
    def print_edit():
        while True:
            Options.print_periodic_task_list()
            edit_task = input('What task do you want to edit? Enter a number - ')
            if not Options.valid_number(edit_task):
                print('Non valid task number!')
                continue
            new_task = input('Enter a new text - ')
            unedited_task = Options.task_list[int(edit_task) - 1]
            unedited_task_status = Options.task_list[int(edit_task) - 1].task_status
            a = Tasks(new_task)
            a.task_status = unedited_task_status
            Options.task_list.append(a)
            del unedited_task
            break
        return Options.task_list

    @staticmethod
    @success_dec
    def print_mark():
        while True:
            Options.print_periodic_task_list()
            numb_task_for_status_changing = input('What task do you want to mark as completed? Enter a number - ')
            if not Options.valid_number(numb_task_for_status_changing):
                print('Non valid task number!')
                continue
            numb_task_for_status_changing = int(numb_task_for_status_changing) - 1
            Options.task_list[numb_task_for_status_changing].task_status = 'Done'
            break
        return Options.task_list

    @staticmethod
    @success_dec
    def print_highlight_all():
        while True:
            multiple = input('If you want to delete all tasks, press 1. \n'
                             'If you want to mark all tasks as completed, press 2. \n'
                             'If you want to mark all tasks as uncompleted, press 3. - ')
            if multiple == '1':
                Options.task_list = []
            elif multiple == '2':
                for i in range(len(Options.task_list)):
                    Options.task_list[i].task_status = "Done"
                Options.print_periodic_task_list()
            elif multiple == '3':
                for i in range(len(Options.task_list)):
                    Options.task_list[i].task_status = "In process"
                Options.print_periodic_task_list()
            else:
                print('Non valid choice enter.')
                continue
            break
        return Options.task_list

    @staticmethod
    def print_show_completed():
        list_done = list(filter(lambda x: x.task_status == "Done", Options.task_list))
        if len(list_done) == 0:
            print("You haven't any completed tasks.")
        num = 1
        while num < (len(list_done) + 1):
            for i in list_done:
                print(num, i)
                num += 1
        return True

    @staticmethod
    def print_show_uncompleted():
        list_undone = list(filter(lambda x: x.task_status == "In process", Options.task_list))
        if len(list_undone) == 0:
            print("All tasks are completed.")
        num = 1
        while num < (len(list_undone) + 1):
            for i in list_undone:
                print(num, i)
                num += 1
        return True

    @staticmethod
    def print_search():
        search = input('What should we look for? ')
        for i in Options.task_list:
            if i.task.find(search) != -1:
                print(i)
        return Options.task_list

    @staticmethod
    def print_task_list():
        Options.print_periodic_task_list()
        a = input('Do you want to open task list from file? (y/n) ')
        if a.lower() in ('y', 'yes'):
            file_lis = os.listdir()
            if len(file_lis) == 0:
                print('No saved files')
            else:
                print("Saved files:")
                for i in range(len(file_lis)):
                    print(i + 1, file_lis[i], sep=' ')
                file_numb = int(input("What file you want to open? Enter a number "))
                f = open(file_lis[file_numb - 1], 'r')
                f = [line.rstrip() for line in f]
                empty = []
                for line in f:
                    l = line.split(' - ')
                    a = Tasks(l[0])
                    a.task_status = l[1]
                    empty.append(a)
                print('Saved in file:')
                i = 1
                while i < (len(empty) + 1):
                    for el in empty:
                        print(i, el)
                        i += 1
            b = input('Do you want to transfer task list from file for new operations? (y/n) ')
            if b.lower() in ('y', 'yes'):
                Options.task_list = empty
                Options.print_periodic_task_list()
        return True

    @staticmethod
    def print_save():
        file_lis = os.listdir()
        print("Saved files:")
        for i in range(len(file_lis)):
            print(i + 1, file_lis[i], sep=' ')
        while True:
            file_choice = input("Choose: 1 - save to a new file \n2 - save to existing file" )
            if file_choice == '1':
                file_name = input("In what file you want to save your task list? ")
                f = open('somefile.txt', 'w')
                for i in Options.task_list:
                    f.write(str(i) + '\n')
                os.rename('somefile.txt', (file_name + '.txt'))
                f.close()
                print('Saved:')
                Options.print_periodic_task_list()
                break
            elif file_choice == '2':
                file_numb = int(input("In what file you want to save your task list? Enter a number "))
                f = open(file_lis[file_numb - 1], 'w')
                for i in Options.task_list:
                    f.write(str(i) + '\n')
                f.close()
                print('Saved:')
                Options.print_periodic_task_list()
                break
            else:
                continue
        return True

    @staticmethod
    def exit_from():
        exit()

class Opt_json(Options):

    @staticmethod
    def list_from_load(list_from_file, new_eq_list):
        for i in list_from_file:
            for key in i:
                a = Tasks(key)
                a.task_status = i[key]
                new_eq_list.append(a)
        return new_eq_list

    @staticmethod
    def print_task_list():
        Options.print_periodic_task_list()
        a = input('Do you want to open task list from file? (y/n) ')
        if a.lower() in ('y', 'yes'):
            file_lis = os.listdir()
            if len(file_lis) == 0:
                print('No saved files')
            else:
                print("Saved files:")
                for i in range(len(file_lis)):
                    print(i + 1, file_lis[i], sep=' ')
                file_numb = int(input("What file you want to open? Enter a number "))
                with open(file_lis[file_numb - 1], 'r') as task_file:
                    data = json.load(task_file)
                load_list= []
                Options.list_from_load(data, load_list)
                print('Saved in file:')
                i = 1
                while i < (len(data) + 1):
                    for el in data:
                        print(i, el)
                        i += 1
            b = input('Do you want to transfer task list from file for new operations? (y/n) ')
            if b.lower() in ('y', 'yes'):
                Options.task_list = load_list
                Options.print_periodic_task_list()
        return True

    @staticmethod
    def temper_list(empty_list, any_list):
        for i in any_list:
            mini = {i.task: i.task_status}
            empty_list.append(mini)
        return empty_list

    @staticmethod
    def print_save():
        file_lis = os.listdir()
        print("Saved files:")
        for i in range(len(file_lis)):
            print(i + 1, file_lis[i], sep=' ')
        while True:
            file_choice = input("1 - save to a new file \n2 - save to existing file")
            if file_choice == '1':
                file_name = input("In what file you want to save your task list?")
                temper = []
                Options.temper_list(temper, Options.task_list)
                with open('somefile.json', 'w') as task_file:
                    json.dump(temper, task_file)
                temper.clear()
                os.rename('somefile.json', (file_name + '.json'))
                print('Saved:')
                Options.print_periodic_task_list()
                break
            elif file_choice == '2':
                file_numb = int(input("In what file you want to save your task list? Enter a number"))
                temper = []
                Options.temper_list(temper, Options.task_list)
                with open(file_lis[file_numb - 1], 'w') as save_file:
                    json.dump(temper, save_file)
                temper.clear()
                print('Saved:')
                Options.print_periodic_task_list()
                break
            else:
                continue
        return True

class Opt_csv(Options):

    @staticmethod
    def print_task_list():
        Options.print_periodic_task_list()
        a = input('Do you want to open task list from file? (y/n) ')
        if a.lower() in ('y', 'yes'):
            file_lis = os.listdir()
            if len(file_lis) == 0:
                print('No saved files')
            else:
                print("Saved files:")
                for i in range(len(file_lis)):
                    print(i + 1, file_lis[i], sep=' ')
                file_numb = int(input("What file you want to open? Enter a number "))
                with open(file_lis[file_numb - 1], 'r') as task_file:
                    reader = csv.DictReader(task_file)
                    line = 0
                    rows = []
                    for row in reader:
                        if line == 0:
                            headers = row
                        else:
                            a = Tasks(row['task'])
                            a.task_status = row['task_status']
                            rows.append(a)
                        line += 1
                print('Saved in file:')
                i = 1
                while i < (len(rows) + 1):
                    for el in rows:
                        print(i, el)
                        i += 1
            b = input('Do you want to transfer task list from file for new operations? (y/n) ')
            if b.lower() in ('y', 'yes'):
                Options.task_list = rows
                Options.print_periodic_task_list()
        return True

    @staticmethod
    def print_save():
        file_lis = os.listdir()
        print("Saved files:")
        for i in range(len(file_lis)):
            print(i + 1, file_lis[i], sep=' ')
        while True:
            file_choice = input("1 - save to a new file \n2 - save to existing file")
            if file_choice == '1':
                file_name = input("In what file you want to save your task list?")
                with open('somefile.csv', 'w') as task_file:
                    writer = csv.writer(task_file)
                    writer.writerow(['task', 'task_status'])
                    for i in Options.task_list:
                        writer.writerow([i.task, i.task_status])
                os.rename('somefile.csv', (file_name + '.csv'))
                print('Saved:')
                Options.print_periodic_task_list()
                break
            elif file_choice == '2':
                file_numb = int(input("In what file you want to save your task list? Enter a number"))
                with open(file_lis[file_numb - 1], 'w') as save_file:
                    writer = csv.writer(save_file)
                    writer.writerow(['task', 'task_status'])
                    for i in Options.task_list:
                        writer.writerow([i.task, i.task_status])
                print('Saved:')
                Options.print_periodic_task_list()
                break
            else:
                continue
        return True

class Opt_txt(Options):

    @staticmethod
    def print_task_list():
        Options.print_periodic_task_list()
        a = input('Do you want to open task list from file? (y/n) ')
        if a.lower() in ('y', 'yes'):
            file_lis = os.listdir()
            if len(file_lis) == 0:
                print('No saved files')
            else:
                print("Saved files:")
                for i in range(len(file_lis)):
                    print(i + 1, file_lis[i], sep=' ')
                file_numb = int(input("What file you want to open? Enter a number "))
                f = open(file_lis[file_numb - 1], 'r')
                f = [line.rstrip() for line in f]
                empty = []
                for line in f:
                    l = line.split(' - ')
                    a = Tasks(l[0])
                    a.task_status = l[1]
                    empty.append(a)
                print('Saved in file:')
                i = 1
                while i < (len(empty) + 1):
                    for el in empty:
                        print(i, el)
                        i += 1
                f.close()
            b = input('Do you want to transfer task list from file for new operations? (y/n) ')
            if b.lower() in ('y', 'yes'):
                Options.task_list = empty
                Options.print_periodic_task_list()
        return True

    @staticmethod
    def print_save():
        file_lis = os.listdir()
        print("Saved files:")
        for i in range(len(file_lis)):
            print(i + 1, file_lis[i], sep=' ')
        while True:
            file_choice = input("Choose: 1 - save to a new file \n2 - save to existing file" )
            if file_choice == '1':
                file_name = input("In what file you want to save your task list? ")
                f = open('somefile.txt', 'w')
                for i in Options.task_list:
                    f.write(str(i) + '\n')
                os.rename('somefile.txt', (file_name + '.txt'))
                f.close()
                print('Saved:')
                Options.print_periodic_task_list()
                break
            elif file_choice == '2':
                file_numb = int(input("In what file you want to save your task list? Enter a number "))
                f = open(file_lis[file_numb - 1], 'w')
                for i in Options.task_list:
                    f.write(str(i) + '\n')
                f.close()
                print('Saved:')
                Options.print_periodic_task_list()
                break
            else:
                continue
        return True

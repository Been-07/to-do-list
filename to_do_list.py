# ======================================|
# Author: Benjamin Shojaee              |
# GitHub: https://github.com/Been-07    |
# ORCID: 0009-0005-2756-7140            |
# ======================================|
import csv
import json

class Task():
    def __init__(self,name,explanation,priority):
        self.name = name
        self.explanation = explanation
        self.priority = priority

    def __str__(self):
        return f"{self.name} , {self.explanation} ,Priority: {self.priority}"

class ToDoList():
    def __init__(self):
        self.Tasks = []
        self.filename_base = "Tasks"
        self.strorage_format = "csv"
        self.load()

    def add_task(self,name,explanation,priority):
        new_task = Task(name,explanation,priority)
        self.Tasks.append(new_task)
        self.save()

    def remove_task(self,index):
        if 0 <= index < len(self.Tasks):
            remove = self.Tasks.pop(index)
            print(f"work{remove.name} has been removed")
            self.save()
        else:
            print("The number entered does not exist")

    def show_task(self):
        if len(self.Tasks) == 0:
            print("The task list is empty")
        else:
            for i,t in enumerate(self.Tasks):
                print(f"{i+1}-{t}")

    def _get_filename(self):
        if self.strorage_format == "csv":
            return self.filename_base + ".csv"
        else:
            return self.filename_base + ".json"
        
    def save_to_csv(self,filename):
        with open(filename,mode='w',newline='',encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['name','explanation','priority'])
            for task in self.Tasks:
                writer.writerow([task.name,task.explanation,task.priority])

    def load_from_csv(self,filename):
        try:
            with open(filename,mode='r',encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)
                for r in reader:
                    if len(r) >= 3:
                        name,explanation,priority = r[0],r[1],r[2]
                        task = Task(name,explanation,priority)
                        self.Tasks.append(task)
        except FileNotFoundError as e:
            print(f"{e}")

    def save_to_json(self,filename):
        data = []
        for t in self.Tasks:
            data.append({
                "name" : t.name,
                "explanation" : t.explanation,
                "priority" : t.priority
            })
        with open(filename,mode='w',encoding='utf-8') as file:
            json.dump(data,file,indent=4,ensure_ascii=False)

    def load_from_json(self,filename):
        try:
            with open(filename,mode='r',encoding='utf-8') as file:
                data = json.load(file)
                for item in data:
                    task = Task(item['name'],item['explanation'],item['priority'])
                    self.Tasks.append(task)
        except FileNotFoundError as e:
            print(f"{e}")

    def save(self):
        filename = self._get_filename()
        if self.strorage_format == "csv":
            self.save_to_csv(filename)
        else:
            self.save_to_json(filename)
    
    def load(self):
        filename = self._get_filename()
        if self.strorage_format == "csv":
            self.load_from_csv(filename)
        else:
            self.load_from_json(filename)

    def change_format(self,new_format):
        if new_format in ['csv','json']:
            self.strorage_format = new_format
            self.save()
            print(f"Storage format changed to {new_format}")    
        else:
            print("Invalid format. Choose 'csv' or 'json'")

def main():
    to_do_list = ToDoList()
    while True:
        print("=" * 70)
        print("TO-DO-LIST-MENU".center(70))
        print("1.Add Task")
        print("2.Remove Task")
        print("3.Show Tasks")
        print(f"4.Change Storage Format(Current Format {to_do_list.strorage_format})")
        print("5.Exit")
        choice = int(input("Choose an option(1-5):"))
        if choice == 1:
            name = input("Task name: ")
            explanation = input("Description: ")
            
            valid_priorities = ['very low', 'low', 'medium', 'high', 'very high']
            while True:
                priority = input("Priority (very low, low, medium, high, very high): ").strip().lower()
                priority = ' '.join(priority.split())
                if priority in valid_priorities:
                    break
                else:
                    print(f"Invalid priority! Please choose from: {', '.join(valid_priorities)}")
            to_do_list.add_task(name, explanation, priority)
            print("Task added ")
        elif choice == 2:
            to_do_list.show_task()
            if len(to_do_list.Tasks) > 0:
                try:
                    index = int(input("Enter the job number you want to delete: "))
                    index -= 1
                    to_do_list.remove_task(index)
                except ValueError:
                    print("Please enter a valid number!")
            else:
                print("Nothing to remove")
        elif choice == 3:
            to_do_list.show_task()
        elif choice == 4:
            new_format = input("Enter csv or json: ").lower()
            to_do_list.change_format(new_format)
        elif choice == 5:
            print("bye bye")
            break
        else:
            print("The selected option does not exist, please try again!")



if __name__ == "__main__":
    main()

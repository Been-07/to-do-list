# ======================================|
# Author: Benjamin Shojaee              |
# GitHub: https://github.com/Been-07    |
# ORCID: 0009-0005-2756-7140            |
# ======================================|

import csv
import json

# Class for each task
class Task:
    def __init__(self, name, desc, priority):
        self.name = name
        self.desc = desc
        self.priority = priority

    def __str__(self):
        return f"{self.name} - {self.desc} [{self.priority}]"


# Main todo list manager
class TodoList:
    def __init__(self):
        self.tasks = []
        self.file_name = "tasks"
        self.format = "csv"   # csv or json
        self.load_data()

    # Add new task
    def add_task(self, name, desc, priority):
        t = Task(name, desc, priority)
        self.tasks.append(t)
        self.save_data()

    # Remove by index (1-based for user)
    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            removed = self.tasks.pop(index)
            print(f"Removed: {removed.name}")
            self.save_data()
        else:
            print("Invalid number")

    # Show all tasks
    def show_tasks(self):
        if not self.tasks:
            print("No tasks yet")
            return
        for i, t in enumerate(self.tasks, start=1):
            print(f"{i}. {t}")

    # Get full filename with extension
    def get_filename(self):
        if self.format == "csv":
            return self.file_name + ".csv"
        return self.file_name + ".json"

    # Save to CSV
    def save_csv(self, filename):
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "desc", "priority"])
            for t in self.tasks:
                writer.writerow([t.name, t.desc, t.priority])

    # Load from CSV
    def load_csv(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader)  # skip header
                for row in reader:
                    if len(row) >= 3:
                        self.tasks.append(Task(row[0], row[1], row[2]))
        except FileNotFoundError:
            print("No saved file found (csv)")

    # Save to JSON
    def save_json(self, filename):
        data = []
        for t in self.tasks:
            data.append({"name": t.name, "desc": t.desc, "priority": t.priority})
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    # Load from JSON
    def load_json(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    self.tasks.append(Task(item["name"], item["desc"], item["priority"]))
        except FileNotFoundError:
            print("No saved file found (json)")

    # Universal save
    def save_data(self):
        filename = self.get_filename()
        if self.format == "csv":
            self.save_csv(filename)
        else:
            self.save_json(filename)

    # Universal load
    def load_data(self):
        filename = self.get_filename()
        if self.format == "csv":
            self.load_csv(filename)
        else:
            self.load_json(filename)

    # Change format and save immediately
    def change_format(self, new_format):
        if new_format in ["csv", "json"]:
            self.format = new_format
            self.save_data()
            print("Format changed")
        else:
            print("Invalid format")


# Main menu
def main():
    todo = TodoList()

    while True:
        print("\n" + "=" * 50)
        print("TODO LIST".center(50))
        print("1. Add task")
        print("2. Remove task")
        print("3. Show tasks")
        print("4. Change format (current: " + todo.format + ")")
        print("5. Exit")

        try:
            choice = int(input("Choose: "))
        except ValueError:
            print("Enter a number")
            continue

        if choice == 1:
            name = input("Name: ")
            desc = input("Description: ")
            # Simple priority validation (just a loop)
            while True:
                p = input("Priority (low/medium/high): ").lower()
                if p in ["low", "medium", "high"]:
                    break
                print("Invalid, try again")
            todo.add_task(name, desc, p)
            print("Task added")

        elif choice == 2:
            todo.show_tasks()
            if todo.tasks:
                try:
                    idx = int(input("Number to remove: ")) - 1
                    todo.remove_task(idx)
                except ValueError:
                    print("Invalid input")

        elif choice == 3:
            todo.show_tasks()

        elif choice == 4:
            new_f = input("Enter 'csv' or 'json': ").lower()
            todo.change_format(new_f)

        elif choice == 5:
            print("Bye")
            break

        else:
            print("Invalid option")


if __name__ == "__main__":
    main()

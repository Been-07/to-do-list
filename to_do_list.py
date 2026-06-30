# ======================================|
# Author: Benjamin Shojaee              |
# GitHub: https://github.com/Been-07    |
# ORCID: 0009-0005-2756-7140            |
# ======================================|
import csv
import json

class Task:
    def __init__(self, name, explanation, priority):
        self.name = name
        self.explanation = explanation
        self.priority = priority

    def __str__(self):
        return f"{self.name} , {self.explanation} , Priority: {self.priority}"


class ToDoList:
    def __init__(self):
        # task storage
        self.tasks = []

        # default file config
        self.filename_base = "tasks"
        self.storage_format = "csv"

        # load saved tasks if available
        self.load()

    def add_task(self, name, explanation, priority):
        self.tasks.append(Task(name, explanation, priority))

        # save after update
        self.save()

    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            removed = self.tasks.pop(index)
            print(f"removed: {removed.name}")

            # persist changes
            self.save()
        else:
            print("invalid index")

    def show_task(self):
        if not self.tasks:
            print("no tasks found")
            return

        for i, task in enumerate(self.tasks, start=1):
            print(f"{i}- {task}")

    def _get_filename(self):
        if self.storage_format == "csv":
            return self.filename_base + ".csv"
        return self.filename_base + ".json"
    def save_to_csv(self, filename):
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            # table header
            writer.writerow(["name", "explanation", "priority"])

            for task in self.tasks:
                writer.writerow([task.name, task.explanation, task.priority])

    def load_from_csv(self, filename):
        try:
            with open(filename, mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)

                # skip header row
                next(reader)

                for row in reader:
                    if len(row) >= 3:
                        self.tasks.append(Task(row[0], row[1], row[2]))

        except FileNotFoundError:
            print("csv file not found")

    def save_to_json(self, filename):
        data = []

        for task in self.tasks:
            data.append({
                "name": task.name,
                "explanation": task.explanation,
                "priority": task.priority
            })

        with open(filename, mode="w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def load_from_json(self, filename):
        try:
            with open(filename, mode="r", encoding="utf-8") as file:
                data = json.load(file)

                for item in data:
                    self.tasks.append(
                        Task(
                            item["name"],
                            item["explanation"],
                            item["priority"]
                        )
                    )

        except FileNotFoundError:
            print("json file not found")

    def save(self):
        filename = self._get_filename()

        if self.storage_format == "csv":
            self.save_to_csv(filename)
        else:
            self.save_to_json(filename)

    def load(self):
        filename = self._get_filename()

        if self.storage_format == "csv":
            self.load_from_csv(filename)
        else:
            self.load_from_json(filename)

    def change_format(self, new_format):
        if new_format in ["csv", "json"]:
            self.storage_format = new_format
            self.save()
            print("format updated")
        else:
            print("invalid format")

def main():
    todo_list = ToDoList()

    # simple menu loop
    while True:
        print("=" * 60)
        print("TO-DO LIST".center(60))
        print("1. Add task")
        print("2. Remove task")
        print("3. Show tasks")
        print(f"4. Change format ({todo_list.storage_format})")
        print("5. Exit")

        try:
            choice = int(input("Choose option: "))
        except ValueError:
            print("enter a valid number")
            continue

        if choice == 1:
            name = input("task name: ")
            explanation = input("description: ")

            valid_priorities = ["very low", "low", "medium", "high", "very high"]

            while True:
                priority = input("priority: ").strip().lower()
                priority = " ".join(priority.split())

                if priority in valid_priorities:
                    break

                print("invalid priority")

            todo_list.add_task(name, explanation, priority)
            print("task added")

        elif choice == 2:
            todo_list.show_task()

            if todo_list.tasks:
                try:
                    index = int(input("task number to remove: ")) - 1
                    todo_list.remove_task(index)
                except ValueError:
                    print("invalid input")
            else:
                print("nothing to remove")

        elif choice == 3:
            todo_list.show_task()

        elif choice == 4:
            new_format = input("csv or json: ").strip().lower()
            todo_list.change_format(new_format)

        elif choice == 5:
            print("bye")
            break

        else:
            print("invalid option")


if __name__ == "__main__":
    main()

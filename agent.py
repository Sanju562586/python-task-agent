import json
from pathlib import Path


TASKS_FILE = Path(__file__).resolve().with_name("tasks.json")


def load_tasks():
    """Load saved tasks, or start with an empty list for a new project."""
    if not TASKS_FILE.exists():
        return []

    with TASKS_FILE.open("r", encoding="utf-8") as file:
        tasks = json.load(file)

    if not isinstance(tasks, list):
        raise ValueError("The tasks file must contain a JSON list.")
    return tasks


def save_tasks(tasks):
    """Write the current task list to the local JSON file."""
    with TASKS_FILE.open("w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=2)
        file.write("\n")


def add_task(description):
    """Create and save a task, returning the new task record."""
    tasks = load_tasks()
    next_id = max((task["id"] for task in tasks), default=0) + 1
    task = {"id": next_id, "description": description, "completed": False}
    tasks.append(task)
    save_tasks(tasks)
    return task


def list_tasks():
    """Return all saved tasks for the caller to display."""
    return load_tasks()


def complete_task(task_id):
    """Mark a matching task complete, or return None if it does not exist."""
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            save_tasks(tasks)
            return task
    return None


def delete_task(task_id):
    """Remove a matching task, or return None if it does not exist."""
    tasks = load_tasks()
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            deleted_task = tasks.pop(index)
            save_tasks(tasks)
            return deleted_task
    return None


def print_help():
    print("Commands:")
    print("  add <task description>  Add a task")
    print("  list                    List all tasks")
    print("  complete <task id>      Complete a task")
    print("  delete <task id>        Delete a task")
    print("  help                    Show these commands")
    print("  quit                    Exit the program")


def handle_command(command_line):
    """Choose a tool from the command and report the tool's result."""
    command, _, argument = command_line.strip().partition(" ")
    argument = argument.strip()

    # The command word selects the tool; the rest of the line is its input.
    if command == "add":
        if not argument:
            print("Please include a description after 'add'.")
            return True
        task = add_task(argument)
        print(f"Added task #{task['id']}: {task['description']}")
    elif command == "list":
        if argument:
            print("The 'list' command does not take an argument.")
            return True
        tasks = list_tasks()
        if not tasks:
            print("No tasks yet.")
        else:
            print("Current tasks:")
            for task in tasks:
                status = "done" if task["completed"] else "open"
                print(f"- #{task['id']}: {task['description']} [{status}]")
    elif command == "complete":
        try:
            task_id = int(argument)
            if task_id < 1:
                raise ValueError
        except ValueError:
            print("Please provide a valid task ID, for example: complete 1")
            return True

        task = complete_task(task_id)
        if task is None:
            print(f"No task found with ID {task_id}.")
        else:
            print(f"Completed task #{task['id']}: {task['description']}")
    elif command == "delete":
        try:
            task_id = int(argument)
            if task_id < 1:
                raise ValueError
        except ValueError:
            print("Please provide a valid task ID, for example: delete 1")
            return True

        task = delete_task(task_id)
        if task is None:
            print(f"No task found with ID {task_id}.")
        else:
            print(f"Deleted task #{task['id']}: {task['description']}")
    elif command == "help":
        print_help()
    elif command in ("quit", "exit"):
        print("Goodbye!")
        return False
    else:
        print("Unknown command. Type 'help' to see available commands.")

    return True


def main():
    print("Task Management Agent")
    print("Type 'help' to see commands. Type 'quit' to exit.")

    while True:
        try:
            command_line = input("agent> ")
        except EOFError:
            print()
            break

        # Keep prompting unless a recognized exit command asks the loop to stop.
        if not handle_command(command_line):
            break


if __name__ == "__main__":
    main()
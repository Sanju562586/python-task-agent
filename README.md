# python-task-agent

This project is a beginner-friendly Python task management agent. It keeps tasks in a local JSON file and lets you manage them through a terminal command loop.

## Features

- Add a task
- List all tasks
- Mark a task as complete
- Delete a task by ID
- Store tasks in `tasks.json`
- Handle invalid inputs and missing task IDs without crashing
- Uses only Python's standard library

## Run locally

1. Open a terminal in the project folder.
2. Make sure Python 3 is installed.
3. Run:

```bash
python agent.py
```

## Commands

- `add Buy groceries` - add a new task
- `list` - view all tasks
- `complete 1` - mark task 1 as done
- `delete 1` - delete task 1
- `help` - display available commands
- `quit` - exit the program

## Example session

```text
$ python agent.py
Task Management Agent
Type 'help' to see commands. Type 'quit' to exit.
agent> add Buy groceries
Added task #1: Buy groceries
agent> list
Current tasks:
- #1: Buy groceries [open]
agent> complete 1
Completed task #1: Buy groceries
agent> quit
Goodbye!
```

## Notes

- The app stores data in `tasks.json` in the same directory as `agent.py`.
- The logic is intentionally simple and modular so it is easy to learn from and expand.

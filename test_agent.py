import agent
import pytest


@pytest.fixture
def task_file(tmp_path, monkeypatch):
    path = tmp_path / "tasks.json"
    monkeypatch.setattr(agent, "TASKS_FILE", path)
    return path


def test_add_task_creates_task(task_file):
    task = agent.add_task("Buy groceries")

    assert task == {
        "id": 1,
        "description": "Buy groceries",
        "completed": False,
    }
    assert agent.list_tasks() == [task]


def test_add_task_uses_next_available_id(task_file):
    agent.save_tasks(
        [
            {"id": 2, "description": "First task", "completed": False},
            {"id": 7, "description": "Second task", "completed": True},
        ]
    )

    task = agent.add_task("New task")

    assert task["id"] == 8


def test_add_task_starts_incomplete(task_file):
    task = agent.add_task("Finish report")

    assert task["completed"] is False


def test_add_task_adds_multiple_tasks(task_file):
    first_task = agent.add_task("First task")
    second_task = agent.add_task("Second task")

    assert first_task["id"] == 1
    assert second_task["id"] == 2
    assert agent.list_tasks() == [first_task, second_task]

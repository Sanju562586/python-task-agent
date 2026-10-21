import pytest

import agent


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


@pytest.mark.parametrize(
    "invalid_task",
    [
        {},
        {"id": "1"},
        {"id": 1.5},
        {"id": True},
        {"id": 0},
        {"id": -1},
        None,
    ],
)
def test_add_task_rejects_invalid_saved_ids_without_changing_file(
    task_file, invalid_task
):
    agent.save_tasks([invalid_task])
    original_contents = task_file.read_text(encoding="utf-8")

    with pytest.raises(ValueError, match="positive integer ID"):
        agent.add_task("New task")

    assert task_file.read_text(encoding="utf-8") == original_contents


def test_complete_task_updates_and_saves_matching_task(task_file):
    task = agent.add_task("Finish report")

    completed_task = agent.complete_task(task["id"])

    assert completed_task == {
        "id": task["id"],
        "description": "Finish report",
        "completed": True,
    }
    assert agent.list_tasks() == [completed_task]


def test_complete_task_returns_none_for_missing_id(task_file):
    agent.add_task("Keep this task")

    assert agent.complete_task(99) is None
    assert agent.list_tasks()[0]["completed"] is False


def test_delete_task_removes_and_returns_matching_task(task_file):
    task = agent.add_task("Remove this task")

    deleted_task = agent.delete_task(task["id"])

    assert deleted_task == task
    assert agent.list_tasks() == []


def test_delete_task_returns_none_for_missing_id(task_file):
    task = agent.add_task("Keep this task")

    assert agent.delete_task(99) is None
    assert agent.list_tasks() == [task]


@pytest.mark.parametrize(
    ("command", "expected_message"),
    [
        ("complete 0", "Please provide a valid task ID, for example: complete 1"),
        ("delete invalid", "Please provide a valid task ID, for example: delete 1"),
    ],
)
def test_task_commands_report_invalid_ids(command, expected_message, capsys):
    assert agent.handle_command(command) is True
    assert capsys.readouterr().out.strip() == expected_message


def test_load_tasks_reports_malformed_json(task_file):
    task_file.write_text("{invalid json", encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid JSON in tasks file") as error:
        agent.load_tasks()

    assert isinstance(error.value.__cause__, ValueError)

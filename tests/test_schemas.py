import pytest
from pydantic import ValidationError

from schemas.task import TaskCreate, TaskReplace


def test_blank_title_is_rejected():
    with pytest.raises(ValidationError):
        TaskCreate(title="   ")


def test_description_defaults_to_empty():
    task = TaskCreate(title="Estudar")
    assert task.description == ""


def test_replace_requires_description():
    with pytest.raises(ValidationError):
        TaskReplace(title="Estudar")
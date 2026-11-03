class TaskNotFound(Exception):
    def __init__(self, task_id):
        self.task_id = task_id


class TaskService:
    def __init__(self, repository):
        self.repository = repository

    def create(self, user_id, title, description):
        return self.repository.insert(user_id, title, description)

    def list_all(self, user_id):
        return self.repository.list_all(user_id)

    def get(self, user_id, task_id):
        task = self.repository.find_by_id(user_id, task_id)
        if task is None:
            raise TaskNotFound(task_id)
        return task

    def update(self, user_id, task_id, title, description):
        task = self.repository.update(user_id, task_id, title, description)
        if task is None:
            raise TaskNotFound(task_id)
        return task

    def change_status(self, user_id, task_id, status):
        task = self.repository.update_status(user_id, task_id, status)
        if task is None:
            raise TaskNotFound(task_id)
        return task

    def remove(self, user_id, task_id):
        title = self.repository.delete(user_id, task_id)
        if title is None:
            raise TaskNotFound(task_id)
        return title
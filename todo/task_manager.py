from todo.task import Task


class TaskManager:
    def __init__(self) -> None:
        self.task_list: list[Task] = []
        self._current_id = 0

    def get_tasks(self) -> list[Task]:
        return self.task_list

    def add_task(self, task_name: str, is_complete: bool = False) -> None:
        task = Task(id=self._generate_id(), name=task_name, is_complated=is_complete)
        self.task_list.append(task)

    def remove_task(self, task_id: str) -> None:
        self.task_list = [task for task in self.task_list if task.id != task_id]

    def mark_complete(self, task_id: str) -> None:
        self.task_list = [
            task if task.id != task_id else Task(id=task.id, name=task.name, is_complated=True)
            for task in self.task_list
        ]

    def _generate_id(self) -> str:
        self._current_id += 1
        return str(self._current_id)

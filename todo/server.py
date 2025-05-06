from mcp.server.fastmcp import FastMCP

from todo.config import Config
from todo.task import Task
from todo.task_manager import TaskManager

mcp = FastMCP(
    name="Doitr",
    host=Config.Server.HOST,
    port=Config.Server.PORT,
    sse_path=Config.Server.SSE_PATH,
)

manager = TaskManager()
manager.add_task("Eat breakfast", is_complete=True)
manager.add_task("Got to the gym")
manager.add_task("Read a book")


@mcp.tool()
def list_tasks() -> list[Task]:
    """List all tasks"""
    return manager.get_tasks()


@mcp.tool()
def add_task(name: str) -> list[Task]:
    """Add a new task

    Args:
        name (str): Name of task

    Returns:
        list[Task]: The updated list of tasks
    """
    manager.add_task(name)
    return manager.get_tasks()


@mcp.tool()
def remove_task(task_id: str) -> list[Task]:
    """Remove a task by ID

    Args:
        task_id (str): Unique task ID

    Returns:
        list[Task]: The updated list of tasks
    """
    manager.remove_task(task_id)
    return manager.get_tasks()


@mcp.tool()
def complete_task(task_id: str) -> list[Task]:
    """Mark a task as completed

    Args:
        task_id (str): Unique task ID

    Returns:
        list[Task]: The updated list of tasks
    """
    manager.mark_complete(task_id)
    return manager.get_tasks()


if __name__ == "__main__":
    mcp.run(transport=Config.Server.TRANSPORT)

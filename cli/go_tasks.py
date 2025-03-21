import logging
import os
import subprocess
from pathlib import Path

import click
import yaml
from singleton_decorator import singleton

# Track parsed files to avoid circular imports
parsed_files = set()
logger = logging.getLogger(__name__)


@click.group(help="Commands imported from task files")
def tasks():
    """Commands imported from task files"""
    pass


@singleton
class GoTasks:
    def __init__(self):
        self.run_callback = None

    def set_callback(self, callback):
        self.run_callback = callback

    # Recursively load tasks from Taskfile.yml and imported files
    def load_tasks(self, taskfile_path, prefix=""):
        taskfile_path = Path(taskfile_path).resolve()  # Ensure absolute path
        if taskfile_path in parsed_files:
            return {}
        parsed_files.add(taskfile_path)

        if not taskfile_path.exists():
            return {}

        with open(taskfile_path, "r") as f:
            taskfile = yaml.safe_load(f)

        tasks = taskfile.get("tasks", {})

        # Add prefix to task names and include descriptions
        prefixed_tasks = {}
        for task_name, task_def in tasks.items():
            prefixed_name = f"{prefix}{task_name}"
            internal = task_def.get("internal", False)
            import_command = task_def.get("import_command", True)
            if not internal and import_command:
                prefixed_tasks[prefixed_name] = {
                    "desc": task_def.get("desc", f"Run the {prefixed_name} task."),
                    "cmds": task_def.get("cmds", []),
                }
        tasks = prefixed_tasks

        # Handle imports
        includes = taskfile.get("includes", {})
        if isinstance(includes, dict):
            for import_name, included_taskfile in includes.items():
                included_path = os.path.join(str(taskfile_path.parent), included_taskfile["taskfile"])
                included_tasks = self.load_tasks(included_path, prefix=f"{import_name}:")
                tasks.update(included_tasks)

        return tasks

    def is_valid_task_name(self, task_name):
        # Check if the task_name is a valid identifier or contains only alphanumeric characters and colons
        if task_name.isidentifier() or all(c.isalnum() or c in ":_- " for c in task_name):
            return True
        return False

    def generate_go_tasks(self):
        taskfile_path = "Taskfile.yml"  # Path to the main Taskfile.yml
        loaded_tasks = self.load_tasks(taskfile_path)

        for task_name, task_def in loaded_tasks.items():

            @tasks.command(name=task_name, help=task_def["desc"])
            def task_command(task_name=task_name):  # Use a default argument to capture the current task_name
                """Run a go-task task."""
                self.run_task(task_name)

    # Dynamic command for running go-task
    def run_task(self, task_name):
        # Sanitize task_name to allow only safe characters (e.g., alphanumeric and underscores)
        if not self.is_valid_task_name(task_name):
            click.echo(f"Invalid task name: '{task_name}'", err=True)
            return
        try:
            env = os.environ.copy()
            subprocess.run(["task", task_name], env=env, check=True)
            self.run_callback(task_name)

        except subprocess.CalledProcessError as e:
            click.echo(f"Error running task '{task_name}': {e}", err=True)
        except FileNotFoundError:
            click.echo("go-task is not installed or not in PATH.", err=True)

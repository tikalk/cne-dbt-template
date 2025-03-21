import unittest
from unittest import mock

from cli.go_tasks import GoTasks


class TestGoTasks(unittest.TestCase):

    def setUp(self):
        self.go_tasks = GoTasks()

    def test_initialization(self):
        self.assertIsNone(self.go_tasks.run_callback)

    def test_set_callback(self):
        def dummy_callback(task_name):
            pass

        self.go_tasks.set_callback(dummy_callback)
        self.assertEqual(self.go_tasks.run_callback, dummy_callback)

    @mock.patch("cli.go_tasks.yaml.safe_load")
    @mock.patch("cli.go_tasks.open", mock.mock_open(read_data="tasks: {}"))
    @mock.patch("cli.go_tasks.Path.exists", return_value=True)
    def test_load_tasks(self, mock_exists, mock_safe_load):
        mock_safe_load.return_value = {"tasks": {"task1": {"desc": "Test task 1", "cmds": ["echo 'Task 1'"]}}}
        tasks = self.go_tasks.load_tasks("Taskfile.yml")
        self.assertIn("task1", tasks)
        self.assertEqual(tasks["task1"]["desc"], "Test task 1")

    def test_is_valid_task_name(self):
        self.assertTrue(self.go_tasks.is_valid_task_name("valid_task_name"))
        self.assertFalse(self.go_tasks.is_valid_task_name("invalid task name!"))

    @mock.patch("cli.go_tasks.subprocess.run")
    @mock.patch("cli.go_tasks.os.environ.copy", return_value={})
    def test_run_task(self, mock_env_copy, mock_subprocess_run):
        def dummy_callback(task_name):
            pass

        self.go_tasks.set_callback(dummy_callback)
        self.go_tasks.run_task("valid_task_name")
        mock_subprocess_run.assert_called_with(["task", "valid_task_name"], env={}, check=True)


if __name__ == "__main__":
    unittest.main()

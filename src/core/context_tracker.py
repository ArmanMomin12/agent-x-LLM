# src/core/context_tracker.py

class ContextTracker:
    """
    Tracks the context of the current interaction including user goals, state, and history.
    """

    def __init__(self):
        self.context = {
            "current_goal": None,
            "task_list": [],
            "history": [],
            "variables": {}
        }

    def set_goal(self, goal: str):
        """Set the main user goal for the session."""
        self.context["current_goal"] = goal
        self.log_event("Goal set", goal)

    def load_context(self, data: dict):
        """Load context from saved memory."""
        self.context["current_goal"] = data.get("current_goal", None)
        self.context["task_list"] = data.get("task_list", [])
        self.context["history"] = data.get("history", [])
        self.context["variables"] = data.get("variables", {})

    def add_task(self, task: str):
        """Add a task to the current task list."""
        self.context["task_list"].append(task)
        self.log_event("Task added", task)

    def complete_task(self, task: str):
        """Mark a task as completed."""
        if task in self.context["task_list"]:
            self.context["task_list"].remove(task)
            self.log_event("Task completed", task)

    def update_variable(self, key: str, value):
        """Update or set a variable in the context."""
        self.context["variables"][key] = value
        self.log_event("Variable updated", f"{key} = {value}")

    def get_variable(self, key: str):
        """Retrieve a stored variable value."""
        return self.context["variables"].get(key, None)

    def get_context(self):
        """Return the current context dictionary."""
        return self.context

    def log_event(self, event_type: str, detail: str):
        """Add an entry to the history log."""
        self.context["history"].append({
            "event": event_type,
            "detail": detail
        })

    def reset(self):
        """Reset the entire context (new session or major shift)."""
        self.__init__()



import json
from datetime import datetime
import os 
import sys
# Ensure the parent directory is in sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)


def remember(self, task_name, task_details):
    """Store a task in memory with its details."""
    task_id = len(self.memory_store) + 1
    self.memory_store[task_id] = {
        "task_name": task_name,
        "task_details": task_details,
        "created_at": datetime.now().isoformat()
    }
    return {"status": "success", "message": f"Task '{task_name}' remembered with ID {task_id}"}
def recall(self, task_name=None, task_id=None):
    """Recall task details by task name or task ID."""
    if task_id:
        task = self.memory_store.get(task_id)
        if task:
            return {"status": "success", "task": task}
        else:
            return {"status": "error", "message": "Task ID not found"}
    
    if task_name:
        tasks = [task for task in self.memory_store.values() if task_name in task['task_name']]
        if tasks:
            return {"status": "success", "tasks": tasks}
        else:
            return {"status": "error", "message": "No tasks found with the given name"}
    return {"status": "error", "message": "No task name or ID provided for recall"}
def remind_me(self, task_name):
    """Set a reminder for a task by name."""
    tasks = [task for task in self.memory_store.values() if task_name in task['task_name']]
    if tasks:
        # For simplicity, we just return the task(s). In a real scenario, you could schedule reminders.
        return {"status": "success", "tasks": tasks}
    else:
        return {"status": "error", "message": "No tasks found to remind"}

# Example Usage
if __name__ == "__main__":
    
    # Remembering a task
    response = remember("buy groceries", {"items": ["milk", "bread", "eggs"], "due": "2024-06-02"})
    print(json.dumps(response, indent=2))

    # Recalling a task by name
    response = recall(task_name="buy groceries")
    print(json.dumps(response, indent=2))

    # Recalling a task by ID
    response = recall(task_id=1)
    print(json.dumps(response, indent=2))

    # Setting a reminder for a task
    response = remind_me("buy groceries")
    print(json.dumps(response, indent=2))

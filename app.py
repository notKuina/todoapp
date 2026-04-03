from flask import Flask, render_template, request, redirect, url_for
import json
import os
from collections import defaultdict
from datetime import datetime

app = Flask(__name__)
FILE_NAME = "tasks.json"

# Load tasks from JSON
def load_tasks():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w") as f:
            json.dump([], f)
    with open(FILE_NAME, "r") as f:
        return json.load(f)

# Save tasks to JSON
def save_tasks(tasks):
    with open(FILE_NAME, "w") as f:
        json.dump(tasks, f)

@app.route("/", methods=["GET", "POST"])
def index():
    tasks = load_tasks()

    if request.method == "POST":
        # Add task
        if "add" in request.form:
            title = request.form.get("task")
            task_date = request.form.get("task_date")
            if title and task_date:
                tasks.append({
                    "title": title,
                    "done": False,
                    "date": task_date
                })
                save_tasks(tasks)

        # Mark done
        elif "done" in request.form:
            index = int(request.form.get("done"))
            tasks[index]["done"] = not tasks[index]["done"]
            save_tasks(tasks)

        # Delete task
        elif "delete" in request.form:
            index = int(request.form.get("delete"))
            tasks.pop(index)
            save_tasks(tasks)

        # Edit task
        elif "edit" in request.form:
            index = int(request.form.get("edit_index"))
            new_title = request.form.get("edit_title")
            if new_title:
                tasks[index]["title"] = new_title
                save_tasks(tasks)

        return redirect(url_for("index"))

    # Group tasks by date
    tasks_by_date = defaultdict(list)
    for idx, task in enumerate(tasks):
        task["index"] = idx  # store original index for buttons
        # Use task["date"] if exists, otherwise today
        task_date = task.get("date", datetime.today().strftime("%Y-%m-%d"))
        task["date"] = task_date  # ensure it exists for saving later
        tasks_by_date[task_date].append(task)

    sorted_dates = sorted(tasks_by_date.keys())

    today = datetime.today().strftime("%Y-%m-%d")

    return render_template(
        "index.html",
        tasks_by_date=tasks_by_date,
        sorted_dates=sorted_dates,
        today=today,
        request=request
    )

if __name__ == "__main__":
    app.run(debug=True)
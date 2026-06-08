import json
import uuid
import os

from datetime import datetime

from events import event_bus

# =========================================
# CONFIG
# =========================================

TASKS_FILE = "tasks.json"

# =========================================
# TASK MANAGER
# =========================================

class TaskManager:

    def __init__(self):

        self.tasks = []

        self.load()

    # =====================================
    # LOAD
    # =====================================

    def load(self):

        if not os.path.exists(
            TASKS_FILE
        ):

            self.tasks = []

            return

        try:

            with open(
                TASKS_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                self.tasks = json.load(f)

        except:

            self.tasks = []

    # =====================================
    # SAVE
    # =====================================

    def save(self):

        with open(
            TASKS_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(

                self.tasks,

                f,

                indent=2,

                ensure_ascii=False
            )

    # =====================================
    # ADD TASK
    # =====================================

    def add_task(
        self,
        task_text,
        priority=1
    ):

        task = {

            "id":
                str(uuid.uuid4()),

            "created":
                str(datetime.now()),

            "status":
                "pending",

            "retries":
                0,

            "priority":
                priority,

            "task":
                task_text
        }

        self.tasks.append(
            task
        )

        self.save()

        event_bus.emit(

            "task_added",

            task
        )

        return task

    # =====================================
    # GET NEXT TASK
    # =====================================

    def get_next_task(self):

        pending = [

            t for t in self.tasks

            if t["status"] == "pending"
        ]

        if not pending:

            return None

        pending.sort(

            key=lambda x:
            x["priority"],

            reverse=True
        )

        task = pending[0]

        task["status"] = "running"

        self.save()

        return task

    # =====================================
    # COMPLETE
    # =====================================

    def complete_task(
        self,
        task_id
    ):

        for task in self.tasks:

            if task["id"] == task_id:

                task["status"] = (
                    "completed"
                )

                self.save()

                event_bus.emit(

                    "task_completed",

                    task
                )

                return

    # =====================================
    # FAIL
    # =====================================

    def fail_task(
        self,
        task_id
    ):

        for task in self.tasks:

            if task["id"] == task_id:

                task["status"] = (
                    "failed"
                )

                task["retries"] += 1

                self.save()

                event_bus.emit(

                    "task_failed",

                    task
                )

                return

    # =====================================
    # COUNT
    # =====================================

    def count(self):

        return len(

            [

                t for t in self.tasks

                if t["status"]
                ==
                "pending"
            ]
        )

    # =====================================
    # LIST
    # =====================================

    def list_tasks(self):

        return self.tasks

# =========================================
# GLOBAL INSTANCE
# =========================================

task_manager = TaskManager()
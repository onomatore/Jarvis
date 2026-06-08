import json
import os

from datetime import datetime

from events import event_bus

from config import (
    MEMORY_FILE,
    MEMORY_LIMIT,
    MEMORY_SUMMARY_LIMIT
)

IGNORE_MEMORY_PATTERNS = [

    "LLM API ERROR",
    "OPENROUTER ERROR",
    "HTTP ERROR",
    "RATE LIMIT",
    "403",
    "429",
    "500",
    "TRACEBACK",
    "EXCEPTION",
    "MODEL FAIL",
    "MODEL EXCEPTION",
    "НИ ОДНА МОДЕЛЬ НЕДОСТУПНА"
]


class Memory:

    def __init__(self):

        self.memories = []

        self.load()

        self.cleanup_memory()

    # =====================================
    # FILTER
    # =====================================

    def should_store(
        self,
        text
    ):

        if not text:
            return False

        text_upper = str(
            text
        ).upper()

        for pattern in IGNORE_MEMORY_PATTERNS:

            if pattern in text_upper:

                return False

        return True

    # =====================================
    # LOAD
    # =====================================

    def load(self):

        if not os.path.exists(
            MEMORY_FILE
        ):

            self.memories = []

            return

        try:

            with open(
                MEMORY_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                self.memories = (
                    json.load(f)
                )

        except Exception:

            self.memories = []

    # =====================================
    # SAVE
    # =====================================

    def save(self):

        try:

            with open(
                MEMORY_FILE,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    self.memories,
                    f,
                    indent=2,
                    ensure_ascii=False
                )

        except Exception as e:

            print(
                "[MEMORY SAVE ERROR]",
                e
            )

    # =====================================
    # CLEANUP
    # =====================================

    def cleanup_memory(self):

        cleaned = []

        for item in self.memories:

            content = item.get(
                "content",
                ""
            )

            if self.should_store(
                content
            ):

                cleaned.append(
                    item
                )

        self.memories = cleaned

        self.save()

    # =====================================
    # ADD
    # =====================================

    def add(
        self,
        role,
        content,
        user_id=None,
        username=None,
        metadata=None
    ):

        if not self.should_store(
            content
        ):
            return

        entry = {

            "time":
                str(datetime.now()),

            "role":
                role,

            "user_id":
                user_id,

            "username":
                username,

            "content":
                content,

            "metadata":
                metadata or {}
        }

        self.memories.append(
            entry
        )

        if len(
            self.memories
        ) > MEMORY_LIMIT:

            self.memories = (
                self.memories[
                    -MEMORY_LIMIT:
                ]
            )

        self.save()

        event_bus.emit(

            "memory_added",

            {
                "role": role,
                "user_id": user_id,
                "username": username,
                "content": content
            }
        )

    # =====================================
    # RECENT
    # =====================================

    def recent(
        self,
        limit=10
    ):

        return self.memories[
            -limit:
        ]

    # =====================================
    # USER RECENT
    # =====================================

    def recent_user(
        self,
        user_id,
        limit=10
    ):

        result = []

        for item in self.memories:

            if item.get(
                "user_id"
            ) == user_id:

                result.append(
                    item
                )

        return result[
            -limit:
        ]

    # =====================================
    # BUILD CONTEXT
    # =====================================

    def build_context(
        self,
        user_id=None
    ):

        if user_id:

            memories = (
                self.recent_user(
                    user_id,
                    MEMORY_SUMMARY_LIMIT
                )
            )

        else:

            memories = (
                self.recent(
                    MEMORY_SUMMARY_LIMIT
                )
            )

        lines = []

        for item in memories:

            role = item.get(
                "role",
                "unknown"
            )

            username = item.get(
                "username",
                "unknown"
            )

            content = item.get(
                "content",
                ""
            )

            lines.append(

                f"{role}"
                f"[{username}]"
                f": {content}"
            )

        return "\n".join(
            lines
        )

    # =====================================
    # SEARCH
    # =====================================

    def search(
        self,
        query,
        user_id=None
    ):

        query = query.lower()

        results = []

        for memory in self.memories:

            if user_id:

                if memory.get(
                    "user_id"
                ) != user_id:

                    continue

            content = (
                memory.get(
                    "content",
                    ""
                ).lower()
            )

            if query in content:

                results.append(
                    memory
                )

        return results[-20:]

    # =====================================
    # USER FACTS
    # =====================================

    def get_user_facts(
        self,
        user_id
    ):

        facts = []

        for item in self.memories:

            if item.get(
                "user_id"
            ) != user_id:

                continue

            facts.append(
                item.get(
                    "content",
                    ""
                )
            )

        return facts[-30:]

    # =====================================
    # CLEAR
    # =====================================

    def clear(self):

        self.memories = []

        self.save()

    # =====================================
    # STATS
    # =====================================

    def stats(self):

        users = set()

        for item in self.memories:

            uid = item.get(
                "user_id"
            )

            if uid:

                users.add(uid)

        return {

            "count":
                len(
                    self.memories
                ),

            "users":
                len(
                    users
                ),

            "file":
                MEMORY_FILE
        }


memory = Memory()
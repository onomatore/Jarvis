import json
import os

from config import USER_MEMORY_FILE


class UserMemory:

    def __init__(self):

        self.data = {}

        self.load()

    # ==========================
    # LOAD
    # ==========================

    def load(self):

        if not os.path.exists(
            USER_MEMORY_FILE
        ):

            self.data = {}

            return

        try:

            with open(
                USER_MEMORY_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                self.data = json.load(f)

        except:

            self.data = {}

    # ==========================
    # SAVE
    # ==========================

    def save(self):

        with open(
            USER_MEMORY_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(

                self.data,

                f,

                indent=2,

                ensure_ascii=False
            )

    # ==========================
    # ENSURE USER
    # ==========================

    def ensure_user(
        self,
        user_id,
        username
    ):

        if user_id not in self.data:

            self.data[user_id] = {

                "username":
                    username,

                "facts": [],

                "preferences": [],

                "goals": []
            }

    # ==========================
    # FACTS
    # ==========================

    def add_fact(
        self,
        user_id,
        username,
        fact
    ):

        self.ensure_user(
            user_id,
            username
        )

        if fact not in (
            self.data[user_id]
            ["facts"]
        ):

            self.data[user_id][
                "facts"
            ].append(fact)

            self.save()

    # ==========================
    # GET FACTS
    # ==========================

    def get_facts(
        self,
        user_id
    ):

        if user_id not in self.data:

            return []

        return self.data[
            user_id
        ]["facts"]

    # ==========================
    # USER PROFILE
    # ==========================

    def get_profile(
        self,
        user_id
    ):

        return self.data.get(
            user_id,
            {}
        )


user_memory = UserMemory()
import json
import requests
import time

from config import (
    OPENROUTER_API_KEY,
    OPENROUTER_URL,
    MODELS_NAME,
    SYSTEM_PROMPT,
    DEBUG
)

# =========================================
# LLM CLASS
# =========================================

class LLM:

    def __init__(self):

        self.model = MODELS_NAME

    #ERROR
    def is_error_response(
            self,
            text
    ):

        if not text:
            return True

        text = text.upper()

        patterns = [

            "LLM API ERROR",

            "OPENROUTER ERROR",

            "RATE LIMIT",

            "403",

            "429",

            "500",

            "TRACEBACK",

            "EXCEPTION"
        ]

        for p in patterns:

            if p in text:
                return True

        return False

    # =====================================
    # BUILD MESSAGES
    # =====================================

    def build_messages(
        self,
        memory_context,
        user_input
    ):

        messages = [

            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        # MEMORY CONTEXT

        if memory_context:

            messages.append({

                "role": "system",

                "content":
                    f"Memory:\n"
                    f"{memory_context}"
            })

        # USER MESSAGE

        messages.append({

            "role": "user",

            "content": user_input
        })

        return messages

    # =====================================
    # CALL MODEL
    # =====================================

    def generate(
            self,
            memory_context,
            user_input
    ):

        messages = self.build_messages(
            memory_context,
            user_input
        )

        if DEBUG:
            print(
                "\n===== PROMPT =====\n"
            )

            print(messages)

            print(
                "\n==================\n"
            )

        for model in self.model:

            try:

                response = requests.post(

                    OPENROUTER_URL,

                    headers={

                        "Authorization":
                            f"Bearer {OPENROUTER_API_KEY}",

                        "Content-Type":
                            "application/json"
                    },

                    json={

                        "model": model,

                        "messages": messages
                    },

                    timeout=60
                )

                if response.status_code != 200:
                    print(
                        "\n[MODEL FAIL]",
                        model,
                        response.status_code
                    )

                    print(
                        response.text
                    )

                    continue

                data = response.json()

                if DEBUG:
                    print(
                        f"\n[MODEL] {model}"
                    )

                    print(data)

                if "error" in data:
                    print(

                        f"[OPENROUTER ERROR] "
                        f"{data['error']}"
                    )

                    continue

                if "choices" not in data:
                    continue

                content = (

                    data["choices"][0]
                    ["message"]
                    ["content"]
                )

                if not content:
                    continue

                return content

            except Exception as e:

                print(

                    f"[MODEL EXCEPTION] "
                    f"{model}: {e}"
                )

                continue

        return (
            "Извините, сейчас ни одна "
            "модель недоступна."
        )

    # =====================================
    # TRY PARSE TOOL
    # =====================================

    def parse_tool_call(
        self,
        text
    ):

        text = text.strip()

        # MUST START WITH JSON

        if not text.startswith("{"):
            return None

        try:

            data = json.loads(text)

            if (
                "tool" in data
                and
                "args" in data
            ):

                return data

        except:
            return None

        return None

# =========================================
# GLOBAL INSTANCE
# =========================================

llm = LLM()
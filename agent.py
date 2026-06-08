import json

from llm import llm

from memory import memory

from events import event_bus

from tools import (
    execute_tool,
    list_tools
)
from planner import planner

from task_manager import task_manager

# =========================================
# AGENT CLASS
# =========================================



class Agent:

    def __init__(self):

        self.task_manager = task_manager

        self.memory = memory

    # =====================================
    # BUILD TOOL CONTEXT
    # =====================================

    def build_tools_context(self):

        tools = list_tools()

        lines = []

        for tool in tools:

            lines.append(

                f"- {tool['name']}: "
                f"{tool['description']}"
            )

        return "\n".join(lines)

    # =====================================
    # HANDLE INPUT
    # =====================================

    def handle_input(
            self,
            user_input,
            user_id=None,
            username=None,
            tool_call=None):

        # SAVE USER MESSAGE
        event_bus.emit(

            "user_message",

            user_input
        )

        memory.add(
            role="user",
            content=user_input,
            user_id=user_id,
            username=username
        )

        # BUILD MEMORY CONTEXT

        memory_context = (
            memory.build_context(
                user_id=user_id)
        )

        # BUILD TOOLS CONTEXT

        tools_context = (
            self.build_tools_context()
        )

        # FINAL INPUT

        final_input = (

            f"Available tools:\n"
            f"{tools_context}\n\n"

            f"User request:\n"
            f"{user_input}"
        )

        # planner

        plan_result = planner.run(
            memory_context,
            final_input
        )

        response = (
            plan_result.get(
                "response",
                ""
            )
        )

        if not response:
            response = (
                "Не удалось получить ответ."
            )


        # =================================
        # TOOL EXECUTION
        # =================================

        if tool_call:

            tool_name = (
                tool_call["tool"]
            )

            tool_args = (
                tool_call["args"]
            )

            # SAVE TOOL CALL

            memory.add(
                role="assistant",
                content=(
                    f"[TOOL CALL] "
                    f"{tool_name} "
                    f"{tool_args}"
                ),
                user_id=user_id,
                username="Jarvis"
            )

            # EXECUTE TOOL

            tool_result = execute_tool(
                tool_name,
                tool_args
            )

            # SAVE RESULT

            memory.add(
                role="tool",
                content=str(tool_result),
                user_id=user_id,
                username="Jarvis"
            )

            # FINAL RESPONSE GENERATION

            final_prompt = (

                f"User request:\n"
                f"{user_input}\n\n"

                f"Tool used:\n"
                f"{tool_name}\n\n"

                f"Tool result:\n"
                f"{tool_result}\n\n"

                f"Now explain result "
                f"to user naturally."
            )

            final_response = llm.generate(
                memory.build_context(
                    user_id=user_id
                ),
                final_prompt
            )

            # SAVE FINAL RESPONSE

            memory.add(
                role="assistant",
                content=final_response,
                user_id=user_id,
                username="Jarvis"
            )

            return final_response


        # =================================
        # NORMAL RESPONSE
        # =================================

        event_bus.emit(

            "assistant_response",

            response
        )

        memory.add(
            role="assistant",
            content=response,
            user_id=user_id,
            username="Jarvis"
        )

        return response


    # =====================================
    # AUTONOMOUS TICK
    # =====================================

    def tick(self):

        task = self.task_manager.get_next_task()

        if not task:
            return

        try:

            result = self.handle_input(
                user_input=task["task"],
                user_id="system",
                username="TaskManager"
            )

            self.task_manager.complete_task(
                task["id"]
            )

            print(
                f"[TASK DONE] {task['task']}"
            )

        except Exception as e:

            print(
                f"[TASK ERROR] {e}"
            )

            self.task_manager.fail_task(
                task["id"]
            )

    # =====================================
    # ADD TASK
    # =====================================

    def add_task(
            self,
            task
    ):

        return self.task_manager.add_task(
            task
        )
    # =====================================
    # TASK COUNT
    # =====================================

    def task_count(self):

        return self.task_manager.count()
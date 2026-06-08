from llm import llm

from tools import (
    execute_tool
)

# =========================================
# PLANNER
# =========================================

class Planner:

    def __init__(self):

        self.max_steps = 5

    # =====================================
    # RUN TASK
    # =====================================

    def run(
        self,
        memory_context,
        user_input
    ):

        current_input = user_input

        steps = []

        for step in range(
            self.max_steps
        ):

            # =============================
            # BUILD PROMPT
            # =============================

            prompt = f"""

You are autonomous AI agent.

You can:
- answer normally
- use tools
- analyze tool results

Current task:
{current_input}

Previous steps:
{steps}

If tool needed:
respond ONLY JSON:

{{
  "tool": "...",
  "args": {{}}
}}

If task completed:
respond normally.

"""

            # =============================
            # LLM
            # =============================

            response = llm.generate(

                memory_context,

                prompt
            )

            # =============================
            # TOOL CALL?
            # =============================

            tool_call = (
                llm.parse_tool_call(
                    response
                )
            )

            # =============================
            # NORMAL RESPONSE
            # =============================

            if not tool_call:

                return {

                    "response":
                        response,

                    "steps":
                        steps
                }

            # =============================
            # EXECUTE TOOL
            # =============================

            tool_name = (
                tool_call["tool"]
            )

            tool_args = (
                tool_call["args"]
            )

            tool_result = execute_tool(
                tool_name,
                tool_args
            )

            if not tool_result:
                tool_result = (
                    "Tool returned no result."
                )

            # SAVE STEP

            step_data = {

                "tool":
                    tool_name,

                "args":
                    tool_args,

                "result":
                    str(tool_result)
            }

            steps.append(step_data)

            if len(steps) >= 2:

                last = steps[-1]
                prev = steps[-2]

                if (
                        last["tool"] ==
                        prev["tool"]
                ):
                    return {

                        "response":
                            "Planner stopped: repeated tool loop.",

                        "steps":
                            steps
                    }

            # NEXT ITERATION INPUT

            current_input = f"""

Original task:
{user_input}

Tool used:
{tool_name}

Tool result:
{tool_result}

Decide next step.

"""

        # =================================
        # LOOP LIMIT
        # =================================

        return {

            "response":
                "Task stopped: max steps reached.",

            "steps":
                steps
        }

# =========================================
# GLOBAL INSTANCE
# =========================================

planner = Planner()
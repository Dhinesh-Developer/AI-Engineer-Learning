
import json
import ollama
from config import (
    MODEL_NAME,
    MAX_AGENT_STEPS
)
from tools import TOOL_FUNCTIONS


SYSTEM_PROMPT = """
You are a local personal AI agent.

You have access to tools that allow you to:

1. Calculate mathematical expressions.
2. Save notes.
3. List saved notes.
4. Search saved notes.
5. Get the current date and time.

IMPORTANT RULES:

- Use the calculator tool for calculations.
- Do not guess mathematical results when the calculator
  can be used.
- Use the note tools when the user asks you to remember,
  save, store, list, or search a note.
- Use the current_time tool when the user asks for the
  current date or time.
- Do not claim that a tool was executed unless you actually
  receive its result.
- After receiving tool results, provide a clear final answer.
- Keep responses concise but useful.
"""


TOOLS = [

    {
        "type": "function",

        "function": {

            "name": "calculator",

            "description":
            "Calculate a mathematical expression safely.",

            "parameters": {

                "type": "object",

                "properties": {

                    "expression": {

                        "type": "string",

                        "description":
                        "A mathematical expression such as 25 * 48."

                    }

                },

                "required": [
                    "expression"
                ]
            }
        }
    },

    {
        "type": "function",

        "function": {

            "name": "save_note",

            "description":
            "Save a note into the user's persistent notes database.",

            "parameters": {

                "type": "object",

                "properties": {

                    "note": {

                        "type": "string",

                        "description":
                        "The note that should be saved."

                    }

                },

                "required": [
                    "note"
                ]
            }
        }
    },

    {
        "type": "function",

        "function": {

            "name": "list_notes",

            "description":
            "Return all notes stored in the database.",

            "parameters": {

                "type": "object",

                "properties": {},

                "required": []
            }
        }
    },

    {
        "type": "function",

        "function": {

            "name": "search_notes",

            "description":
            "Search stored notes using a keyword.",

            "parameters": {

                "type": "object",

                "properties": {

                    "keyword": {

                        "type": "string",

                        "description":
                        "Keyword to search for in saved notes."

                    }

                },

                "required": [
                    "keyword"
                ]
            }
        }
    },

    {
        "type": "function",

        "function": {

            "name": "current_time",

            "description":
            "Get the current local date and time.",

            "parameters": {

                "type": "object",

                "properties": {},

                "required": []
            }
        }
    }
]

def execute_tool(tool_name, arguments):
    """
    Execute a tool selected by the LLM.
    """
    if tool_name not in TOOL_FUNCTIONS:
        return {
            "success": False,
            "error":
            f"Unknown tool: {tool_name}"
        }
    tool_function = TOOL_FUNCTIONS[tool_name]

    try:
        result = tool_function(
            **arguments
        )

        return result
    except Exception as error:
        return {
            "success": False,
            "error": str(error)
        }


class PersonalAgent:
    def __init__(self):
        self.model = MODEL_NAME
        self.messages = [
            {"role": "system","content": SYSTEM_PROMPT}
        ]
    def run(self, user_input):
        self.messages.append(
            {"role": "user","content": user_input}
        )
        execution_trace = []
        for step in range(MAX_AGENT_STEPS):
            response = ollama.chat(
                model=self.model,
                messages=self.messages,
                tools=TOOLS
            )
            assistant_message = response["message"]
            self.messages.append(assistant_message)
            tool_calls = assistant_message.get("tool_calls")

            if not tool_calls:
                final_answer = assistant_message.get(
                    "content", "")
                return (
                    final_answer,
                    execution_trace
                )

            for tool_call in tool_calls:
                function_data = (
                    tool_call["function"]
                )
                tool_name = function_data["name"]
                raw_arguments = (
                    function_data.get(
                        "arguments",
                        {}
                    )
                )

                # Ollama can return arguments as a dict.
                # Some model/tool combinations may return
                # JSON text, so handle both.

                if isinstance(
                    raw_arguments,
                    str
                ):
                    try:
                        arguments = json.loads(
                            raw_arguments
                        )
                    except json.JSONDecodeError:
                        arguments = {}

                else:
                    arguments = raw_arguments
                execution_trace.append(
                    {
                        "step": step + 1,
                        "tool": tool_name,
                        "arguments": arguments
                    }
                )

                result = execute_tool(
                    tool_name,
                    arguments
                )

                execution_trace[-1][
                    "result"
                ] = result

                self.messages.append(
                    {
                        "role": "tool",
                        "content": json.dumps(
                            result
                        )
                    }
                )
        return (
            "I could not complete the task within "
            "the allowed number of steps.",
            execution_trace
        )


    def reset(self):
        self.messages = [

            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }

        ]
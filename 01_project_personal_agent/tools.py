# tools.py

import ast
import operator
from datetime import datetime

from database import (
    save_note,
    get_all_notes,
    search_notes
)


# 1. SAFE CALCULATOR
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _evaluate_node(node):
    """
    Recursively evaluate a mathematical AST node.
    """

    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(
            "Only numbers are allowed."
        )

    if isinstance(node, ast.UnaryOp):
        operator_function = _ALLOWED_OPERATORS.get(
            type(node.op)
        )
        if operator_function is None:
            raise ValueError(
                "Unsupported unary operator."
            )
        return operator_function(
            _evaluate_node(node.operand)
        )

    if isinstance(node, ast.BinOp):
        operator_function = _ALLOWED_OPERATORS.get(
            type(node.op)
        )
        if operator_function is None:

            raise ValueError(
                "Unsupported operator."
            )

        left = _evaluate_node(node.left)
        right = _evaluate_node(node.right)
        return operator_function(
            left,
            right
        )

    raise ValueError(
        "Invalid mathematical expression."
    )


def calculator(expression):
    """
    Safely calculate a mathematical expression.

    Example:
        calculator("25 * 48")
    """

    try:
        tree = ast.parse(
            expression,
            mode="eval"
        )
        result = _evaluate_node(
            tree.body
        )
        return {
            "success": True,
            "expression": expression,
            "result": result
        }
    except Exception as error:

        return {
            "success": False,
            "error": str(error)
        }



# 2. SAVE NOTE

def save_note_tool(note):
    """
    Save a note into SQLite.
    """

    try:
        result = save_note(note)
        return result
    except Exception as error:
        return {
            "success": False,
            "error": str(error)
        }



# 3. LIST NOTES

def list_notes_tool():
    """
    Return all saved notes.
    """
    try:
        notes = get_all_notes()
        formatted_notes = []
        for note in notes:
            formatted_notes.append(
                {
                    "id": note[0],
                    "note": note[1],
                    "created_at": note[2]
                }
            )
        return {
            "success": True,
            "notes": formatted_notes
        }
    except Exception as error:
        return {
            "success": False,
            "error": str(error)
        }


# 4. SEARCH NOTES

def search_notes_tool(keyword):
    """
    Search saved notes.
    """
    try:
        notes = search_notes(keyword)
        formatted_notes = []
        for note in notes:
            formatted_notes.append(
                {
                    "id": note[0],
                    "note": note[1],
                    "created_at": note[2]
                }
            )
        return {
            "success": True,
            "keyword": keyword,
            "notes": formatted_notes
        }

    except Exception as error:

        return {
            "success": False,
            "error": str(error)
        }


# 5. CURRENT TIME

def current_time():
    """
    Return the current local date and time.
    """

    now = datetime.now()

    return {
        "success": True,
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "datetime": now.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    }



# TOOL REGISTRY

TOOL_FUNCTIONS = {
    "calculator": calculator,
    "save_note": save_note_tool,
    "list_notes": list_notes_tool,
    "search_notes": search_notes_tool,
    "current_time": current_time
}
import re
import pandas as pd
from typing import TypedDict, Optional
from langgraph.graph import StateGraph, START, END
from database import get_schema, execute_sql
from llm import llm

class AgentState(TypedDict):
    question: str
    schema: str
    sql_query: str
    error: Optional[str]
    dataframe: Optional[pd.DataFrame]
    insights: str
    attempts: int

def get_database_schema(state: AgentState):
    schema = get_schema()
    return {"schema": schema}

def generate_sql(state: AgentState):
    question = state["question"]
    schema = state["schema"]

    prompt = f"""
You are an expert SQL data analyst.
You are working with SQLite.
DATABASE SCHEMA: {schema}
USER QUESTION : {question}
Your task is to generate ONE valid SQLite SQL query.

Rules:
1. Return ONLY the SQL query.
2. Do not use markdown.
3. Do not explain the query.
4. Only use tables and columns from the schema.
5. Use SQLite-compatible SQL.
6. Never modify the database. 
7. Never use INSERT, UPDATE, DELETE, DROP, ALTER, CREATE. 
8. Only generate SELECT queries.
"""
    response = llm.invoke(prompt)

    # Convert list content to string if necessary
    if isinstance(response.content, list):
        content_text = "".join(
            part.get("text", "") if isinstance(part, dict) else str(part)
            for part in response.content
        )
    else:
        content_text = response.content

    sql = content_text.strip()
    sql = re.sub(r"```sql", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"```", "", sql)
    sql = sql.strip()

    return {
        "sql_query": sql,
        "error": None
    }


def execute_generated_sql(state: AgentState):
    sql_query = state["sql_query"]
    dataframe, error = execute_sql(sql_query)
    attempts = state.get("attempts", 0)
    
    if error:
        return {
            "dataframe": None,
            "error": error,
            "attempts": attempts + 1
        }

    return {
        "dataframe": dataframe,
        "error": None,
        "attempts": attempts + 1
    }

def check_sql_result(state: AgentState):
    if state["error"] is not None:
        if state["attempts"] < 3:
            return "repair"
        return "failed"
    return "success"

def repair_sql(state: AgentState): 
    question = state["question"]
    schema = state["schema"]
    previous_sql = state["sql_query"]
    error = state["error"] 
    
    prompt = f"""You are a SQL debugging expert.
You are working with SQLite. 
DATABASE SCHEMA: {schema}
USER QUESTION: {question} 
PREVIOUS SQL: {previous_sql}
SQL ERROR: {error} 

Fix the SQL query.
Rules: 
1. Return ONLY the corrected SQL. 
2. Do not use markdown. 
3. Do not explain anything.
4. Only use tables and columns from the schema.
5. Use SQLite-compatible syntax. 
6. Only generate SELECT queries. 
7. Do not modify the database."""

    response = llm.invoke(prompt)

    # Convert list content to string if necessary
    if isinstance(response.content, list):
        content_text = "".join(
            part.get("text", "") if isinstance(part, dict) else str(part)
            for part in response.content
        )
    else:
        content_text = response.content

    repaired_sql = content_text.strip()
    repaired_sql = re.sub(r"```sql", "", repaired_sql, flags=re.IGNORECASE)
    repaired_sql = re.sub(r"```", "", repaired_sql)
    repaired_sql = repaired_sql.strip()

    return {
        "sql_query": repaired_sql,
        "error": None
    }


def generate_insights(state: AgentState):
    dataframe = state["dataframe"]
    question = state["question"]
    
    if dataframe is None or dataframe.empty:
        return {"insights": "The query returned no data."}

    data_text = dataframe.to_string(index=False)
    prompt = f"""You are a data analyst.
The user asked: {question} 
The SQL query produced this result: 
{data_text} 

Give a concise analysis. Include: 
1. What the result shows. 
2. Important trends or observations. 
3. Useful business insight.
Do not invent information that is not present in the data.

Keep the response under 150 words."""

    response = llm.invoke(prompt)

    # Convert list content to string if necessary
    if isinstance(response.content, list):
        content_text = "".join(
            part.get("text", "") if isinstance(part, dict) else str(part)
            for part in response.content
        )
    else:
        content_text = response.content

    return {"insights": content_text.strip()}

graph_builder = StateGraph(AgentState)

graph_builder.add_node("get_schema", get_database_schema)
graph_builder.add_node("generate_sql", generate_sql)
graph_builder.add_node("execute_sql", execute_generated_sql)
graph_builder.add_node("repair_sql", repair_sql)
graph_builder.add_node("generate_insights", generate_insights)

graph_builder.add_edge(START, "get_schema")
graph_builder.add_edge("get_schema", "generate_sql")
graph_builder.add_edge("generate_sql", "execute_sql")

graph_builder.add_conditional_edges(
    "execute_sql", 
    check_sql_result,
    {
        "repair": "repair_sql",
        "success": "generate_insights",
        "failed": END
    }
)

graph_builder.add_edge("repair_sql", "execute_sql")
graph_builder.add_edge("generate_insights", END)

agent = graph_builder.compile()
#sql_generator.py

from core.llm import ask_llm
from utils.helpers import clean_sql
from config.business_rules import get_business_rules
from core.memory import update_memory, get_memory_filters


def generate_sql(question, schema_text, url, headers):

    # 🔥 NEW: update memory using LLM
    update_memory(question, url, headers)

    # get memory filters
    memory_filter = get_memory_filters()

    prompt = f"""
    You are a SQL expert.

    Schema:
    {schema_text}

    Memory Filters:
    {memory_filter}

    IMPORTANT:
    - If question refers to "this user", do NOT use memory filters
    - Instead assume it refers to last result (if unclear, return best guess)

    Instructions:
    - Apply filters only when relevant
    - Use JOINs when needed
    - Only return SQL

    Question:
    {question}
    """

    sql = ask_llm(prompt, url, headers)

    return clean_sql(sql)
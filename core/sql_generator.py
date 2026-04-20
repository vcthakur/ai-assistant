#sql_generator.py

from core.llm import ask_llm
from utils.helpers import clean_sql
from config.business_rules import get_business_rules
from core.memory import update_memory, get_memory_filters
from core.memory import get_entity_filter


def generate_sql(question, schema_text, url, headers):

    # 🔥 NEW: update memory using LLM
    update_memory(question, url, headers)

    # get memory filters
    memory_filter = get_memory_filters()
    entity_filter = get_entity_filter()

    prompt = f"""
    You are a SQL expert.

    Schema:
    {schema_text}

    Memory Filters:
    {memory_filter}

    Entity Filter (IMPORTANT):
    {entity_filter}

    Instructions:
    - If question refers to "this user", use Entity Filter
    - Otherwise use Memory Filters
    - Use JOINs when needed
    - Only return SQL

    Question:
    {question}
    """

    sql = ask_llm(prompt, url, headers)

    return clean_sql(sql)
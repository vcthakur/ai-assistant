from core.llm import ask_llm
from utils.helpers import clean_sql


def generate_sql(question, schema_text, url, headers):

    prompt = f"""
    You are a SQL expert.

    STRICT RULES:
    - Return ONLY SQL
    - Understand conversation context
    - Use previous context if question is dependent

    Schema:
    {schema_text}

    User Input:
    {question}
    """

    sql = ask_llm(prompt, url, headers)

    return clean_sql(sql)
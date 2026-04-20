#assistant.py

from core.sql_generator import generate_sql
from core.executor import run_sql
from core.llm import ask_llm
from core.memory import update_entity_memory, get_entity_filter

# memory
chat_history = []

def generate_sql_with_retry(question, schema_text, url, headers, spark, retries=2):

    error_msg = ""

    for i in range(retries):

        sql_query = generate_sql(question, schema_text, url, headers)

        result_text, result_df = run_sql(sql_query, spark)

        if "SQL Error" not in result_text:
            return sql_query, result_text, result_df

        error_msg = result_text

        question = f"""
        Fix this SQL based on error:

        Original Question: {question}
        Error: {error_msg}
        """

    return sql_query, result_text, result_df


def hybrid_assistant(user_input, schema_text, url, headers, spark):

    print("✅ Running from feature branch")

    chat_history.append({"role": "user", "content": user_input})

    sql_query, result_text, result_df = generate_sql_with_retry(
        user_input, schema_text, url, headers, spark
    )

    print("\n🔍 SQL:\n", sql_query)
    print("\n📊 Result:\n", result_text)
    
    # 🔥 NEW: store entity
    update_entity_memory(result_df)

    final_prompt = f"""
    You are a data analyst.

    Conversation:
    {chat_history}

    User Question:
    {user_input}

    SQL Result:
    {result_text}

    Instructions:
    - Give clear answer
    - Keep it simple
    """

    answer = ask_llm(final_prompt, url, headers)

    chat_history.append({"role": "assistant", "content": answer})

    return answer
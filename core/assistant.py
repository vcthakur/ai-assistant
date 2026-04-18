#assistant.py

from core.sql_generator import generate_sql
from core.executor import run_sql
from core.llm import ask_llm

# memory
chat_history = []


def generate_sql_with_retry(question, schema_text, url, headers, spark, retries=2):

    error_msg = ""

    for i in range(retries):

        # include chat history
        context = "\n".join([f"{c['role']}: {c['content']}" for c in chat_history])

        enhanced_question = f"""
        Conversation:
        {context}

        Current Question:
        {question}
        """

        sql_query = generate_sql(enhanced_question, schema_text, url, headers)

        result = run_sql(sql_query, spark)

        if "SQL Error" not in result:
            return sql_query, result

        error_msg = result

        question = f"""
        Fix this SQL based on error:

        Original Question: {question}
        Error: {error_msg}
        """

    return sql_query, result


def hybrid_assistant(user_input, schema_text, url, headers, spark):

    chat_history.append({"role": "user", "content": user_input})

    sql_query, result = generate_sql_with_retry(
        user_input, schema_text, url, headers, spark
    )

    print("\n🔍 SQL:\n", sql_query)
    print("\n📊 Result:\n", result)

    final_prompt = f"""
    You are a data analyst.

    Conversation:
    {chat_history}

    User Question:
    {user_input}

    SQL Result:
    {result}

    Instructions:
    - Give clear answer
    - Keep it simple
    """

    answer = ask_llm(final_prompt, url, headers)

    chat_history.append({"role": "assistant", "content": answer})

    return answer
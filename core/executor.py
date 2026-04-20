#executor.py

def is_safe_query(query):
    forbidden = ["DELETE", "UPDATE", "INSERT", "DROP", "ALTER", "CREATE", "TRUNCATE", "REPLACE", "MERGE", "REMOVE"]
    return not any(word in query.upper() for word in forbidden)


def run_sql(query, spark):

    if not is_safe_query(query):
        return "❌ Unsafe query blocked"

    try:
        df = spark.sql(query)

        if df.count() == 0:
            return "⚠️ No data found"

        return df.limit(10).toPandas().to_string(index=False)

    except Exception as e:
        return f"SQL Error: {str(e)}"
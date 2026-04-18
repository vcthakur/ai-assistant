#helpers.py

def clean_sql(query):
    query = query.strip()

    # Remove markdown
    query = query.replace("```sql", "").replace("```", "")

    # Find first SELECT
    select_index = query.upper().find("SELECT")
    if select_index == -1:
        return query

    query = query[select_index:]

    # Cut at first semicolon
    if ";" in query:
        query = query[:query.index(";")]

    return query.strip()
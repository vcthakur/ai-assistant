def get_llm_config(dbutils):
    
    host = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiUrl().get()
    token = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().get()

    endpoint = "databricks-meta-llama-3-1-8b-instruct"

    url = f"{host}/serving-endpoints/{endpoint}/invocations"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    return url, headers
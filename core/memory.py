from core.llm import ask_llm
import json

memory = {}

def extract_memory(user_input, url, headers):
 
    prompt = f"""
    Extract filters from the user query.
 
    Return ONLY JSON.
 
    Keys:
    state, gender, department
 
    Input: {user_input}
    """
 
    response = ask_llm(prompt, url, headers)
 
    # extract JSON part safely
    match = re.search(r"\{.*\}", response, re.DOTALL)
 
    if match:
        try:
            return json.loads(match.group())
        except:
            return {}
 
    return {}
    
def should_reset_memory(user_input):

    text = user_input.lower()

    keywords = [
        "this user",
        "that user",
        "his",
        "her",
        "their"
    ]

    return any(k in text for k in keywords)


def update_memory(user_input, url, headers):
    global memory

    # 🔥 NEW: reset if referring to specific entity
    if should_reset_memory(user_input):
        memory = {}

    extracted = extract_memory(user_input, url, headers)

    for key, value in extracted.items():
        memory[key] = value

    return memory

def get_memory_filters():

    conditions = []

    if "state" in memory:
        conditions.append(f"a.state = '{memory['state']}'")

    if "gender" in memory:
        conditions.append(f"u.gender = '{memory['gender']}'")

    if "department" in memory:
        conditions.append(f"c.department = '{memory['department']}'")

    return " AND ".join(conditions)


def reset_memory():
    global memory
    memory = {}
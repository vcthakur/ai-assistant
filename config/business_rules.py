def get_business_rules():

    return {
        "active users": "age > 30",
        "young users": "age < 25",
        "senior users": "age > 50",
        "male users": "gender = 'male'",
        "female users": "gender = 'female'"
    }
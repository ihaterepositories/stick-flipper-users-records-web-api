def serialize_individual(userrecord) -> dict:
    return {
        "id": str(userrecord["_id"]),
        "username": userrecord["username"],
        "bestscore": userrecord["bestscore"]
    }

def serialize_list(userrecords) -> list:
    return [serialize_individual(userrecord) for userrecord in userrecords]
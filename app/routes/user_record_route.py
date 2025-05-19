from config import userrecords_collection
from app.models.user_record import UserRecord
from app.utils.serialization.user_record_serializer import serialize_individual, serialize_list
from app.utils.responses.response_creator import ok, bad_request, server_error

from fastapi import APIRouter, Query, Body
from bson import ObjectId
from pymongo.errors import PyMongoError
from fastapi.exceptions import RequestValidationError

item_router = APIRouter()

# GET
@item_router.get("/userrecords", summary="Get all records")
async def get_all(
    sort: str = Query(None, description="Sort by field (e.g., 'bestscore')"),
    order: int = Query(1, description="Sort order (1 for ascending, -1 for descending)"),
    limit: int = Query(0, description="Limit the number of items to return"),
    skip: int = Query(0, description="Skip the first n items")
):
    try:
        # Validate the sort field
        valid_sort_fields = ["bestscore", "username", "created_at"]  # Add valid fields here
        if sort and sort not in valid_sort_fields:
            return bad_request(f"Invalid sort field: {sort}. Valid fields are {valid_sort_fields}.")

        # Build the query
        query = userrecords_collection.find()

        # Apply sorting if a valid sort field is provided
        if sort:
            query = query.sort(sort, order)

        # Apply limit and skip
        query = query.limit(limit).skip(skip)

        # Serialize the results
        user_records = serialize_list(query)

        return ok(user_records)

    except PyMongoError as e:
        return server_error(f"Server error: {e}")
    except Exception as e:
        return server_error(f"Server error: {e}")

# GET
@item_router.get("/userrecord/byUsername", summary="Get a record by username")
async def get(username: str = Query(None, description="UserRecord username")):

    if username is None:
        return bad_request("Username is required.")

    try:
        user_record = serialize_individual(userrecords_collection.find_one({"username": username}))
        return ok(user_record)
    
    except PyMongoError as e:
        return server_error(f"Server error: {e}")
    except Exception as e:
        return server_error(f"Server error: {e}")

# GET
@item_router.get("/userrecord/rank", summary="Get the rank of a user by username")
async def get_rank(username: str = Query(..., description="Username to find the rank for")):

    if username is None:
        return bad_request("Username is required.")

    try:
        
        user_records = serialize_list(
            userrecords_collection.find().sort("bestscore", -1)
        )

        for index, record in enumerate(user_records):
            if record["username"] == username:
                return ok({"rank": index + 1})

        return bad_request("User not found in the leaderboard.")

    except PyMongoError as e:
        return server_error(f"Server error: {e}")
    except Exception as e:
        return server_error(f"Server error: {e}")

# POST
@item_router.post("/userrecord", summary="Add a new record")
async def post(new_user_record: UserRecord = Body(..., description="User record to add")):

    if new_user_record is None or new_user_record.username is None or new_user_record.bestscore is None:
        return bad_request("Input is empty.")
    
    try:
        if not new_user_record.username:
            return bad_request("Username are required.")

        is_name_taken = userrecords_collection.find_one({"username": new_user_record.username})
        if is_name_taken:
            return bad_request("Username already taken.")

        userrecords_collection.insert_one(new_user_record.model_dump())
        return ok()
    
    except RequestValidationError as e:
        return bad_request(f"Validation error: {e.errors()}")
    except PyMongoError as e:
        return server_error(f"Server error: {e}")
    except Exception as e:
        return server_error(f"Server error: {e}")

# PUT
@item_router.put("/userrecord/update_record", summary="Update an existing record")
async def put(
    username: str = Query(..., description="Username of the record to update"), 
    new_record: str = Query(..., description="New record")
    ):

    if username is None:
        return bad_request("Username is required.")
    
    if new_record is None:
        return bad_request("New record is required.")
    
    try:
        user_record = userrecords_collection.find_one({"username": username})

        if user_record is None:
            return bad_request("User record not found.")
        
        user_record["bestscore"] = new_record
        updated_user_record = UserRecord(**user_record)
        userrecords_collection.update_one({"username": username}, {"$set": updated_user_record.model_dump()})
        return ok()
    
    except PyMongoError as e:
        return server_error(f"Server error: {e}")
    except Exception as e:
        return server_error(f"Server error: {e}")

# DELETE
@item_router.delete("/userrecord", summary="Delete an existing record")
async def delete(id: str = Query(None, description="User record ID to delete")):

    if id is None:
        return bad_request("ID is required.")
    
    try:
        userrecords_collection.delete_one({"_id": ObjectId(id)})
        return ok()
    
    except PyMongoError as e:
        return server_error(f"Server error: {e}")
    except Exception as e:
        return server_error(f"Server error: {e}")
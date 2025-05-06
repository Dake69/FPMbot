from database.db import db

users_collection = db["users"]

async def save_user(user_id: int, full_name: str, phone_number: str, previous_school: str):
    user_data = {
        "user_id": user_id,
        "full_name": full_name,
        "phone_number": phone_number,
        "previous_school": previous_school,
        "point_complited": [],
        "is_complited": False,
        "photo": None
    }
    await users_collection.update_one({"user_id": user_id}, {"$set": user_data}, upsert=True)

async def get_user(user_id: int):
    return await users_collection.find_one({"user_id": user_id})

async def delete_user(user_id: int):
    await users_collection.delete_one({"user_id": user_id})

async def update_user_photo(user_id: int, photo_id: str):
    await users_collection.update_one({"user_id": user_id}, {"$set": {"photo": photo_id}})


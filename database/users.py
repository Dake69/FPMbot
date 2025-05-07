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

async def get_all_photos():
    return await users_collection.find({"photo": {"$ne": None}}).to_list(length=None)

async def get_all_users():
    return await users_collection.find().to_list(length=None)

async def get_user_by_photo(photo_id: str):
    return await users_collection.find_one({"photo": photo_id})

async def get_user_by_id_and_point(user_id: int, point_code: int):
    user = await users_collection.find_one({"user_id": user_id, "point_complited": point_code})
    if user:
        return {
            "user_id": user["user_id"],
            "full_name": user.get("full_name", "Невідомий"),
            "point_complited": user.get("point_complited", [])
        }
    return None

async def get_point_complited_count(user_id: int):
    user = await users_collection.find_one({"user_id": user_id}, {"point_complited": 1})
    if user and "point_complited" in user:
        return len(user["point_complited"])
    return 0
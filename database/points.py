import random
from database.db import db

points_collection = db["points"]

async def generate_unique_code():
    while True:
        code = random.randint(100000, 999999)
        existing_point = await points_collection.find_one({"code": code})
        if not existing_point:
            return code

async def add_point(name: str, description: str):
    code = await generate_unique_code()
    point = {"name": name, "description": description, "code": code}
    await points_collection.insert_one(point)
    return point

async def get_point_by_code(code: int):
    return await points_collection.find_one({"code": code})

async def get_all_points():
    return await points_collection.find().to_list(length=None)

async def update_point(code: int, name: str = None, description: str = None):
    update_data = {}
    if name:
        update_data["name"] = name
    if description:
        update_data["description"] = description

    result = await points_collection.update_one({"code": code}, {"$set": update_data})
    return result.modified_count > 0

async def delete_point(code: int):
    result = await points_collection.delete_one({"code": code})
    return result.deleted_count > 0
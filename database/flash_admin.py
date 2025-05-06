import random
from database.db import db
from database.users import users_collection

flash_admins_collection = db["flash_admins"]

async def create_flash_admin(admin_id: int):
    admin_data = {
        "admin_id": admin_id,
        "photo_ratings": {},
        "remaining_photos": []
    }

    await flash_admins_collection.update_one({"admin_id": admin_id}, {"$set": admin_data}, upsert=True)

async def delete_flash_admin(admin_id: int):
    await flash_admins_collection.delete_one({"admin_id": admin_id})

async def get_flash_admin(admin_id: int):
    return await flash_admins_collection.find_one({"admin_id": admin_id})

async def get_all_flash_admins():
    return await flash_admins_collection.find().to_list(length=None)

async def shuffle_photos_for_all_admins():
    admins = await flash_admins_collection.find({}, {"admin_id": 1}).to_list(length=None)
    if not admins:
        return

    for admin in admins:
        photos = await users_collection.find({"photo": {"$ne": None}}, {"photo": 1}).to_list(length=None)
        photo_ids = [photo["photo"] for photo in photos]

        random.shuffle(photo_ids)

        await flash_admins_collection.update_one(
            {"admin_id": admin["admin_id"]},
            {"$set": {"remaining_photos": photo_ids}}
        )

async def get_random_photo_for_admin(admin_id: int):
    admin = await flash_admins_collection.find_one({"admin_id": admin_id})
    if not admin or not admin["remaining_photos"]:
        return None

    return admin["remaining_photos"][0]

async def rate_photo(admin_id: int, photo_id: str, rating: int):
    await flash_admins_collection.update_one(
        {"admin_id": admin_id},
        {
            "$set": {f"photo_ratings.{photo_id}": rating},
            "$pull": {"remaining_photos": photo_id}
        }
    )

async def get_admin_ratings(admin_id: int):
    admin = await flash_admins_collection.find_one({"admin_id": admin_id})
    if not admin:
        return None
    return admin.get("photo_ratings", {})
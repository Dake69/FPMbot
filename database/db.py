import motor.motor_asyncio

#from config import MONGO_URI

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb+srv://bilenkoartur6:yMVBWRoAeIqDfpBB@cluster0.bamjzjf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

db = client["autoWelder"]

async def test_connection():
    try:
        collections = await db.list_collection_names()
        print(f"✅ Успішно підключено до MongoDB! Колекції: {collections}")
    except Exception as e:
        print(f"❌ Помилка підключення до MongoDB: {e}")
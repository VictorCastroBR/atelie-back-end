from pymongo import MongoClient
from bson import ObjectId
from src.infrastructure.config import settings
from src.core.entities.user import User

client = MongoClient(settings.MONGO_URI)
db = client[settings.DATABASE_NAME]
users_collection = db["users"]

def create_user(user: User) -> str:
    user_dict = user.dict(exclude={"id"})
    result = users_collection.insert_one(user_dict)
    return str(result.inserted_id)

def find_user_by_email(email: str) -> User | None:
    doc = users_collection.find_one({"email": email})
    if doc:
        return User(id=str(doc["_id"]), **doc)
    return None
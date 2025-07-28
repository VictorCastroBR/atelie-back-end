from pymongo import MongoClient
from bson import ObjectId
from src.infrastructure.config import settings
from src.core.entities.user import User
from src.core.entities.product import Product

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

products_collection = db["products"]

def create_product(product: Product) -> str:
    doc = product.dict(exclude={"id"})
    result = products_collection.insert_one(doc)
    return str(result.inserted_id)

def list_products() -> list[Product]:
    docs = products_collection.find()
    return [Product(id=str(doc["_id"]), **doc) for doc in docs]